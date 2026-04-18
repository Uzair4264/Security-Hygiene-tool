# Security Hygiene Automation Platform — CLAUDE.md

## Project Overview

A cloud-native security scanning platform built as a portfolio/resume project by Uzair Ali. It performs passive HTTP header, TLS/SSL, and misconfiguration checks against a target URL, calculates a security hygiene score, and displays results in a dashboard.

**Resume claims to verify:** FastAPI (note: actual implementation uses raw Lambda handlers, not FastAPI), AWS Lambda + API Gateway, DynamoDB, OWASP ZAP (mocked), Nuclei (mocked), Semgrep (mocked), GitHub Actions CI/CD.

---

## Project Structure

```
draft/
├── backend/              # Python serverless backend (FULLY WORKING)
├── frontend/             # Next.js frontend (needs integration fixes)
├── .github/workflows/    # CI (ci.yml) and CD (deploy.yml)
├── .gitignore
├── README.md
└── CLAUDE.md             # This file
```

---

## Backend (COMPLETE — do not change architecture)

### How to Run Locally
```bash
cd backend
# Install deps (first time only)
pip install -r requirements.txt -r requirements-dev.txt

# Start local server
python local_server.py    # Runs on http://localhost:5000

# Run tests
python -m pytest tests/ -v
```

### API Endpoints — Exact Shapes

All endpoints return `{ "success": bool, "data": {...} }` on success or `{ "success": false, "error": { "message": "...", "code": "..." } }` on error.

#### `GET /health`
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

#### `POST /scan/start`
Request body:
```json
{
  "target": "https://example.com",       // required, must be http/https, no private IPs
  "scan_type": "quick",                  // "quick" | "full"
  "environment": "staging",             // optional: "dev" | "staging" | "production"
  "github_repo": "https://github.com/owner/repo"  // optional, must be full GitHub URL
}
```
Response (202):
```json
{
  "success": true,
  "data": {
    "scan_id": "537a063b-...",
    "status": "PENDING",
    "message": "Scan initiated successfully"
  }
}
```
Error codes: `INVALID_URL`, `INVALID_REPO`, `VALIDATION_ERROR`

#### `GET /scan/{scan_id}/status`
Response:
```json
{
  "success": true,
  "data": {
    "scan_id": "...",
    "status": "COMPLETED",         // PENDING | RUNNING | COMPLETED | FAILED
    "target": "https://example.com",
    "scan_type": "quick",
    "created_at": "2026-04-18T17:54:26.084393",
    "started_at": "...",
    "completed_at": "...",
    "score": { "value": 47, "grade": "F" }  // only present when COMPLETED
  }
}
```
Error codes: `SCAN_NOT_FOUND`

#### `GET /scan/{scan_id}/result`
Response (only works when status is COMPLETED):
```json
{
  "success": true,
  "data": {
    "scan_id": "...",
    "user_id": "...",
    "target": "https://example.com",
    "scan_type": "quick",
    "environment": null,
    "status": "COMPLETED",
    "created_at": "...",
    "started_at": "...",
    "completed_at": "...",
    "score": {
      "score": 47,
      "grade": "F",
      "summary": "Critical security vulnerabilities",
      "total_issues": 8,
      "critical_count": 0,
      "high_count": 2,
      "medium_count": 2,
      "low_count": 3,
      "breakdown": { "headers": -53, "tls": 0 }
    },
    "tool_results": [
      {
        "tool": "headers",
        "category": "headers",
        "severity": { "critical": 0, "high": 2, "medium": 2, "low": 3, "info": 1 },
        "issues": [
          {
            "name": "Missing Strict-Transport-Security header",
            "description": "...",
            "severity": "high",
            "category": "headers",
            "cwe": null,
            "owasp": "A05:2021 – Security Misconfiguration",
            "recommendation": "Add: Strict-Transport-Security: max-age=31536000; includeSubDomains",
            "evidence": "Header 'Strict-Transport-Security' not found in response"
          }
        ],
        "execution_time": 0.77,
        "status": "success",
        "error": null
      }
    ],
    "recommendations": [
      {
        "priority": "HIGH",
        "title": "Fix High Severity Vulnerabilities",
        "description": "Identified 2 high severity issues.",
        "action": "Plan remediation for high severity issues within the next sprint"
      }
    ]
  }
}
```
Error codes: `SCAN_NOT_FOUND`, `SCAN_NOT_COMPLETED`

### Key Backend Files
- [backend/serverless.yml](backend/serverless.yml) — AWS Lambda + API Gateway IaC (Serverless Framework v3)
- [backend/src/api/api_health.py](backend/src/api/api_health.py) — health handler
- [backend/src/api/scan/start_scan.py](backend/src/api/scan/start_scan.py) — scan initiation handler
- [backend/src/api/scan/get_status.py](backend/src/api/scan/get_status.py) — status handler
- [backend/src/api/scan/get_result.py](backend/src/api/scan/get_result.py) — results handler
- [backend/src/core/core_orchestrator.py](backend/src/core/core_orchestrator.py) — scan workflow engine
- [backend/src/core/core_scoring.py](backend/src/core/core_scoring.py) — scoring: CRITICAL=-25, HIGH=-15, MEDIUM=-7, LOW=-3, INFO=0
- [backend/tests/](backend/tests/) — 55 passing pytest tests
- [backend/local_server.py](backend/local_server.py) — Flask dev server simulating Lambda on port 5000

### Deployment
```bash
# Set secrets in GitHub repo Settings > Secrets > Actions:
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, JWT_SECRET

# Manual deploy:
cd backend
export JWT_SECRET=$(python -c "import secrets; print(secrets.token_hex(32))")
npx serverless deploy --stage dev --region us-east-1
```
Deploys 6 Lambda functions + API Gateway + DynamoDB (PAY_PER_REQUEST) to AWS Free Tier.

