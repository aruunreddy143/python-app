# AWS ECR Setup Guide

## Overview

This repository includes GitHub Actions workflows for building and pushing Docker images to Amazon ECR (Elastic Container Registry).

## Prerequisites

1. **AWS Account** with ECR access
2. **GitHub Repository** with repository access
3. **IAM Role** configured for GitHub OIDC

## Step-by-Step Setup

### 1. Create an ECR Repository

```bash
aws ecr create-repository \
    --repository-name python-app \
    --region us-east-1 \
    --image-scan-on-push \
    --encryption-configuration encryptionType=AES
```

### 2. Configure GitHub OIDC Provider (if not already done)

```bash
aws iam create-open-id-connect-provider \
    --url https://token.actions.githubusercontent.com \
    --client-id-list sts.amazonaws.com \
    --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1
```

### 3. Create IAM Role for GitHub Actions

Create a file named `trust-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::YOUR_ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:aruunreddy143/python-app:ref:refs/heads/main"
        }
      }
    }
  ]
}
```

Create the role:

```bash
aws iam create-role \
    --role-name github-actions-ecr-role \
    --assume-role-policy-document file://trust-policy.json
```

### 4. Attach ECR Permissions Policy

Create a file named `ecr-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchGetImage",
        "ecr:GetDownloadUrlForLayer",
        "ecr:DescribeImages",
        "ecr:DescribeRepositories",
        "ecr:ListImages"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload",
        "ecr:PutImage",
        "ecr:StartImageScan"
      ],
      "Resource": "arn:aws:ecr:us-east-1:YOUR_ACCOUNT_ID:repository/python-app"
    }
  ]
}
```

Attach the policy:

```bash
aws iam put-role-policy \
    --role-name github-actions-ecr-role \
    --policy-name ecr-push-policy \
    --policy-document file://ecr-policy.json
```

### 5. Add Repository Secret to GitHub

1. Go to your GitHub repository settings
2. Navigate to **Secrets and variables** → **Actions**
3. Create a new repository secret:
   - **Name**: `AWS_ROLE_TO_ASSUME`
   - **Value**: `arn:aws:iam::YOUR_ACCOUNT_ID:role/github-actions-ecr-role`

## Workflows Included

### 1. `build-and-push-ecr.yml`
- Triggers on: push to main/develop, pull requests, manual trigger
- Builds Docker image
- Pushes to ECR with git SHA tag and latest tag
- Uses AWS OIDC for authentication

### 2. `ecr-scan.yml`
- Triggers on: push to main, daily schedule (2 AM UTC), manual trigger
- Scans ECR image for vulnerabilities
- Provides scan results

## Environment Variables

Update the following in the workflow files if needed:

```yaml
AWS_REGION: us-east-1        # Your AWS region
ECR_REPOSITORY: python-app   # Your ECR repository name
```

## Manual Build and Push (Local)

```bash
# Authenticate with ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build image
docker build -t YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/python-app:latest .

# Push to ECR
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/python-app:latest
```

## Troubleshooting

### Authentication Issues
- Verify AWS credentials are properly configured
- Check IAM role trust policy includes GitHub repository
- Ensure `AWS_ROLE_TO_ASSUME` secret is set correctly

### Image Build Failures
- Check Dockerfile syntax
- Verify all dependencies are available
- Check Docker build logs for errors

### ECR Scan Issues
- Ensure image was successfully pushed before scanning
- Check ECR repository exists and is accessible
- Verify IAM permissions include `ecr:StartImageScan`

## Security Considerations

1. **Role Restriction**: Limit role assumption to specific repository/branch
2. **Repository Scanning**: Enable image scan on push in ECR settings
3. **Lifecycle Policy**: Set image retention policies in ECR
4. **Vulnerability Alerts**: Configure ECR to send SNS notifications

## References

- [AWS ECR Documentation](https://docs.aws.amazon.com/ecr/)
- [GitHub Actions AWS Documentation](https://github.com/aws-actions)
- [OIDC in GitHub Actions](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
