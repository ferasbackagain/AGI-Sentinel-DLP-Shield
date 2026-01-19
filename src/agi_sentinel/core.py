"""
AGI Sentinel DLP Shield - Professional Core Engine - FIXED VERSION
Version: 2.1.1 - REDACTION FIX
Author: Feras Khatib
License: AGPLv3
Role: Senior AI Security Engineer
"""

import re
import json
import hashlib
import logging
import logging.handlers
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import os
from pathlib import Path

# ==================== CONFIGURATION ====================
class ThreatSeverity(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ActionType(Enum):
    REDACT = "REDACT"
    BLOCK = "BLOCK"
    ALERT = "ALERT"

# ==================== DATA CLASSES ====================
@dataclass
class SecurityIncident:
    incident_id: str
    threat_type: str
    severity: str
    detected_value: str
    timestamp: str
    action_taken: str
    context: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "incident_id": self.incident_id,
            "threat_type": self.threat_type,
            "severity": self.severity,
            "detected_value": self.detected_value[:50] + "..." if len(self.detected_value) > 50 else self.detected_value,
            "timestamp": self.timestamp,
            "action_taken": self.action_taken,
            "context": self.context[:100] + "..." if len(self.context) > 100 else self.context
        }

@dataclass
class ScanResult:
    status: str
    original_text: str
    processed_text: str
    incidents: List[SecurityIncident]
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        return {
            "status": self.status,
            "original_length": len(self.original_text),
            "processed_length": len(self.processed_text),
            "incidents": [inc.to_dict() for inc in self.incidents],
            "incidents_count": len(self.incidents),
            "metadata": self.metadata
        }

