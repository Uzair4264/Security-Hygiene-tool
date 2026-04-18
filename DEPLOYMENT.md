# Deployment Guide — Zentrion Security Platform

**Stack:** Python Lambda backend + Next.js frontend + DynamoDB  
**Target:** AWS Free Tier  
**Time to complete:** ~45–60 minutes (first time)

---

## AWS Services Used

| Service | What it does | Free Tier |
|---------|-------------|-----------|
| **AWS Lambda** | Runs your Python scan handlers | 1M requests + 400K GB-sec/month — **permanent** |
| **API Gateway** | HTTP API routes to Lambda | 1M calls/month — **12 months** |
| **DynamoDB** | Stores scan data | 25 GB + 25 RCU/WCU — **permanent** |
| **AWS Amplify** | Hosts Next.js frontend | 1,000 build-min + 15 GB served/month — **12 months** |
| **IAM** | Permissions for everything | Always free |
| **CloudWatch** | Lambda logs | 5 GB logs ingested/month — **permanent** |

**Estimated monthly cost: $0** for development/portfolio usage.

---

## Prerequisites

- [ ] GitHub account with this repo pushed
- [ ] AWS account (free): https://aws.amazon.com/free
- [ ] Node.js 20+ installed locally
- [ ] Python 3.11 installed locally
- [ ] AWS CLI installed: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

---

## Step 1 — Create an IAM User for Deployment

Never use your AWS root account for deployments. Create a dedicated IAM user.

### 1.1 Open IAM Console

1. Sign in to AWS Console → search **IAM** → open it
2. Left sidebar → **Users** → **Create user**
3. Username: `zentrion-deployer`
4. Click **Next**

### 1.2 Attach Permissions

Choose **Attach policies directly** and add these managed policies:

| Policy | Why needed |
|--------|-----------|
| `AWSLambda_FullAccess` | Deploy Lambda functions |
| `AmazonAPIGatewayAdministrator` | Deploy API Gateway |
| `AmazonDynamoDBFullAccess` | Create DynamoDB table |
| `AmazonS3FullAccess` | Serverless Framework uses S3 for deployment artifacts |
| `IAMFullAccess` | Serverless creates IAM roles for Lambda |
| `CloudWatchLogsFullAccess` | Lambda logging |

> **Security note:** For a production system you would scope these down. For a portfolio project this is fine.

Click **Next** → **Create user**

### 1.3 Generate Access Keys

1. Click the `zentrion-deployer` user → **Security credentials** tab
2. Scroll to **Access keys** → **Create access key**
3. Select **Command Line Interface (CLI)** → **Next** → **Create access key**
4. **Copy both values now** — you cannot see the secret again:
   - Access key ID: `AKIA...`
   - Secret access key: `wJalrXUtn...`

---

## Step 2 — Configure AWS CLI Locally

```bash
aws configure
```

Enter when prompted:
```
AWS Access Key ID: AKIA...              (from Step 1.3)
AWS Secret Access Key: wJalrXUtn...    (from Step 1.3)
Default region name: us-east-1
Default output format: json
```

Verify it works:
```bash
aws sts get-caller-identity
```

Expected output:
```json
{
    "UserId": "AIDA...",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/zentrion-deployer"
}
```

---

## Step 3 — Deploy the Backend

### 3.1 Generate a JWT Secret

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output — this is your `JWT_SECRET`. Example: `a3f8c2d1e4b7...`

### 3.2 Install Backend Dependencies

```bash
cd backend
npm install
pip install -r requirements.txt
```

### 3.3 Deploy with Serverless Framework

```bash
cd backend
JWT_SECRET=<your-secret-here> npx serverless deploy --stage dev --region us-east-1 --verbose
```

On Windows PowerShell:
```powershell
$env:JWT_SECRET="<your-secret-here>"
npx serverless deploy --stage dev --region us-east-1 --verbose
```

On Windows Command Prompt:
```cmd
set JWT_SECRET=<your-secret-here>
npx serverless deploy --stage dev --region us-east-1 --verbose
```

