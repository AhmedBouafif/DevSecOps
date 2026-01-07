# Security Configuration for ConsumeSafe Application

## Security Hardening Measures Implemented

### 1. Application Security

#### Rate Limiting
- Implemented Flask-Limiter to prevent DDoS attacks
- Global limits: 200 requests per day, 50 per hour
- Endpoint-specific limit: 10 requests per minute for product checking

#### Security Headers (Flask-Talisman)
- HTTPS enforcement (configurable)
- Strict Transport Security (HSTS)
- Content Security Policy (CSP)
- X-Frame-Options
- X-Content-Type-Options
- X-XSS-Protection

#### Input Validation
- Product name validation and sanitization
- JSON schema validation for API requests
- SQL injection prevention (no database in current version)

### 2. Docker Security

#### Non-Root User
- Application runs as non-root user (appuser:appuser)
- UID/GID: 1000

#### Minimal Base Image
- Using python:3.11-slim for smaller attack surface
- Only necessary packages installed

#### Read-Only Filesystem
- Container filesystem configured with minimal write permissions

#### Health Checks
- Docker health check monitors application availability
- Automatic container restart on failure

### 3. Kubernetes Security

#### Pod Security Context
- `runAsNonRoot: true`
- `allowPrivilegeEscalation: false`
- Dropped all Linux capabilities
- User ID: 1000

#### Network Policies
- Ingress: Only allow traffic on port 5000
- Egress: Restricted to DNS only
- Pod-to-pod communication controlled

#### Resource Limits
- Memory requests: 128Mi, limits: 256Mi
- CPU requests: 100m, limits: 500m
- Prevents resource exhaustion attacks

#### Probes
- Liveness probe: Ensures container is running
- Readiness probe: Traffic only routed to ready pods

### 4. CI/CD Security

#### Security Scanning Tools

**Bandit** - Python security linter
- Scans code for common security issues
- Checks for hardcoded passwords, SQL injection, etc.

**Safety** - Dependency vulnerability checker
- Checks requirements.txt for known vulnerabilities
- Updates vulnerable packages

**Trivy** - Container image scanner
- Scans Docker images for vulnerabilities
- Checks OS packages and application dependencies
- SARIF format for GitHub integration

#### Automated Checks
- Security scans run on every push
- Vulnerability reports uploaded as artifacts
- Blocks deployment if critical issues found (configurable)

### 5. Additional Security Best Practices

#### Environment Variables
- Sensitive data stored in environment variables
- .env file gitignored
- Kubernetes secrets for production

#### Logging
- Application errors logged without exposing sensitive data
- Failed requests tracked for monitoring

#### CORS Configuration
- Can be configured for specific origins
- Not wide-open by default

#### Dependencies
- Pinned versions in requirements.txt
- Regular security updates recommended

## Security Checklist for Production

- [ ] Enable HTTPS enforcement in Flask-Talisman
- [ ] Configure proper CORS origins
- [ ] Set up Kubernetes secrets for sensitive data
- [ ] Configure TLS certificates for LoadBalancer
- [ ] Enable audit logging in Kubernetes
- [ ] Set up monitoring and alerting (Prometheus/Grafana)
- [ ] Implement backup and disaster recovery
- [ ] Regular security audits and penetration testing
- [ ] Keep dependencies updated
- [ ] Use secrets management (HashiCorp Vault, AWS Secrets Manager)
- [ ] Implement Web Application Firewall (WAF)
- [ ] Enable pod security policies/admission controllers
- [ ] Configure network segmentation
- [ ] Implement intrusion detection system (IDS)

## Compliance Notes

This application implements security measures aligned with:
- OWASP Top 10
- CIS Kubernetes Benchmark
- Docker CIS Benchmark
- NIST Cybersecurity Framework

## Vulnerability Disclosure

If you discover a security vulnerability, please email: security@example.com
