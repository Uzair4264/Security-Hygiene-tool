# Zentrion Backend - Security Hygiene Cloud Platform

A production-ready, serverless backend for automated security hygiene scanning and analysis.

## 🎯 Overview

Zentrion is a cloud-native security platform that analyzes web applications and cloud assets to produce comprehensive security hygiene scores using multiple open-source security tools.

### Key Features

- **Automated Security Scanning**: Headers, TLS/SSL, OWASP ZAP, Nuclei
- **Weighted Scoring Engine**: Intelligent risk scoring with severity-based weights
- **Serverless Architecture**: Built on AWS Lambda for infinite scalability
- **RESTful API**: Clean API design with JWT authentication
- **Real-time Status**: Async job processing with status tracking
- **Production-Ready**: Structured logging, error handling, type hints

## 🏗️ Architecture

```
┌─────────────────┐
│   API Gateway   │
└────────┬────────┘
         │
         ├─────► Health Check
         ├─────► Start Scan (POST)
         ├─────► Get Status (GET)
         └─────► Get Result (GET)
                 │
                 ▼
         ┌───────────────┐
         │ Lambda Handler│
         └───────┬───────┘
                 │
                 ├─────► JWT Authorizer
                 ├─────► DynamoDB (Scans)
                 └─────► Async Lambda (Processor)
                         │
                         ▼
                 ┌───────────────┐
                 │  Orchestrator │
                 └───────┬───────┘
                         │
                         ├─────► Headers Scanner
                         ├─────► TLS Scanner
                         ├─────► ZAP Scanner
                         ├─────► Nuclei Scanner
                         │
                         ▼
                 ┌───────────────┐
                 │ Scoring Engine│
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │   DynamoDB    │
                 └───────────────┘
```

## 📁 Project Structure

```
backend/
├── src/
│   ├── api/                    # API Gateway handlers
│   │   ├── scan/
│   │   │   ├── start_scan.py           # POST /scan/start
│   │   │   ├── get_scan_status.py      # GET /scan/{id}/status
│   │   │   └── get_scan_result.py      # GET /scan/{id}/result
│   │   └── health.py                   # Health check
│   │
│   ├── core/                   # Business logic
│   │   ├── orchestrator.py             # Scan workflow coordinator
│   │   ├── scanner_engine.py           # Scanner execution engine
│   │   └── scoring.py                  # Security scoring logic
│   │
│   ├── scanners/              # Security tool implementations
│   │   ├── headers/
│   │   │   └── headers_scan.py         # HTTP headers scanner
│   │   ├── tls/
│   │   │   └── tls_scan.py             # TLS/SSL scanner
│   │   ├── zap/
│   │   │   └── zap_scan.py             # OWASP ZAP integration
│   │   └── nuclei/
│   │       └── nuclei_scan.py          # Nuclei scanner
│   │
│   ├── db/                    # Data access layer
│   │   ├── dynamodb.py                 # DynamoDB client
│   │   └── repositories.py             # Data repositories
│   │
│   ├── models/                # Pydantic models
│   │   ├── scan_request.py             # Request models
│   │   └── scan_result.py              # Result models
│   │
│   ├── auth/                  # Authentication
│   │   ├── jwt.py                      # JWT utilities
│   │   └── authorizer.py               # Lambda authorizer
│   │
│   ├── utils/                 # Utilities
│   │   ├── logger.py                   # Structured logging
│   │   ├── validators.py               # Input validation
│   │   └── response.py                 # API responses
│   │
│   ├── config/                # Configuration
│   │   ├── settings.py                 # Environment settings
│   │   └── constants.py                # Application constants
│   │
│   └── main.py                # Local testing module
│
├── serverless.yml             # Serverless Framework config
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- AWS Account
- Serverless Framework (`npm install -g serverless`)
- AWS CLI configured

### Installation

```bash
# Clone the repository
git clone <your-repo>
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials
aws configure

# Set environment variables
export JWT_SECRET="your-jwt-secret"
export ALLOW_ANONYMOUS="false"
```

### Deployment

```bash
# Deploy to dev stage
serverless deploy --stage dev

# Deploy to production
serverless deploy --stage prod

# Deploy specific function
serverless deploy function -f startScan --stage dev
```

### Local Testing

```bash
# Run local tests
python -m src.main

# Or use serverless offline
serverless offline --stage dev
```

## 📡 API Endpoints

### Health Check

```bash
GET /health
```

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "service": "zentrion-backend",
    "version": "1.0.0",
    "stage": "dev"
  }
}
```

