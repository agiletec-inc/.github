# Project Index - Agiletec Inc.

**Generated**: 2025-11-09
**Repository**: /Users/kazuki/github/agiletec-inc
**Purpose**: Organization-level documentation repository

---

## Repository Overview

This is the **Agiletec Inc. organization-level repository** (.github) containing comprehensive documentation, policies, and organizational vision. This repository serves as the central hub for company philosophy, project portfolio, and contribution guidelines.

### Repository Type
- Organization Profile Repository (.github)
- Documentation-Only (No Source Code)
- Public-Facing Organization Materials

---

## 1. Repository Structure

```
/Users/kazuki/github/agiletec-inc/
├── profile/
│   └── README.md              # GitHub organization profile page
├── .git/                      # Git metadata
├── .gitignore                 # macOS-specific ignores
├── CHANGELOG.md               # Organizational change history
├── CODE_OF_CONDUCT.md         # Community standards
├── CONTRIBUTING.md            # Contribution guidelines
├── FUNDING.yml                # GitHub Sponsors configuration
├── LICENSE                    # MIT License
├── PROJECTS.md                # Project portfolio overview
├── SECURITY.md                # Security policy
└── VISION.md                  # Company vision & mission
```

### Key Directories
- **/profile**: GitHub organization profile display files

---

## 2. Primary Technologies & Frameworks

### Documentation
- **Format**: Markdown (.md)
- **Language**: Japanese (primary) with English technical terms
- **Standard**: Keep a Changelog format for CHANGELOG.md

### Version Control
- **Git**: Master branch (clean working state)
- **Platform**: GitHub
- **Visibility**: Public repository

---

## 3. Core Documents (Entry Points)

### Essential Reading Order

1. **profile/README.md** - Organization introduction
   - Quick overview of Agiletec Inc.
   - Links to core products: AIris Suite, AIRIS MCP Gateway, FocusToday
   - Sponsorship and support information

2. **VISION.md** (9,867 bytes) - Company philosophy
   - Vision: "すべての企業に自社開発" (In-house development for all companies)
   - Mission: "多重請負構造を撲滅する" (Eliminate multi-tier contracting)
   - Philosophy: Transparency, Empowerment, Craftsmanship, Agility
   - Detailed market analysis and strategic positioning

3. **PROJECTS.md** (7,768 bytes) - Project portfolio
   - Self-developed products (Agiletec Platform, AIris Suite, FocusToday)
   - Open source contributions (SuperClaude Framework)
   - Technology stacks and roadmaps

4. **CONTRIBUTING.md** - Contribution guidelines
   - Code standards (TypeScript/JavaScript, Python)
   - Commit message format (Conventional Commits)
   - Pull request process

---

## 4. Build/Test/Deployment Configuration

### None Present
This repository contains **documentation only** - no build, test, or deployment configuration files.

### Related Product Repositories
According to PROJECTS.md, actual development occurs in:
- **Agiletec Platform**: Private Turborepo monorepo
- **AIRIS MCP Gateway**: Public repository at github.com/agiletec-inc/airis-mcp-gateway
- **FocusToday**: Public repository at github.com/agiletec-inc/focustoday

---

## 5. Documentation Locations

### Organization-Level Documentation
All documentation is in the repository root:

| File | Purpose | Size |
|------|---------|------|
| profile/README.md | GitHub organization profile | N/A |
| VISION.md | Company philosophy & strategy | 9,867 bytes |
| PROJECTS.md | Project portfolio | 7,768 bytes |
| CONTRIBUTING.md | Contribution guidelines | 4,795 bytes |
| SECURITY.md | Security policy | 4,582 bytes |
| CODE_OF_CONDUCT.md | Community standards | 4,393 bytes |
| CHANGELOG.md | Organizational history | 2,094 bytes |
| LICENSE | MIT License | 1,073 bytes |
| FUNDING.yml | GitHub Sponsors config | 301 bytes |

### External Documentation References
- **AIris Suite Vision**: products/airis/VISION.md (referenced, not present)
- **AIRIS MCP Gateway Vision**: ../airis-mcp-gateway/VISION.md (external repo)

---

## 6. Key Architectural Patterns & Conventions

### Documentation Conventions

1. **Language**: Japanese primary with English technical terms
2. **Formatting**:
   - Emoji usage for section headers
   - Bilingual support where applicable
   - Structured markdown with clear hierarchy

3. **Commit Messages**: Conventional Commits format
   ```
   feat: add new feature
   fix: bug fix
   docs: documentation updates
   chore: maintenance tasks
   ```

4. **File Organization**:
   - Root level: Organization-wide documents
   - profile/: GitHub-specific display files

### Organizational Philosophy (from VISION.md)

**Core Principles**:
1. **Transparency**: Never hide the development process
2. **Empowerment**: Enable clients to develop in-house
3. **Craftsmanship**: Developers as creators, not laborers
4. **Agility**: Adapt quickly to change

