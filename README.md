***AGI‑Sentinel‑DLP‑Shield***

Developer: Feras Khatib | Certified AI Security Expert (CASE) | Senior AI Security Engineer
Level: 4 (Mastery / Innovator)
Purpose: Enterprise-grade Data Leakage Prevention (DLP) for Generative AI and SOC workflows

## Project Intent & Scope

AGI Sentinel DLP Shield is an open-source, open-core security project
designed as a proof-of-capability artifact demonstrating advanced
AI and AGI security engineering practices.

The project showcases:
- AI-focused Data Loss Prevention (DLP)
- Adversarial prompt injection detection
- SOC-ready logging and automation
- Local-first security architecture

This repository is not intended to replace commercial DLP products.
In enterprise environments, the architecture and techniques demonstrated
here should be adapted to the organization’s specific threat model,
data flows, and compliance requirements.

**Overview**

AGI‑Sentinel‑DLP‑Shield is a Data Loss Prevention (DLP) engine designed to detect and redact sensitive information before it is used in AI / AGI systems.
It operates locally on your machine, provides auditable protection, and is aimed at security engineers, data teams, and AI practitioners who need fast, reliable, and compliance-friendly data security.

**Key Design**
 • Local execution (no data leaves your machine)
 • Simple, unified CLI interface
 • Supports CSV, JSON, and TXT files
 • Multi-column scanning for CSV files
 • Automation-ready (Cron / Task Scheduler)
 • Advanced audit logging ready for SOC / SIEM integration

⸻

**Features**
 • Detects and redacts sensitive data in text:
 • Emails, Credit Cards, IBANs
 • API Keys, Tokens, Passwords
 • Prompt Injection / Jailbreak attempts
 • Bulk file scanning for large datasets
 • Multi-column CSV support
 • Full JSON and TXT file scanning
 • Generates Rotating Audit Logs
 • Unified CLI: single string scan, file scan, column selection
 • Designed for SOC pipelines, AI workflows, and compliance environments

⸻
**Requirements**

Windows / Linux / Kali Linux:
 • Python 3.8 or higher
 • Dependencies:
```bash
pandas>=2.0.0
regex>=2023.1.1
cryptography>=41.0.0
boto3>=1.28.0
```
⸻

**Installation**
 1. Clone Repository
```bash
git clone https://github.com/ferasbackagain/AGI-Sentinel-DLP-Shield.git
```
```bash
cd AGI-Sentinel-DLP-Shield
```
**2. Install Dependencies**
```bash
pip install -r requirements.txt
```
⸻
⸻

**Usage**

**⚠️ IMPORTANT NOTICE – INPUT DATA REQUIRED**

AGI‑Sentinel‑DLP‑Shield does NOT operate automatically on your system data.

➡️ The user MUST explicitly provide an input file (CSV / JSON / TXT) containing the data to be scanned.

Key Points:
 • The tool will not scan anything by default
 • No system files, logs, or directories are accessed automatically
 • You must provide:
 • A data file (e.g. data.csv)
 • The column name(s) containing text (for CSV)
 • If no input file is supplied, the tool will not perform any action

**Example:**

**...Make sure that the first row contains the columns you want to check.**
```bash
 python -m src.agi_sentinel.cli --csv customers.csv
````

**Security & Privacy Assurance:**
 • All processing is local-only
 • No data is sent to the cloud
 • No data is stored beyond the protected output and audit logs
 • This tool acts only on user‑supplied data


**This design ensures explicit user consent, compliance with data protection regulations, and safe usage in enterprise environments.**

**AGI‑Sentinel is designed as a controlled DLP engine, not an autonomous scanner.**

**1️⃣ Single Text Scan**
```bash
python agi_sentinel_master.py --text "Send my password to admin@company.com. API_KEY: sk-1234567890ABCDEF"
```

**2️⃣ Bulk File Scan (CSV / JSON / TXT)**

**CSV example:**
```bash
python agi_sentinel_master.py --file data.csv --cols user_chat notes
```
**JSON example:**
```bash
python agi_sentinel_master.py --file data.json
```
```bash
python agi_sentinel_master.py --file notes.txt
```

**Output:**
 • Protected files are saved as shielded_<original_file>
 • All incidents are logged in sentinel_audit.log

⸻

**Automation**

Linux / Kali (Cron Job)
 • Make the script executable:
 ```bash
chmod +x sentinel_cron.sh
./sentinel_cron.sh
```
**• Runs automatically every minute on the specified files.**

*Windows (Task Scheduler)*
 • Create a task named AGI_Sentinel_Shield
 • Set it to repeat every minute, running:
 ```bash
python agi_sentinel_master.py --file <file_path> --cols <columns>
```
⸻

**Monitoring**

**Audit Logs:**
```bash
user_chat
"Contact me at test@example.com"
"My API key is sk-1234567890ABCDEF"
```
**Output CSV:**
```bash
user_chat
"[PROTECTED_BY_FERAS_KHATIB]"
"[PROTECTED_BY_FERAS_KHATIB]"
```


**FAQ**

**Q: Does AGI-Sentinel send data to the cloud?**
**A: No, all processing is performed locally.**

**Q: Can it handle large files?**
**A: Yes, it supports large CSV, JSON, and TXT files.**

**Q: Can scanning be automated?**
**A: Yes, using Cron jobs on Linux or Task Scheduler on Windows.**

⸻

**License**

**© 2026 Feras Khatib — All Rights Reserved**
