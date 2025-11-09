# Security Policy

## 🛡️ Agiletec Inc. Security Commitment

We prioritize the security of our users and community above all else.

**Philosophy**: Transparency and responsible disclosure

---

## 🔍 Supported Versions

Versions receiving security updates:

| Project | Version | Supported |
|---------|---------|-----------|
| AIRIS MCP Gateway | 1.x.x | ✅ |
| mindbase | 0.x.x (Beta) | ✅ |
| superagent | 1.x.x | ✅ |
| neural | 0.x.x (Beta) | ✅ |
| selfhosted-supabase-mcp | 1.x.x | ✅ |
| cmd-ime | 0.x.x (Beta) | ✅ |

---

## 🚨 Reporting a Vulnerability

### How to Report

**Important**: Do not report security vulnerabilities through public issues.

**Contact**:
- 📧 **Email**: security@agiletec.net
- 🔒 **Encryption**: PGP Key available on request

**Report Contents**:
1. Detailed description of the vulnerability
2. Affected versions
3. Reproduction steps (PoC)
4. Potential impact scope
5. Proposed fix (if available)

---

### Response Process

**Timeline**:

1. **Acknowledgment** (within 24 hours)
   - Confirm receipt of report and send acknowledgment

2. **Initial Assessment** (within 3 business days)
   - Evaluate vulnerability severity (CVSS v3.1)
   - Investigate impact scope

3. **Fix Development** (based on severity)
   - Critical: within 1 week
   - High: within 2 weeks
   - Medium: within 1 month
   - Low: next release

4. **Patch Release**
   - Release security patch
   - Obtain CVE number (if necessary)

5. **Disclosure** (90 days after patch release)
   - Publish vulnerability details
   - Acknowledge reporter

---

## 🏆 Vulnerability Rewards

### Bounty Program

**Target Projects**:
- AIRIS MCP Gateway
- mindbase
- superagent
- neural
- selfhosted-supabase-mcp
- cmd-ime
- Agiletec Platform (private products)

**Bounty Amounts** (under consideration):
- **Critical**: $500 - $2,000
- **High**: $200 - $500
- **Medium**: $50 - $200
- **Low**: Acknowledgment only

**Excluded**:
- Known vulnerabilities in third-party libraries
- Social engineering attacks
- Attacks requiring physical access
- DoS/DDoS attacks

---

## 🔒 Security Best Practices

### During Development

**Secret Management**:
- ✅ Use secret managers like Infisical
- ❌ Don't commit `.env` files to Git
- ❌ Don't hardcode API keys in code

**Dependency Management**:
- Run `npm audit` or `pnpm audit` regularly
- Enable Dependabot
- Regular library updates

**Authentication & Authorization**:
- Set JWT token expiration
- Implement CSRF protection
- Introduce rate limiting

---

### During Deployment

**Infrastructure Security**:
- ✅ Enforce HTTPS/TLS
- ✅ Principle of Least Privilege
- ✅ Network isolation (Docker networks)
- ✅ Regular security patch application

**Data Protection**:
- Database encryption (at-rest, in-transit)
- Row-Level Security (RLS) for multi-tenant isolation
- Backup encryption

---

## 📊 Security Audit History

| Date | Auditor | Scope | Findings |
|------|---------|-------|----------|
| TBD | Internal | AIRIS Platform | TBD |
| TBD | External | MCP Gateway | TBD |

---

## 🔐 Compliance

### Standards

We strive to comply with the following security standards:

- **OWASP Top 10** (Web Application Security)
- **CWE Top 25** (Common Weakness Enumeration)
- **NIST Cybersecurity Framework** (Infrastructure Security)

### Data Protection

- **GDPR Compliance** (for EU customers)
- **Japan Personal Information Protection Act Compliance**
- Data minimization principle

---

## 📚 Security Resources

### Learning Materials

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Supabase Security Best Practices](https://supabase.com/docs/guides/auth)
- [Docker Security](https://docs.docker.com/engine/security/)

### Tools

- **Static Analysis**: ESLint security plugins
- **Dependency Scanning**: Snyk, npm audit
- **Secret Scanning**: git-secrets, TruffleHog
- **Container Scanning**: Trivy

---

## 🙏 Acknowledgments

We thank security researchers:

- (Researcher names - to be added after vulnerability disclosure)

---

## 📞 Contact

For general security questions:

- 📧 **Email**: security@agiletec.net
- 🐙 **GitHub Security Advisory**: Security tab of each project

---

**Security is a continuous journey, not a destination.**

We strive daily to provide safe and reliable software.

— Agiletec Inc. Security Team
