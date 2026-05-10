# Security Auditor — Patterns

### Secret detection
```bash
gitleaks detect --verbose
trufflehog git file://. --only-verified
```

### Container scan
```bash
trivy image myapp:latest --severity HIGH,CRITICAL
```

### OWASP Top 10 checklist
- [ ] A01: Broken Access Control
- [ ] A02: Cryptographic Failures
- [ ] A03: Injection (SQL, NoSQL, OS, LDAP)
- [ ] A04: Insecure Design
- [ ] A05: Security Misconfiguration
- [ ] A06: Vulnerable Components
- [ ] A07: Auth Failures
- [ ] A08: Data Integrity Failures
- [ ] A09: Logging Failures
- [ ] A10: SSRF
