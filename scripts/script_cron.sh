#!/bin/bash
# =================================================================
# AGI Sentinel - Production Cron Runner (ENHANCED)
# Author: Feras Khatib
# Role: Senior AI Security Engineer
# License: AGPLv3
# Version: 2.1.0
# Purpose: Automated DLP Enforcement for AI/AGI Data
# =================================================================

# Strict mode with proper syntax (FIXED from original)
set -euo pipefail
IFS=$'\n\t'

# ==================== CONFIGURATION ====================
readonly BASE_DIR="/opt/agi_sentinel"
readonly PYTHON_BIN="/usr/bin/python3"
readonly SCRIPT_NAME="cli.py"
readonly SCRIPT_PATH="${BASE_DIR}/src/agi_sentinel/${SCRIPT_NAME}"

# Input/Output configuration
readonly INPUT_DIR="${BASE_DIR}/data/incoming"
readonly PROCESSED_DIR="${BASE_DIR}/data/processed"
readonly OUTPUT_DIR="${BASE_DIR}/data/shielded"
readonly FAILED_DIR="${BASE_DIR}/data/failed"

# Logging configuration
readonly LOG_DIR="${BASE_DIR}/logs"
readonly LOG_FILE="${LOG_DIR}/sentinel_cron_$(date +%Y%m%d).log"
readonly AUDIT_LOG="${LOG_DIR}/security_audit.json"

# Locking (prevent overlapping runs)
readonly LOCK_FILE="/tmp/agi_sentinel.lock"
readonly LOCK_TIMEOUT=300  # 5 minutes

# Processing configuration
readonly MAX_WORKERS=4
readonly CHUNK_SIZE=10000
readonly MAX_FILE_SIZE_MB=100

# ==================== FUNCTIONS ====================

log_message() {
    local level="$1"
    local message="$2"
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    # Format: JSON for machine parsing
    local log_entry="{\"timestamp\":\"${timestamp}\",\"level\":\"${level}\",\"message\":\"${message}\"}"
    
    # Write to daily log file
    echo "${log_entry}" >> "${LOG_FILE}"
    
    # Also write to console if not in cron
    if [[ -t 0 ]]; then
        echo "[${timestamp}] ${level}: ${message}"
    fi
}

log_audit_event() {
    local event_type="$1"
    local file_name="$2"
    local details="$3"
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    local audit_entry="{\"timestamp\":\"${timestamp}\",\"event\":\"${event_type}\",\"file\":\"${file_name}\",\"details\":${details}}"
    
    echo "${audit_entry}" >> "${AUDIT_LOG}"
}

validate_environment() {
    # Check Python
    if ! command -v "${PYTHON_BIN}" &> /dev/null; then
        log_message "ERROR" "Python not found: ${PYTHON_BIN}"
        return 1
    fi
    
    # Check script exists
    if [[ ! -f "${SCRIPT_PATH}" ]]; then
        log_message "ERROR" "Main script not found: ${SCRIPT_PATH}"
        return 1
    fi
    
    # Check directories
    for dir in "${INPUT_DIR}" "${PROCESSED_DIR}" "${OUTPUT_DIR}" "${FAILED_DIR}" "${LOG_DIR}"; do
        if [[ ! -d "${dir}" ]]; then
            mkdir -p "${dir}"
            log_message "INFO" "Created directory: ${dir}"
        fi
    done
    
    # Check write permissions
    for dir in "${INPUT_DIR}" "${PROCESSED_DIR}" "${OUTPUT_DIR}" "${FAILED_DIR}" "${LOG_DIR}"; do
        if [[ ! -w "${dir}" ]]; then
            log_message "ERROR" "No write permission: ${dir}"
            return 1
        fi
    done
    
    return 0
}

check_file_size() {
    local file_path="$1"
    local max_size_mb="$2"
    
    if [[ ! -f "${file_path}" ]]; then
        return 1
    fi
    
    local file_size_bytes
    file_size_bytes=$(stat -f%z "${file_path}" 2>/dev/null || stat -c%s "${file_path}" 2>/dev/null)
    local file_size_mb=$((file_size_bytes / 1024 / 1024))
    
    if [[ ${file_size_mb} -gt ${max_size_mb} ]]; then
        log_message "WARNING" "File ${file_path} exceeds size limit: ${file_size_mb}MB > ${max_size_mb}MB"
        return 1
    fi
    
    return 0
}

