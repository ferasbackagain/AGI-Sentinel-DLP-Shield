🛡️ AGI Sentinel DLP Shield v2.1.0

Advanced AI Security Protection System - Created by [Your Name Here]

https://img.shields.io/badge/License-AGPLv3-blue.svg
https://img.shields.io/badge/python-3.8+-green.svg
https://img.shields.io/badge/version-2.1.0-orange.svg
https://img.shields.io/badge/security-enterprise-red.svg
https://img.shields.io/badge/author-Your%20Name-purple.svg

👨‍💻 About the Author

[Your Full Name] - [Your Role/Title] with expertise in:

· Artificial Intelligence Security
· Data Loss Prevention (DLP) Systems
· Cybersecurity and Threat Intelligence
· Machine Learning Model Protection
· Enterprise Security Architecture

Contact Information:

· 📧 Email: your.email@example.com
· 🐙 GitHub: @yourusername
· 💼 LinkedIn: Your Name
· 🐦 Twitter: @yourhandle
· 🌐 Website: yourwebsite.com

---

📖 Table of Contents

· ✨ Features
· 🚀 Quick Start
· 📦 Installation
· 🎯 Usage Guide
· 🔧 Available Commands
· 📊 Examples
· 🛡️ Protection Types
· ⚡ Performance
· 📁 Project Structure
· 🐳 Docker Support
· 🤝 Contributing
· 📜 License
· 👨‍💻 Author Information

---

✨ Features

🔐 Core Security Features

· PII Detection & Redaction: Emails, Credit Cards, Phone Numbers, SSN, Passport
· API Key Protection: OpenAI, AWS, Google, GitHub, Slack, SendGrid tokens
· AI-Specific Defense: Prompt injection, jailbreak, DAN mode, adversarial attacks
· Secret Detection: JWT tokens, Base64/Hex encoded secrets
· Financial Data Protection: IBAN numbers, Bank Account details

⚡ Technical Capabilities

· Parallel Processing: Multi-threading with configurable workers
· Bulk File Support: CSV, JSON with intelligent column scanning
· Secure Logging: JSON audit logs with zero PII storage
· Custom Rules: Extensible regex-based rule system
· Production Ready: Docker, Cron jobs, Cloud integration

📊 Enterprise Features

· Comprehensive Reporting: Detailed statistics and analytics
· High Performance: 5000+ characters/second throughput
· Scalable Architecture: Handles large datasets efficiently
· Open Source: AGPLv3 licensed, community-driven development

---

🚀 Quick Start

Installation in 60 Seconds
# Method 1: From PyPI (Recommended)
pip install agi-sentinel-dlp-shield

# Method 2: From Source
git clone https://github.com/yourusername/AGI-Sentinel-DLP-Shield.git
cd AGI-Sentinel-DLP-Shield
pip install -e .

# Method 3: Using Docker
docker pull yourusername/agi-sentinel:latest

Your First Scan
# Quick test
agi-sentinel --text "My email is test@example.com and card is 4111111111111111"

# With verbose output
agi-sentinel --text "test@example.com" --verbose

# Export results
agi-sentinel --text "test@example.com" --export results.json

---

📦 Installation

System Requirements

· Operating System: Linux, macOS, Windows (WSL2 recommended)
· Python: 3.8 or higher
· Memory: 2GB minimum (4GB recommended for large files)
· Storage: 100MB free space

Detailed Installation Steps

Option 1: Standard Installation
# 1. Clone repository
git clone https://github.com/yourusername/AGI-Sentinel-DLP-Shield.git
cd AGI-Sentinel-DLP-Shield

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install as package
pip install -e .

# 5. Verify installation
agi-sentinel --version

Option 2: Docker Installation
# Build from Dockerfile
docker build -t agi-sentinel .

# Run container
docker run -v $(pwd)/data:/app/data agi-sentinel --text "test@example.com"

# Use pre-built image
docker run -v $(pwd):/data ghcr.io/yourusername/agi-sentinel:latest

Option 3: Production Deployment
# Install as system service (Linux)
sudo ./scripts/install_as_service.sh

# Schedule automated scans (Cron)
echo "0 */2 * * * /opt/agi_sentinel/scripts/production_runner.sh" | sudo crontab -

# Configure as API service
cd api_server
pip install -r requirements.txt
python app.py

---

🎯 Usage Guide

Command Structure
agi-sentinel [MODE] [INPUT] [OPTIONS]

Modes:
  --text        Scan single text
  --csv         Scan CSV file
  --json-file   Scan JSON file











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