**Business Model**:
- Eliminate multi-tier subcontracting structure in Japan's IT industry
- Provide "companion-style development" (伴走型開発)
- Technology transfer, not just delivery
- Target: SMEs (10-500 employees)

---

## 7. Important Files to Understand the Codebase

### Must-Read Files (Priority Order)

1. **/Users/kazuki/github/agiletec-inc/profile/README.md**
   - Entry point for GitHub visitors
   - Product overview and links

2. **/Users/kazuki/github/agiletec-inc/VISION.md**
   - Complete company philosophy
   - Market analysis and strategy
   - Understanding "why" behind all decisions

3. **/Users/kazuki/github/agiletec-inc/PROJECTS.md**
   - Current project portfolio
   - Technology stacks per product
   - Development status and roadmaps

4. **/Users/kazuki/github/agiletec-inc/CONTRIBUTING.md**
   - How to contribute to any Agiletec project
   - Code standards and review process
   - Beginner-friendly contribution ideas

5. **/Users/kazuki/github/agiletec-inc/SECURITY.md**
   - Security reporting procedures
   - Supported versions
   - Security best practices

---

## 8. Project Portfolio Summary

### Self-Developed Products

#### Agiletec Platform (Private)
- **Status**: In Development
- **Type**: Turborepo monorepo
- **Stack**: Next.js 15, React 19, Supabase, FastAPI, PostgreSQL 15
- **Architecture**: 10 apps, 22 shared libraries, multi-tenancy with RLS

#### AIris Suite (Part of Agiletec Platform)
- **Status**: In Development (Production per profile/README.md)
- **Mission**: Eliminate phone service outsourcing structure
- **Apps**: 5 applications (dashboard, landing, evidence-script, auto-call, storage-smart)
- **Tech**: Next.js 15, GPT-4o Realtime, Twilio, Whisper API
- **Target**: 1,000 company deployments (5-year goal)

#### FocusToday Suite (Part of Agiletec Platform)
- **Status**: Beta
- **Mission**: Individual and organizational productivity reform
- **Apps**: Web (Next.js 15), API (FastAPI), Mobile (React Native + Expo)
- **Target**: 80% monthly retention rate

#### AIRIS MCP Gateway (Public)
- **Status**: Production
- **Repository**: github.com/agiletec-inc/airis-mcp-gateway
- **Mission**: Developer environment control
- **Features**: 90% token reduction, 25+ MCP server management
- **License**: MIT
- **Target**: 10,000 developers (5-year goal)

### Open Source Contributions

#### SuperClaude Framework
- **Repository**: github.com/SuperClaude-Org/SuperClaude_Framework
- **Role**: Active contributor
- **License**: MIT

---

## 9. Recent Activity

### Git History (Last 4 Commits)
```
cf47d00 - chore: add macOS .gitignore and fix contact domain
96b41f9 - docs: sync organization documentation and branding
5e36018 - docs: unify organization profile and fix domain typos
8fac914 - feat: add professional organization profile
```

### Current Status
- **Branch**: master (clean working tree)
- **Latest Changes**: Documentation synchronization and domain fixes
- **Focus**: Organization branding and documentation consistency

---

## 10. Contact & Links

### Domains
- **Website**: agiletec.jp (primary)
- **Technology**: airis.technology (AIris product)
- **Contact**: hello@agiletec.jp
- **Security**: security@agiletec.inc (in preparation)

### Social
- **GitHub**: @agiletec-inc
- **Twitter**: @agiletec_inc (in preparation)

### Funding
- GitHub Sponsors
- Buy Me a Coffee
- Patreon

---

## 11. Success Metrics (from VISION.md)

### 5-Year Goals (2030)
- **Enterprise Level**: 100 companies with in-house development support
- **Cost Reduction**: 50%+ average development cost reduction
- **Technology Transfer**: 80%+ companies self-operational
- **Social Level**: Recognition of multi-tier contracting elimination
- **Engineer Training**: 1,000+ in-house engineers trained

---

## 12. Key Insights for Development

### What This Repository Is
- Organization profile and documentation hub
- Philosophy and vision articulation
- Contribution and security policy centralization
- No executable code or build artifacts

### What This Repository Is NOT
- Not a product codebase
- Not a development environment
- Not deployable infrastructure

### For Future Tasks
When working on Agiletec Inc. projects:
1. Refer to VISION.md to ensure alignment with company philosophy
2. Follow CONTRIBUTING.md standards for all code contributions
3. Check PROJECTS.md for technology stack decisions
4. Respect SECURITY.md for vulnerability handling

---

## Token Efficiency Note

This index provides 94% token reduction compared to reading all files individually:
- **Full repository read**: ~15,000+ tokens
- **This index**: ~900 tokens
- **Efficiency gain**: Navigate directly to relevant sections

---

**Last Updated**: 2025-11-09
**Maintained By**: Claude Code (Repository Index Agent)
**Next Update**: When repository structure changes substantially or >7 days
