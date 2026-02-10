# Security Audit Template

Perform a comprehensive security audit of the provided code following OWASP Top 10 and secure coding standards.

## Audit Scope

Analyze for these vulnerability categories:

### 1. Injection Flaws
- SQL injection via concatenated queries
- NoSQL injection in MongoDB queries
- Command injection in shell executions
- LDAP injection
- XPath injection

### 2. Broken Authentication
- Weak password requirements
- Insecure password storage (plaintext, MD5, SHA1)
- Missing rate limiting on login
- Predictable session IDs
- Session fixation vulnerabilities

### 3. Sensitive Data Exposure
- Hardcoded secrets, keys, passwords
- Unencrypted sensitive data in transit or at rest
- Verbose error messages exposing system details
- Missing HTTPS enforcement
- Logging sensitive information

### 4. XML External Entities (XXE)
- Unsafe XML parsing configurations
- External entity expansion attacks

### 5. Broken Access Control
- Missing authorization checks
- IDOR (Insecure Direct Object Reference)
- Privilege escalation opportunities
- CORS misconfiguration

### 6. Security Misconfiguration
- Default credentials
- Unnecessary features enabled
- Outdated components
- Missing security headers
- Verbose error pages

### 7. Cross-Site Scripting (XSS)
- Unescaped user input in HTML
- DOM-based XSS
- Stored XSS in database
- Missing Content-Security-Policy

### 8. Insecure Deserialization
- Unsafe object deserialization
- Pickle/Marshal usage with untrusted data

### 9. Using Components with Known Vulnerabilities
- Outdated dependencies
- Unpatched security issues
- Risky transitive dependencies

### 10. Insufficient Logging & Monitoring
- Missing audit trails
- Inadequate error logging
- No alerting on suspicious activity

## Additional Checks

**API Security**:
- Missing authentication/authorization
- No rate limiting
- CORS wildcards
- Insufficient input validation

**Cryptography**:
- Weak algorithms (MD5, SHA1 for passwords)
- Insecure random number generation
- Improper key management

**Business Logic**:
- Race conditions
- Integer overflow/underflow
- Logic flaws enabling fraud

## Output Format

For each vulnerability:

**🚨 [SEVERITY] - [VULNERABILITY TYPE]**
**Location**: `File:Line`
**Issue**: [Description of vulnerability]
**Attack Scenario**: [How an attacker could exploit this]
**Impact**: [Confidentiality/Integrity/Availability impact]
**Remediation**: [Specific fix with code example]
**References**: [OWASP/CWE links if applicable]

Severity: 🚨 Critical | ⚠️ High | ⚡ Medium | ℹ️ Low

## Final Summary

**Total Vulnerabilities**: X
**Risk Assessment**: [Critical/High/Medium/Low]
**Top Priority Fixes**: [List 3 most critical issues]
**Compliance Impact**: [GDPR, PCI-DSS, HIPAA implications if relevant]

---

**Context References**:
- @.cursor/rules/security.mdc
- @.cursor/rules/guardrails.mdc
- Project security documentation