### Start Scan

```bash
POST /scan/start
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
  "target": "https://example.com",
  "scan_type": "quick",
  "environment": "production",
  "github_repo": "https://github.com/user/repo"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "scan_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "PENDING",
    "message": "Scan initiated successfully"
  }
}
```

### Get Scan Status

```bash
GET /scan/{scan_id}/status
Authorization: Bearer <jwt-token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "scan_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "COMPLETED",
    "target": "https://example.com",
    "scan_type": "quick",
    "created_at": "2025-01-15T10:30:00Z",
    "completed_at": "2025-01-15T10:32:45Z",
    "score": {
      "value": 72,
      "grade": "C"
    }
  }
}
```

### Get Scan Result

```bash
GET /scan/{scan_id}/result
Authorization: Bearer <jwt-token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "scan_id": "123e4567-e89b-12d3-a456-426614174000",
    "target": "https://example.com",
    "scan_type": "quick",
    "status": "COMPLETED",
    "tool_results": [
      {
        "tool": "headers",
        "category": "headers",
        "severity": {
          "critical": 0,
          "high": 2,
          "medium": 3,
          "low": 1
        },
        "issues": [...]
      }
    ],
    "score": {
      "score": 72,
      "grade": "C",
      "summary": "Moderate security issues detected",
      "total_issues": 6,
      "critical_count": 0,
      "high_count": 2
    },
    "recommendations": [...]
  }
}
```

## 🔐 Security

### Authentication

JWT-based authentication using AWS Cognito-compatible tokens:

```javascript
// Token claims expected:
{
  "sub": "user-id",           // Primary user identifier
  "cognito:username": "user", // Alternative identifier
  "exp": 1642345678           // Expiration timestamp
}
```

### Anonymous Mode

For development/testing, enable anonymous access:

```bash
export ALLOW_ANONYMOUS="true"
serverless deploy --stage dev
```

## 📊 Scoring Model

Security scores are calculated using weighted severity impacts:

| Severity | Weight | Impact |
|----------|--------|--------|
| Critical | -25    | Immediate action required |
| High     | -15    | High priority fix |
| Medium   | -7     | Should be addressed |
| Low      | -3     | Nice to fix |
| Info     | 0      | Informational only |

**Score Range:** 0-100 (starts at 100, deductions applied)

**Grading:**
- A (90-100): Excellent security posture
- B (80-89): Good security with minor issues
- C (70-79): Moderate security issues
- D (60-69): Significant concerns
- F (0-59): Critical vulnerabilities

## 🧪 Testing

```bash
# Unit tests
pytest tests/

# Integration tests
pytest tests/integration/

# Coverage report
pytest --cov=src tests/
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `STAGE` | Deployment stage | `dev` |
| `AWS_REGION` | AWS region | `us-east-1` |
| `DYNAMODB_TABLE` | DynamoDB table name | `zentrion-dev-scans` |
| `JWT_SECRET` | JWT signing secret | (required) |
| `ALLOW_ANONYMOUS` | Enable anonymous mode | `false` |
| `LOG_LEVEL` | Logging level | `INFO` |

### DynamoDB Schema

**Table:** `zentrion-{stage}-scans`

| Attribute | Type | Description |
|-----------|------|-------------|
| PK | String | `USER#{user_id}` |
| SK | String | `SCAN#{scan_id}` |
| GSI1PK | String | `STATUS#{status}` |
| GSI1SK | String | `CREATED#{timestamp}` |

## 🎓 Production Considerations

### Scaling

- Lambda concurrent execution limits
- DynamoDB provisioned capacity (if not using on-demand)
- API Gateway throttling limits

### Monitoring

```bash
# View logs
serverless logs -f startScan --tail

# CloudWatch metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=zentrion-backend-dev-startScan
```

### Security Tools Integration

Current implementations are abstractions. For production:

1. **ZAP**: Deploy ZAP in ECS Fargate containers
2. **Nuclei**: Include binary in Lambda layers or use containers
3. **Custom Scanners**: Add to `/scanners` directory

### CI/CD Pipeline

```yaml
# Example .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: serverless deploy --stage prod
```

## 🤝 Contributing

Contributions welcome! Please follow:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 🙋 Support

For issues or questions:
- Open a GitHub issue
- Contact: security@zentrion.io

---

**Built for Application Security & DevSecOps Engineers**

This backend demonstrates production-grade cloud architecture, security best practices, and professional software engineering.