---

## Frontend (Next.js — needs fixes)

### Tech Stack
- **Next.js 16** with App Router (`app/` directory)
- **TypeScript**
- **Tailwind CSS v4**
- **shadcn/ui** (Radix UI components, configured at `frontend/components.json`)
- **Recharts** for charts
- **lucide-react** for icons

### How to Run Locally
```bash
cd frontend
npm install    # or pnpm install
npm run dev    # Runs on http://localhost:3000
```
Frontend `.env` already points to `http://localhost:5000` (the backend local server).

### Pages (App Router)
| Route | File | Purpose |
|-------|------|---------|
| `/` | `app/page.tsx` | Landing / home |
| `/scan` | `app/scan/page.tsx` | Submit URL, start scan, poll progress |
| `/dashboard` | `app/dashboard/page.tsx` | Show scan results, charts, score |
| `/findings` | `app/findings/page.tsx` | Detailed issue list |
| `/history` | `app/history/page.tsx` | Past scan history |
| `/health` | `app/health/page.tsx` | Backend health check |
| `/settings` | `app/settings/page.tsx` | App settings |
| `/reports` | `app/reports/page.tsx` | Reports page |
| `/cicd` | `app/cicd/page.tsx` | CI/CD integration info |
| `/test-connection` | `app/test-connection/page.tsx` | API connection test |

### API Client (already wired up)
- [frontend/lib/api.ts](frontend/lib/api.ts) — `ZentrionAPI` class, singleton `api` exported
  - `api.healthCheck()` → GET /health
  - `api.startScan(request)` → POST /scan/start
  - `api.getScanStatus(scanId)` → GET /scan/{id}/status
  - `api.getScanResult(scanId)` → GET /scan/{id}/result
  - `api.pollScanStatus(scanId, intervalMs, maxAttempts, onProgress)` — polling helper
  - `api.startAndTrackScan(request, onProgress)` — start + poll + result in one call

- [frontend/lib/types.ts](frontend/lib/types.ts) — TypeScript types that match backend exactly
  - `ScanRequest`, `ScanStartResponse`, `ScanStatusResponse`, `ScanResultResponse`
  - `ToolResult`, `Issue`, `SecurityScore`, `Recommendation`, `HealthResponse`

### Known Frontend Bugs to Fix
1. **`/scan` page — environment values mismatch**: `<SelectItem value="development">` but backend only accepts `"dev"` | `"staging"` | `"production"`. Change `"development"` → `"dev"`.

2. **`/scan` page — github_repo default value**: Default state is `"acme-corp/web-application"` (not a full URL). Backend expects `"https://github.com/owner/repo"` or empty. Either change the default or update the placeholder to show full URL format.

3. **`/scan` page — scan complete card**: Hardcoded `"Found 12 issues across 4 severity levels"` — should use the actual result data.

4. **`/dashboard` page — no `scan_id` state**: If you visit `/dashboard` directly without `?scan_id=...`, it shows an infinite loading spinner. Needs an empty state / redirect to `/scan`.

5. **Remaining pages may have placeholder/static data** — `/findings`, `/history`, `/reports` likely have hardcoded mock data and need to be wired to the API.

### Component Library
Components are in `frontend/components/ui/` (shadcn/ui). Already installed:
`Button`, `Card`, `Input`, `Label`, `Badge`, `Select`, `RadioGroup`, `Progress`, `Dialog`, `Table`, `Tabs`, `Tooltip`, `Toast`, etc.

---

## Auth Notes
- **Local dev**: `ALLOW_ANONYMOUS=true` is set in `local_server.py` — NO token required for any endpoint.
- **Production (Lambda)**: JWT Bearer token required. The Lambda authorizer (`auth_authorizer.py`) validates tokens and passes `user_id` to handlers via `requestContext.authorizer.user_id`.
- The frontend does not currently send auth tokens. For a portfolio project with `ALLOW_ANONYMOUS=false` on prod, you would need to add token generation/storage. For now, `ALLOW_ANONYMOUS=true` works fine.

---

## CI/CD Wiring
- [.github/workflows/ci.yml](.github/workflows/ci.yml) — runs on every push: pytest + Semgrep SAST
- [.github/workflows/deploy.yml](.github/workflows/deploy.yml) — runs on push to `main`: `npx serverless deploy`
- Required GitHub Secrets: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `JWT_SECRET`
- Optional: `SEMGREP_APP_TOKEN` (Semgrep runs `continue-on-error: true` without it)

---

## Scoring Logic (for frontend display)
| Grade | Score Range | Severity Weights |
|-------|------------|-----------------|
| A | 90–100 | CRITICAL: -25 per issue |
| B | 80–89 | HIGH: -15 per issue |
| C | 70–79 | MEDIUM: -7 per issue |
| D | 60–69 | LOW: -3 per issue |
| F | 0–59 | INFO: 0 (no penalty) |

Score starts at 100, deductions applied, clamped to 0 minimum.

---

## Environment Variables

### Backend (`backend/.env` for local, Lambda env set by serverless.yml)
```
LOCAL_MODE=true           # use in-memory DB, skip Lambda invocation
ALLOW_ANONYMOUS=true      # skip JWT auth (local dev only)
JWT_SECRET=...            # required in production
STAGE=dev
DYNAMODB_TABLE=zentrion-backend-dev-scans
AWS_REGION=us-east-1
```

### Frontend (`frontend/.env`)
```
NEXT_PUBLIC_API_URL=http://localhost:5000   # backend URL
NEXT_PUBLIC_ENV=local
NEXT_PUBLIC_API_TIMEOUT=30000
```
For production, change `NEXT_PUBLIC_API_URL` to the API Gateway URL from `serverless deploy` output.