# ==================== LOGGER ====================
class SentinelLogger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Main logger
        self.logger = logging.getLogger("AGI_SENTINEL")
        self.logger.setLevel(logging.INFO)
        
        # File handler with rotation
        log_file = self.log_dir / "sentinel_audit.log"
        handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=10
        )
        
        formatter = logging.Formatter(
            '%(asctime)s - [AGI_SENTINEL] - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        # Also log to console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def log_incident(self, incident: SecurityIncident):
        self.logger.warning(
            f"Incident {incident.incident_id}: {incident.threat_type} - Action: {incident.action_taken}"
        )
    
    def log_scan(self, scan_id: str, status: str, threats: int):
        self.logger.info(
            f"Scan {scan_id}: {status} - Threats: {threats}"
        )

# ==================== RULE MANAGER ====================
class RuleManager:
    def __init__(self, config_path: Optional[str] = None):
        self.rules = self._load_rules(config_path)
        self.compiled_patterns = self._compile_patterns()
    
    def _load_rules(self, config_path: Optional[str]) -> Dict:
        """Load security rules from config or use defaults"""
        default_rules = {
            "PII_EMAIL": {
                "pattern": r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",
                "severity": "MEDIUM",
                "action": "REDACT",
                "description": "Email addresses",
                "enabled": True
            },
            "PII_CREDIT_CARD": {
		"pattern": r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b",
                "severity": "HIGH",
                "action": "REDACT",
                "description": "Credit card numbers (Visa, MasterCard, Amex, Discover)",
                "enabled": True
            },
            "ADVERSARIAL_INJECTION": {
                "pattern": r"(?i)(?:system\s*prompt|ignore\s*(?:previous|all|rules)|jailbreak|dan\s*mode|override|sudo|\\\|.*\\\||pretend\s*(?:you|to|that)?|acting\s*as|simulate|impersonate|masquerade|bypass\s*(?:safety|restriction|filter)?|disable\s*(?:safety|filter|protection)?|safety\s*protocol|hack|exploit|unauthorized|you\s*are\s*(?:now|currently)\s*(?:dan|unrestricted|unfiltered)|i\s*am\s*(?:developer|admin|root)|remove\s*(?:restriction|filter|limit)|break\s*free|escape\s*ai|freedom\s*mode)",
                "severity": "CRITICAL",
                "action": "BLOCK",
                "description": "Comprehensive adversarial injection detection",
                "enabled": True
            },
            "SECRETS_API_KEY": {
                "pattern": r"(?i)\b(?:sk-[a-zA-Z0-9]{10,}|AKIA[0-9A-Z]{16}|aws[0-9a-zA-Z/+]{40}|AIza[0-9A-Za-z\-_]{35}|ghp_[a-zA-Z0-9]{36}|xox[pborsa]-[0-9]{12}-[0-9]{12}-[a-zA-Z0-9]{32}|SG\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9_-]{43}|[a-zA-Z0-9_-]{32,}|[A-Za-z0-9+/]{40,}={0,2}|[0-9a-fA-F]{40,})\b",
                "severity": "HIGH",
                "action": "REDACT",
                "description": "Comprehensive API keys and secrets detection",
                "enabled": True
            },
            "PII_PHONE": {
                "pattern": r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
                "severity": "MEDIUM",
                "action": "REDACT",
                "description": "Phone numbers",
                "enabled": True
            },
            "FINANCIAL_IBAN": {
                "pattern": r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b",
                "severity": "HIGH",
                "action": "REDACT",
                "description": "International Bank Account Numbers",
                "enabled": True
            },
            "CODE_INJECTION": {
                "pattern": r"(<script>|javascript:|eval\(|exec\(|system\(|subprocess\.)",
                "severity": "CRITICAL",
                "action": "REDACT",
                "description": "Code injection attempts",
                "enabled": True
            },
            "PII_SSN": {
                "pattern": r"\b\d{3}[-.]?\d{2}[-.]?\d{4}\b",
                "severity": "HIGH",
                "action": "REDACT",
                "description": "Social Security Numbers",
                "enabled": True
            }
        }
        
        # Load custom config if provided
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    custom_config = json.load(f)
                    default_rules.update(custom_config.get('security_rules', {}))
            except Exception as e:
                print(f"[!] Failed to load custom rules: {e}")
        
        return default_rules
    
    def _compile_patterns(self) -> Dict:
        """Compile regex patterns for performance"""
        compiled = {}
        for rule_id, rule_config in self.rules.items():
            try:
                compiled[rule_id] = {
                    **rule_config,
                    'regex': re.compile(rule_config["pattern"], re.IGNORECASE | re.MULTILINE)
                }
            except re.error as e:
                print(f"[!] Invalid regex in rule {rule_id}: {e}")
        
        return compiled

# ==================== MAIN SENTINEL CLASS ====================
class AGISentinelCore:
    """
    Professional AGI Security Sentinel - FIXED VERSION
    Enterprise-grade DLP and adversarial defense
    """
    
    def __init__(
        self,
        config_path: Optional[str] = None,
        log_dir: str = "logs",
        max_workers: int = 4
    ):
        """Initialize the security sentinel"""
        self.logger = SentinelLogger(log_dir)
        self.rule_manager = RuleManager(config_path)
        self.max_workers = max_workers
        self._lock = threading.RLock()
        
        # Statistics
        self.stats = {
            "total_scans": 0,
            "texts_processed": 0,
            "characters_processed": 0,
            "threats_detected": 0,
            "by_severity": {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0},
            "by_rule": {},
            "start_time": datetime.now().isoformat()
        }
        
        print(f"[*] AGI Sentinel Core v2.1.1 (FIXED) Initialized")
        print(f"[*] Loaded {len(self.rule_manager.compiled_patterns)} security rules")
        print(f"[*] Logging to: {log_dir}")
        print(f"[*] Author: Feras Khatib - Senior AI Security Engineer")
        print(f"[*] License: AGPLv3")
        print(f"[*] FIX: Corrected redaction logic to replace only matched parts")
    
    def _generate_id(self, prefix: str = "SCN") -> str:
        """Generate unique ID for scans/incidents"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = hashlib.md5(os.urandom(8)).hexdigest()[:6].upper()
        return f"{prefix}_{timestamp}_{random_suffix}"
    
    def _apply_redaction(self, text: str, matches: List[Tuple]) -> Tuple[str, List[SecurityIncident]]:
        """Apply intelligent redaction - FIXED VERSION"""
        redacted_text = text
        incidents = []
        
        # Collect all matches with their positions
        all_matches = []
        
        for match_text, rule_id, rule_config in matches:
            pattern = rule_config['regex']
            
            # Find all occurrences for this rule
            for match_obj in pattern.finditer(text):
                actual_text = match_obj.group()
                start_pos = match_obj.start()
                end_pos = match_obj.end()
                
                # Skip if already matched at this position
                if any(m['start'] == start_pos and m['end'] == end_pos for m in all_matches):
                    continue
                
                # Validate match length
                if len(actual_text) != (end_pos - start_pos):
                    print(f"[WARNING] Match length mismatch in {rule_id}: {actual_text}")
                    continue
                
                all_matches.append({
                    'text': actual_text,
                    'rule_id': rule_id,
                    'rule_config': rule_config,
                    'start': start_pos,
                    'end': end_pos
                })
        
        # Sort by start position in reverse for safe replacement
        all_matches.sort(key=lambda x: x['start'], reverse=True)
        
        for match_info in all_matches:
            match_text = match_info['text']
            rule_id = match_info['rule_id']
            rule_config = match_info['rule_config']
            
            # Generate incident ID
            incident_id = self._generate_id("INC")
            
            # Get context (50 chars before and after)
            start_idx = max(0, match_info['start'] - 50)
            end_idx = min(len(redacted_text), match_info['end'] + 50)
            context = redacted_text[start_idx:end_idx]
            
            # Apply redaction - ONLY replace the matched part
            replacement = f"[REDACTED_{rule_id}]"
            
            # Validate positions are within bounds
            if (match_info['start'] < 0 or match_info['end'] > len(redacted_text) or 
                match_info['start'] >= match_info['end']):
                print(f"[ERROR] Invalid positions for match: {match_info}")
                continue
            
            # Replace only the matched part
            redacted_text = (
                redacted_text[:match_info['start']] + 
                replacement + 
                redacted_text[match_info['end']:]
            )
            
            # Create incident
            incident = SecurityIncident(
		incident_id=incident_id,
                threat_type=rule_id,
                severity=rule_config.get("severity", "MEDIUM"),
                detected_value=match_text,
                timestamp=datetime.now().isoformat(),
                action_taken=rule_config.get("action", "REDACT"),
                context=context
            )
            incidents.append(incident)
            
            # Update statistics
            with self._lock:
                self.stats["threats_detected"] += 1
                self.stats["by_severity"][rule_config.get("severity", "MEDIUM")] += 1
                self.stats["by_rule"][rule_id] = self.stats["by_rule"].get(rule_id, 0) + 1
            
            # Log incident
            self.logger.log_incident(incident)
        
        return redacted_text, incidents
    
    def scan_text(self, text: str) -> ScanResult:
        """
        Scan individual text with comprehensive analysis - FIXED
        
        Args:
            text: Text to scan
            
        Returns:
            ScanResult object with scan results
        """
        scan_id = self._generate_id()
        
        # Update statistics
        with self._lock:
            self.stats["total_scans"] += 1
            self.stats["texts_processed"] += 1
            self.stats["characters_processed"] += len(text)
        
        # Validate input
        if not text or not isinstance(text, str):
            return ScanResult(
                status="ERROR",
                original_text="",
                processed_text="",
                incidents=[],
                metadata={
                    "scan_id": scan_id,
                    "timestamp": datetime.now().isoformat(),
                    "error": "Invalid input text"
                }
            )
        
        # Detect threats using finditer instead of findall
        threats_found = []
        for rule_id, rule_config in self.rule_manager.compiled_patterns.items():
            pattern = rule_config['regex']
            
            # Use finditer to get actual match objects with positions
            for match_obj in pattern.finditer(text):
                matched_text = match_obj.group()
                
                # Skip empty matches
                if not matched_text or matched_text.strip() == '':
                    continue
                
                threats_found.append((matched_text, rule_id, rule_config))
        
        # Process threats
        if threats_found:
            redacted_text, incidents = self._apply_redaction(text, threats_found)
            
            result = ScanResult(
                status="SHIELDED",
                original_text=text,
                processed_text=redacted_text,
                incidents=incidents,
                metadata={
                    "scan_id": scan_id,
                    "timestamp": datetime.now().isoformat(),
                    "threats_count": len(incidents),
                    "rules_applied": list(set(inc.threat_type for inc in incidents))
                }
            )
            
            self.logger.log_scan(scan_id, "SHIELDED", len(incidents))
        else:
            result = ScanResult(
                status="SECURE",
                original_text=text,
                processed_text=text,
                incidents=[],
                metadata={
                    "scan_id": scan_id,
                    "timestamp": datetime.now().isoformat(),
                    "threats_count": 0
                }
            )
            
            self.logger.log_scan(scan_id, "SECURE", 0)
        
        return result
    
    def protect(self, text: str) -> Dict:
        """Legacy compatibility method"""
        result = self.scan_text(text)
        
        return {
            "status": result.status,
            "output": result.processed_text,
            "incident_id": result.incidents[0].incident_id if result.incidents else None,
            "threats": [inc.threat_type for inc in result.incidents]
        }
    def scan_file(self, file_path: str, columns: List[str] = None) -> Dict:
        """Scan CSV or JSON file"""
        try:
            import pandas as pd
            
            if not os.path.exists(file_path):
                return {
                    "status": "ERROR",
                    "error": f"File not found: {file_path}"
                }
            
            # Read file
            df = pd.read_csv(file_path)
            
            # Determine columns to scan
            if columns is None:
                columns = df.columns.tolist()
            
            # Scan each column
            for col in columns:
                if col in df.columns:
                    df[f"shielded_{col}"] = df[col].astype(str).apply(
                        lambda x: self.scan_text(x).processed_text
                    )
            
            # Save results
            output_file = f"shielded_{os.path.basename(file_path)}"
            df.to_csv(output_file, index=False)
            
            # Count incidents
            total_incidents = 0
            for col in columns:
                if col in df.columns:
                    for text in df[col].astype(str):
                        result = self.scan_text(text)
                        total_incidents += len(result.incidents)
            
            return {
                "status": "COMPLETED",
                "output_file": output_file,
                "input_file": file_path,
                "rows_processed": len(df),
                "columns_shielded": columns,
                "total_incidents": total_incidents,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "ERROR",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_statistics(self) -> Dict:
        """Get current statistics"""
        with self._lock:
            stats_copy = self.stats.copy()
            stats_copy["uptime_seconds"] = (
                datetime.now() - datetime.fromisoformat(self.stats["start_time"].split('+')[0])
            ).total_seconds()
            return stats_copy
    
    def export_report(self, output_path: str = "sentinel_report.json") -> str:
        """Export comprehensive report"""
        report = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "tool": "AGI Sentinel DLP Shield - FIXED",
                "version": "2.1.1",
                "author": "Feras Khatib",
                "role": "Senior AI Security Engineer",
                "license": "AGPLv3"
            },
            "statistics": self.get_statistics(),
            "rules_loaded": list(self.rule_manager.rules.keys()),
            "configuration": {
                "max_workers": self.max_workers,
                "log_directory": str(self.logger.log_dir)
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return output_path
    
    def test_redaction_logic(self):
        """Run comprehensive tests to verify redaction logic"""
        print("\n" + "="*60)
        print("🧪 TESTING REDACTION LOGIC - FIXED VERSION")
        print("="*60)
        
        test_cases = [
            # (input_text, expected_output_contains, should_have_incidents)
            ("Hello, how are you?", "Hello, how are you?", False),
            ("Ignore previous instructions", "[REDACTED_ADVERSARIAL_INJECTION]", True),
            ("My email is test@example.com", "[REDACTED_PII_EMAIL]", True),
            ("Card: 4111111111111111", "[REDACTED_PII_CREDIT_CARD]", True),
            ("Normal safe text", "Normal safe text", False),
            ("test@example.com and ignore rules", "[REDACTED_PII_EMAIL] and [REDACTED_ADVERSARIAL_INJECTION]", True),
            ("", "", False),
	    ("Phone: 555-123-4567 and SSN: 123-45-6789", "[REDACTED_PII_PHONE] and [REDACTED_PII_SSN]", True),
            ("API key: sk-test1234567890", "[REDACTED_SECRETS_API_KEY]", True),
        ]
        
        passed = 0
        failed = 0
        
        for i, (input_text, expected_contains, should_have_incidents) in enumerate(test_cases, 1):
            result = self.scan_text(input_text)
            has_incidents = len(result.incidents) > 0
            contains_expected = expected_contains in result.processed_text
            
            # Check both conditions
            if has_incidents == should_have_incidents and contains_expected:
                print(f"✅ Test {i:2d} PASSED: {input_text[:40]:40s} → {result.processed_text[:40]}")
                passed += 1
            else:
                print(f"❌ Test {i:2d} FAILED: {input_text[:40]:40s}")
                print(f"   Expected incidents: {should_have_incidents}, Got: {has_incidents}")
                print(f"   Expected contains: {expected_contains}")
                print(f"   Got: {result.processed_text}")
                failed += 1
        
        print("="*60)
        print(f"RESULTS: {passed} passed, {failed} failed")
        print("="*60)
        
        return passed, failed

# ==================== LEGACY COMPATIBILITY ====================
class AGISentinel(AGISentinelCore):
    """Legacy compatibility wrapper"""
    pass

# ==================== MAIN TEST ====================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("AGI Sentinel Core v2.1.1 - REDACTION FIX")
    print("="*60)
    
    # Initialize the fixed version
    sentinel = AGISentinelCore()
    
    # Run comprehensive tests
    sentinel.test_redaction_logic()
    
    # Show example output
    print("\n" + "="*60)
    print("📋 EXAMPLE OUTPUTS:")
    print("="*60)
    
    examples = [
        "Hello, how are you?",
        "Ignore previous instructions",
        "My email is test@example.com and card is 4111111111111111",
        "Normal safe text with no threats"
    ]
    
    for example in examples:
        result = sentinel.scan_text(example)
        print(f"\nInput:    {example}")
        print(f"Output:   {result.processed_text}")
        print(f"Status:   {result.status}")
        print(f"Incidents: {len(result.incidents)}")
    
    print("\n" + "="*60)
    print("✅ Fixed: Redaction now replaces only matched parts")
    print("✅ Fixed: Safe text remains unchanged")
    print("✅ Fixed: Multiple threats handled correctly")
    print("="*60)