**This takes 2–5 minutes.** Serverless will:
1. Package your Python code + dependencies into a ZIP
2. Upload to S3
3. Create/update 6 Lambda functions
4. Create API Gateway with all routes
5. Create DynamoDB table `zentrion-backend-dev-scans`
6. Create IAM role for Lambda

### 3.4 Save the API URL

At the end of deployment you will see output like:

```
Service Information
service: zentrion-backend
stage: dev
region: us-east-1

endpoints:
  GET  - https://abc123xyz.execute-api.us-east-1.amazonaws.com/dev/health
  POST - https://abc123xyz.execute-api.us-east-1.amazonaws.com/dev/scan/start
  GET  - https://abc123xyz.execute-api.us-east-1.amazonaws.com/dev/scan/{scan_id}/status
  GET  - https://abc123xyz.execute-api.us-east-1.amazonaws.com/dev/scan/{scan_id}/result
```

**Copy the base URL:** `https://abc123xyz.execute-api.us-east-1.amazonaws.com/dev`

### 3.5 Verify Backend is Live

```bash
curl https://abc123xyz.execute-api.us-east-1.amazonaws.com/dev/health
```

Expected:
```json
{"success": true, "data": {"status": "healthy", "service": "zentrion-backend", "version": "1.0.0", "stage": "dev"}}
```

---

## Step 4 — Deploy the Frontend (AWS Amplify)

AWS Amplify is the easiest way to host a Next.js app on AWS. It reads from your GitHub repo and auto-deploys on every push.

### 4.1 Create the Frontend Environment File

Create `frontend/.env.production` with your real API URL:

```env
NEXT_PUBLIC_API_URL=https://abc123xyz.execute-api.us-east-1.amazonaws.com/dev
NEXT_PUBLIC_ENV=production
NEXT_PUBLIC_API_TIMEOUT=30000
```

Commit and push this file (it does not contain secrets — only a public URL):

```bash
git add frontend/.env.production
git commit -m "Add production environment config"
git push origin main
```

### 4.2 Open AWS Amplify

1. AWS Console → search **Amplify** → open it
2. Click **Create new app** (or **New app** → **Host web app**)

### 4.3 Connect GitHub

1. Select **GitHub** → **Next**
2. Click **Authorize AWS Amplify** → sign in to GitHub if prompted
3. Select your repository: `<your-username>/draft` (or whatever the repo is named)
4. Branch: `main`
5. Click **Next**

### 4.4 Configure Build Settings

Amplify may auto-detect Next.js. If not, set manually:

**App name:** `zentrion-frontend`  
**Environment:** `dev` (or `production`)

Amplify will show a build configuration. Replace it with this:

```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - cd frontend
        - npm ci
    build:
      commands:
        - cd frontend
        - npm run build
  artifacts:
    baseDirectory: frontend/.next
    files:
      - '**/*'
  cache:
    paths:
      - frontend/node_modules/**/*
      - frontend/.next/cache/**/*
```

Click **Next**

### 4.5 Add Environment Variables in Amplify

Before clicking **Save and deploy**, click **Advanced settings** and add:

| Key | Value |
|-----|-------|
| `NEXT_PUBLIC_API_URL` | `https://abc123xyz.execute-api.us-east-1.amazonaws.com/dev` |
| `NEXT_PUBLIC_ENV` | `production` |
| `NEXT_PUBLIC_API_TIMEOUT` | `30000` |

Click **Save and deploy**

### 4.6 Wait for Build

The first build takes 3–8 minutes. You can watch the logs in the Amplify console.

When complete you will see a URL like:
```
https://main.d1abc2defg.amplifyapp.com
```

Open it — your frontend is live.

---

## Step 5 — Wire Up GitHub Actions CI/CD

This makes every push to `main` automatically deploy the backend.

### 5.1 Add GitHub Secrets

Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these three secrets:

