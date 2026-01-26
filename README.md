# Security Hygiene Automation Platform

This project is a cloud-native security hygiene automation platform that performs safe, passive security checks against web applications and presents the results in a centralized dashboard.

The goal of this project is to demonstrate real-world AppSec and DevSecOps workflows using industry tools and a realistic cloud architecture.

---

## What This Project Does

* Performs automated security hygiene scans
* Runs passive DAST, SAST, and misconfiguration checks
* Normalizes findings and calculates a security score
* Stores scan history and results
* Supports CI/CD security enforcement
* Designed for AWS deployment

No active exploitation or intrusive attacks are performed.

---

## Tech Stack

### Frontend

* React or Next.js
* Tailwind CSS
* Hosted on AWS S3 with CloudFront

### Backend

* Python
* FastAPI

### Security Tools

* Custom Python logic for HTTP security headers
* Python SSL and OpenSSL for TLS checks
* OWASP ZAP passive scan via REST API
* Nuclei for misconfiguration scanning via CLI
* Semgrep for SAST via CLI

### Database

* AWS DynamoDB

### Cloud

* AWS S3
* AWS CloudFront
* AWS API Gateway
* AWS Lambda
* AWS ECS or EC2 for OWASP ZAP

---

## High-Level Architecture

User interacts with the frontend application.
The frontend communicates with a FastAPI backend.
The backend orchestrates multiple security tools.
Findings are normalized, scored, and stored in DynamoDB.
Results are returned to the frontend for visualization.

---

## Scan Flow

1. User submits a target URL
2. Backend validates the target
3. HTTP header checks are performed
4. TLS configuration is analyzed
5. OWASP ZAP performs a passive scan
6. Nuclei scans for known misconfigurations
7. Semgrep performs static analysis where applicable
8. Findings are normalized and scored
9. Results are stored in DynamoDB
10. Dashboard displays scan results

---

## Risk Scoring

Each finding impacts the overall hygiene score.

Example scoring logic:

* Critical reduces score significantly
* High reduces score moderately
* Medium and Low reduce score minimally

Final score ranges from 0 to 100 and is used to track security posture over time.

---

## CI/CD Integration

This project is designed to integrate with GitHub Actions.

Typical pipeline:

* Code linting and tests
* Semgrep SAST scan
* Frontend build
* Backend packaging
* Deployment to AWS

Optional policy enforcement can fail the pipeline if the hygiene score is below a defined threshold.

---

## Project Structure

```
frontend/
  app/
    dashboard/
    findings/
    history/
    scan/
    settings/
  components/
  lib/

backend/
  api/
  scanners/
  scoring/
  storage/
  main.py
```

---

## Ethical Use Notice

This project only performs non-intrusive and passive security checks.

Only scan systems you own or have explicit permission to test.

---

## Use Cases

* Learning AppSec and DevSecOps
* Security hygiene monitoring
* CI/CD security gates
* Final year university project
* Junior security or cloud engineer portfolio

---

## Author

Uzair Ali


