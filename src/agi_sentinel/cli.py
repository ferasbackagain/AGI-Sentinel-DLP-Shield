"""
AGI Sentinel CLI - Working Version
"""

import argparse
import sys
import json
from pathlib import Path

# استيراد ثابت من core
from .core import AGISentinelCore, AGISentinel, ScanResult

def display_banner():
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║               DLP SHIELD v2.1.0 - ENTERPRISE EDITION         ║
    ║         Advanced AI Security Protection System              ║
    ║                                                              ║
    ║               Author: Feras Khatib                          ║
    ║           Senior AI Security Engineer                       ║
    ║               License: AGPLv3                               ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_result(result: ScanResult, verbose: bool = False):
    print("\n" + "="*60)
    print("SCAN RESULTS")
    print("="*60)
    
    print(f"Status: {result.status}")
    print(f"Original length: {len(result.original_text)} chars")
    print(f"Protected length: {len(result.processed_text)} chars")
    print(f"Threats detected: {len(result.incidents)}")
    
    if result.incidents:
        print(f"\nDetected Threats:")
        for incident in result.incidents[:5]:
            print(f"  • {incident.threat_type} ({incident.severity})")
        
        if len(result.incidents) > 5:
            print(f"  ... and {len(result.incidents) - 5} more")
    
    if verbose and result.incidents:
        print(f"\nDetailed Incidents:")
        for incident in result.incidents:
            print(f"\n  Incident ID: {incident.incident_id}")
            print(f"  Type: {incident.threat_type}")
            print(f"  Severity: {incident.severity}")
            print(f"  Action: {incident.action_taken}")
            print(f"  Timestamp: {incident.timestamp}")
    
    if verbose:
        print(f"\nProtected Text:")
        print(f"  {result.processed_text}")
    
    print("="*60)

def main():
    display_banner()
    
    parser = argparse.ArgumentParser(
        description="AGI Sentinel - Advanced DLP for AI Systems"
    )
    
    parser.add_argument("--text", help="Text to scan")
    parser.add_argument("--csv", help="CSV file for bulk scanning")
    parser.add_argument("--cols", nargs='+', help="Columns to scan", default=None)
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--config", help="Custom configuration file")
    parser.add_argument("--workers", type=int, default=4, help="Parallel workers")
    parser.add_argument("--export", help="Export results to JSON file")
    
    args = parser.parse_args()
    
    try:
        # Initialize sentinel
        sentinel = AGISentinelCore(
            config_path=args.config,
            max_workers=min(args.workers, 16)
        )
        
        # Mode 1: Single text scan
        if args.text:
            if args.verbose:
                print(f"[*] Scanning text ({len(args.text)} characters)...")
            
            result = sentinel.scan_text(args.text)
            
            print_result(result, args.verbose)
            
            # Export if requested
            if args.export:
                export_path = Path(args.export)
                with open(export_path, 'w', encoding='utf-8') as f:
                    json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
                
                print(f"[+] Results exported to: {export_path}")
        
        # Mode 2: CSV file scan
        elif args.csv:
            if args.verbose:
                print(f"[*] Starting bulk scan of {args.csv}")
                print(f"[*] Workers: {args.workers}, Columns: {args.cols or 'ALL'}")
            
            result = sentinel.scan_file(
                file_path=args.csv,
columns=args.cols
            )
            
            if result['status'] == 'COMPLETED':
                print(f"\n[+] Scan completed successfully!")
                print(f"[+] Output file: {result['output_file']}")
                print(f"[+] Rows processed: {result.get('rows_processed', 'N/A')}")
                print(f"[+] Columns shielded: {result.get('columns_shielded', [])}")
            else:
                print(f"[!] Scan failed: {result.get('error', 'Unknown error')}")
        
        # No input provided
        else:
            print("\n[AGI-SENTINEL NOTICE]")
            print("No input file or text was provided.")
            print("\nPlease provide one of the following options:")
            print("  --text \"your text here\"")
            print("  --csv  <file.csv>  --cols <column_name1> <column_name2>")
            print("\nExample:")
            print("  python -m src.agi_sentinel.cli --text \"test@example.com\"")
            print("  python -m src.agi_sentinel.cli --csv data.csv --cols email phone")
    
    except KeyboardInterrupt:
        print("\n[!] Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)
    
    # Final message
    if args.text or args.csv:
        print("\n" + "="*60)
        print("[*] AGI Sentinel operation completed")
        print("="*60)

if __name__ == "__main__":
    main()