| Name | Value |
|------|-------|
| `AWS_ACCESS_KEY_ID` | `AKIA...` (from Step 1.3) |
| `AWS_SECRET_ACCESS_KEY` | `wJalrXUtn...` (from Step 1.3) |
| `JWT_SECRET` | The secret you generated in Step 3.1 |

### 5.2 Verify CI/CD Works

Push any small change to `main`:

```bash
git commit --allow-empty -m "trigger CI/CD test"
git push origin main
```

Go to GitHub → **Actions** tab. You should see two workflows running:
- **CI — Test & Lint**: runs pytest + Semgrep
- **CD — Deploy to AWS**: runs `serverless deploy`

Both should show green checkmarks within 5–10 minutes.

---

## Step 6 — Verify Full Stack End-to-End

With both backend and frontend deployed, test the golden path:

1. Open your Amplify URL
2. Navigate to `/health` — should show backend status "healthy"
3. Navigate to `/scan` — submit `https://example.com` as target
4. Watch the progress — should move through PENDING → RUNNING → COMPLETED
5. Navigate to `/dashboard?scan_id=<id>` — should show scan results with score

---

## Architecture Diagram

```
GitHub Push to main
        │
        ├─── GitHub Actions CI ──────► pytest + Semgrep (pass/fail)
        │
        └─── GitHub Actions CD ──────► Serverless Framework
                                              │
                                              ▼
                                    AWS API Gateway (HTTP API)
                                              │
                              ┌───────────────┼───────────────┐
                              ▼               ▼               ▼
                         Lambda            Lambda          Lambda
                        (health)       (start_scan)     (get_status)
                                            │
                                            ▼
                                   Lambda (processScan)
                                   [async invocation]
                                            │
                                            ▼
                                       DynamoDB
                                  (scan results table)

User Browser
        │
        └─► AWS Amplify (Next.js frontend)
                    │
                    └─► API Gateway (above)
```

---

## Tearing Down (to avoid charges)

If you want to delete everything:

```bash
# Remove backend (Lambda, API Gateway, DynamoDB table)
cd backend
npx serverless remove --stage dev --region us-east-1

# Remove S3 deployment bucket (Serverless creates one)
aws s3 ls | grep zentrion          # find the bucket name
aws s3 rb s3://BUCKET-NAME --force
```

For Amplify: AWS Console → Amplify → your app → **App settings** → **General** → **Delete app**

---

## Troubleshooting

### "Unable to import module" error in Lambda
Handler path mismatch. Check `backend/serverless.yml` — all handler paths must match actual filenames exactly. The correct paths are:
- `src/api/api_health.handler`
- `src/api/scan/start_scan.handler`
- `src/api/scan/get_status.handler`
- `src/api/scan/get_result.handler`
- `src/auth/auth_authorizer.handler`
- `src/core/core_orchestrator.handler`

### Serverless deploy fails with credentials error
```
Error: AWS provider credentials not found.
```
Run `aws configure` again and make sure the region is `us-east-1`.

### Amplify build fails
- Check that `frontend/.env.production` exists and is committed
- Check that the build spec uses `cd frontend` before each command
- Check build logs in the Amplify console for the exact error

### CORS errors in browser
API Gateway has CORS configured in `serverless.yml`. If you see CORS errors, the frontend URL must match. For Amplify, CORS is open (`*`) so this should not be an issue.

### Scan stays PENDING forever
In production (Lambda), `start_scan` asynchronously invokes `processScan` via `lambda:InvokeFunction`. If it stays PENDING, check CloudWatch logs for the `processScan` function:  
AWS Console → Lambda → `zentrion-backend-dev-processScan` → **Monitor** → **View CloudWatch logs**

---

## Cost Monitoring

Set up a billing alert so you get an email if charges exceed $1:

1. AWS Console → search **Billing** → **Budgets** → **Create budget**
2. Choose **Monthly cost budget**
3. Amount: `$1`
4. Email: your email address
5. Create

This protects against accidental usage going over free tier.