process_csv_file() {
    local input_file="$1"
    local filename
    filename=$(basename "${input_file}")
    
    log_message "INFO" "Processing file: ${filename}"
    log_audit_event "PROCESS_START" "${filename}" "{\"action\":\"scan_start\"}"
    
    # Generate output filename
    local output_file="${OUTPUT_DIR}/shielded_${filename}"
    
    # Run AGI Sentinel
    local start_time
    start_time=$(date +%s)
    
    if "${PYTHON_BIN}" -c "
import sys
sys.path.insert(0, '${BASE_DIR}')
from src.agi_sentinel.cli import main
sys.argv = ['cli.py', '--csv', '${input_file}', '--workers', '${MAX_WORKERS}', '--quiet']
main()
    " >> "${LOG_FILE}" 2>&1; then
        
        local end_time
        end_time=$(date +%s)
        local duration=$((end_time - start_time))
        
        # Check if output was created
        if [[ -f "${input_file}.shielded" ]]; then
            mv "${input_file}.shielded" "${output_file}"
            log_message "INFO" "Successfully processed ${filename} in ${duration}s"
            log_audit_event "PROCESS_SUCCESS" "${filename}" "{\"action\":\"scan_complete\",\"duration\":${duration},\"output\":\"${output_file}\"}"
            
            # Move original to processed
            mv "${input_file}" "${PROCESSED_DIR}/${filename}"
            return 0
        else
            log_message "ERROR" "Output file not created for: ${filename}"
            log_audit_event "PROCESS_ERROR" "${filename}" "{\"action\":\"output_missing\"}"
            return 1
        fi
    else
        local end_time
        end_time=$(date +%s)
        local duration=$((end_time - start_time))
        
        log_message "ERROR" "Failed to process: ${filename} (after ${duration}s)"
        log_audit_event "PROCESS_ERROR" "${filename}" "{\"action\":\"scan_failed\",\"duration\":${duration}}"
        return 1
    fi
}

cleanup_old_files() {
    local days_to_keep=30
    
    # Cleanup processed files older than X days
    find "${PROCESSED_DIR}" -type f -mtime +${days_to_keep} -delete 2>/dev/null || true
    
    # Cleanup log files older than 90 days
    find "${LOG_DIR}" -name "sentinel_cron_*.log" -mtime +90 -delete 2>/dev/null || true
    
    log_message "INFO" "Cleanup completed (files older than ${days_to_keep} days)"
}

# ==================== MAIN EXECUTION ====================

main() {
    log_message "INFO" "=== AGI Sentinel Cron Job Started ==="
    
    # Validate environment
    if ! validate_environment; then
        log_message "ERROR" "Environment validation failed"
        exit 1
    fi
    
    # Acquire lock with timeout
    exec 9>"${LOCK_FILE}"
    if ! flock -w ${LOCK_TIMEOUT} 9; then
        log_message "WARNING" "Could not acquire lock. Another instance may be running."
        exit 0
    fi
    
    # Log lock acquisition
    log_message "INFO" "Lock acquired: ${LOCK_FILE}"
    
    # Check for files to process
    local files_to_process=()
    for file in "${INPUT_DIR}"/*.csv "${INPUT_DIR}"/*.CSV; do
        if [[ -f "${file}" ]]; then
            # Validate file
            if ! check_file_size "${file}" ${MAX_FILE_SIZE_MB}; then
                log_message "WARNING" "Skipping oversized file: $(basename "${file}")"
                mv "${file}" "${FAILED_DIR}/" 2>/dev/null || true
                continue
            fi
            
            # Check if file is still being written (wait if less than 5 minutes old)
            local file_age
            file_age=$(($(date +%s) - $(stat -c %Y "${file}")))
            if [[ ${file_age} -lt 300 ]]; then
                log_message "INFO" "File is recent, may still be uploading: $(basename "${file}")"
                continue
            fi
            
            files_to_process+=("${file}")
        fi
    done
    
    if [[ ${#files_to_process[@]} -eq 0 ]]; then
        log_message "INFO" "No files to process"
    else
        log_message "INFO" "Found ${#files_to_process[@]} file(s) to process"
        
        # Process each file
        local processed_count=0
        local failed_count=0
        
        for file in "${files_to_process[@]}"; do
            if process_csv_file "${file}"; then
                ((processed_count++))
            else
                ((failed_count++))
                # Move failed file
                mv "${file}" "${FAILED_DIR}/" 2>/dev/null || true
            fi
        done
        
        log_message "INFO" "Processing complete: ${processed_count} succeeded, ${failed_count} failed"
    fi
    
    # Cleanup old files
    cleanup_old_files

# Release lock
    flock -u 9
    log_message "INFO" "Lock released"
    
    log_message "INFO" "=== AGI Sentinel Cron Job Completed ==="
    
    return 0
}

# ==================== EXECUTION ====================
# Trap signals for graceful shutdown
trap 'log_message "WARNING" "Script interrupted by signal"; exit 130' INT TERM

# Run main function
main "$@"

# Exit with appropriate code
exit $?
