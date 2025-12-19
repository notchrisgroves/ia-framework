# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do NOT** open a public GitHub issue
2. Email the maintainer directly or use GitHub's private vulnerability reporting
3. Include: description, reproduction steps, potential impact

## Security Best Practices

### Credential Handling
- Never commit `.env` files
- All credentials load from environment variables
- Pre-commit hooks block credential commits

### File Security
- `sessions/`, `plans/`, `output/` are gitignored
- Personal content stays in your local instance

## Acknowledgments

We appreciate responsible disclosure of security issues.
