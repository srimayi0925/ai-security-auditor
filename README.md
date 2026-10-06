# 🔐 AI Security Auditor

AI Security Auditor is a web-based cybersecurity tool that performs a basic security configuration audit of websites.

The tool checks HTTPS and important security headers, calculates a security score, identifies the risk level, and uses Gemini AI to explain the findings and recommend security improvements.

## 🚀 Features

- 🌐 Website URL security audit
- 🔒 HTTPS detection
- 🛡️ Security header analysis
- 📊 Weighted security score
- 🟢🟠🔴 Risk level identification
- 🤖 Gemini AI-powered security analysis
- 📋 Audit summary
- 📥 Downloadable security audit report
- ⚠️ Error handling for invalid or unreachable websites

## 🔍 Security Checks

The auditor checks for important security configurations such as:

- Strict-Transport-Security (HSTS)
- Content-Security-Policy (CSP)
- X-Content-Type-Options
- X-Frame-Options / Clickjacking Protection
- Referrer-Policy
- Permissions-Policy
- HTTPS

## 📈 Security Score

The application calculates a weighted security score out of 100 based on the security configurations found.

### Risk Levels

| Score | Risk Level |
|------:|------------|
| 85–100 | 🟢 Low |
| 60–84 | 🟠 Medium |
| 0–59 | 🔴 High |

> A low score does not automatically mean that a website is hacked or compromised. The tool performs a basic security configuration audit.

## 🤖 AI Security Analysis

After the security audit, Gemini AI analyzes the findings and provides:

1. Risk Level
2. Security Findings
3. Why the findings matter
4. Recommended fixes
5. Overall security assessment

The AI is used to explain technical security findings in an easier-to-understand way.

## 🛠️ Technologies Used

- **Python**
- **Streamlit** – Web application interface
- **Requests** – Website HTTP requests
- **Google Gemini API** – AI-powered security analysis
- **python-dotenv** – Environment variable management

## 📁 Project Structure

```text
AI-Security-Auditor/
│
├── app.py
├── auditor.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env
