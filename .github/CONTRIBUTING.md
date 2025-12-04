# Contributing to python-app

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/aruunreddy143/python-app.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Commit your changes: `git commit -am 'Add feature description'`
6. Push to the branch: `git push origin feature/your-feature-name`
7. Submit a pull request

## Development Setup

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- Git

### Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run with Docker Compose:
   ```bash
   docker-compose up
   ```

3. Access the application at `http://localhost:8000`
4. API documentation available at `http://localhost:8000/docs`

## Code Standards

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## AWS ECR Setup

### Repository Secrets Required

Add the following GitHub secrets for ECR integration:
- `AWS_ROLE_TO_ASSUME`: Your AWS IAM role ARN for OIDC

### Example IAM Role Policy

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
          "token.actions.githubusercontent.com:sub": "repo:aruunreddy143/python-app:*"
        }
      }
    }
  ]
}
```

## Pull Request Process

1. Update the README.md with details of changes to the interface
2. Increase version numbers in any example files following SemVer
3. Ensure the build passes all checks
4. Request review from maintainers
5. Once approved, maintainer will merge your PR

## Issues

- Use GitHub Issues for bug reports and feature requests
- Provide clear descriptions and reproduction steps for bugs
- Include relevant logs and error messages

## Questions?

Feel free to open a discussion or issue if you have questions!
