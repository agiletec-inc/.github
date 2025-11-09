# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is Agiletec Inc.'s **organization profile repository** - a documentation-only repository containing the company's vision, project portfolio, and policies. There is **no source code** in this repository.

**Primary Language**: English (all documents translated to English as of 2025-11-09)

## Repository Purpose

This repository serves as:
1. GitHub organization profile (visible at github.com/agiletec-inc)
2. Central documentation for company philosophy and mission
3. Reference for contribution guidelines and security policies
4. Portfolio overview linking to actual development projects

## Key Documents Structure

Read documents in this order to understand the organization:

1. **profile/README.md** - Public GitHub profile introduction with links to all 9 OSS repositories
2. **VISION.md** - Complete company philosophy
   - Mission: Eliminate the multi-tier subcontracting structure
   - Vision: In-house development for every company
   - Core values: Transparency, Empowerment, Craftsmanship, Agility
3. **PROJECTS.md** - Product portfolio and tech stacks
4. **CONTRIBUTING.md** - Contribution guidelines and code standards
5. **CODE_OF_CONDUCT.md** - Community standards
6. **SECURITY.md** - Security policy and vulnerability reporting
7. **CHANGELOG.md** - Organizational changelog

## Open Source Projects (9 Repositories)

### AI & LLM Tools
- **airis-mcp-gateway** - MCP gateway (90% token reduction) - Production, 32 stars
- **superagent** - Claude Code enhancement framework - Active Development
- **mindbase** - AI conversation knowledge management - Active Development
- **neural** - Local translation tool - Beta

### Developer Tools
- **selfhosted-supabase-mcp** - Supabase MCP server - Production
- **cmd-ime** - macOS input method switcher - Beta

### Distribution
- **homebrew-tap** - Official Homebrew tap - Active
- **homebrew-mindbase** - MindBase Homebrew tap - Active

### Organization
- **.github** - This repository (organization profile and community health)

## Documentation Standards

### Language Convention
- **Primary**: English for all documentation
- **Technical Terms**: Standard English technical terminology
- **Japanese Context**: Japanese business context explained in English (e.g., "multi-tier subcontracting structure" referring to Japan's IT industry)
- **Code Examples**: English comments

### Formatting
- Use emoji section headers (🎯, 🚀, 💡, etc.)
- Maintain structured markdown hierarchy
- Include table of contents for long documents

### Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new product to portfolio
fix: correct typo in vision document
docs: update security policy
chore: sync organization branding
```

### Code Standards (from CONTRIBUTING.md)

**TypeScript/JavaScript:**
- ESLint + Prettier compliance
- Explicit type definitions
- Comments explain WHY, not WHAT

**Python:**
- Black + Ruff compliance
- Type hints required (Python 3.12+)
- Google-style docstrings

**Principles:**
- SOLID, DRY, YAGNI, KISS

## Company Philosophy Context

When editing documentation, maintain alignment with core philosophy:

1. **Transparency** - Make processes and decisions visible
2. **Empowerment** - Enable self-sufficiency, not dependency
3. **Craftsmanship** - Value technical excellence and pride in work
4. **Agility** - Embrace change and rapid iteration

**Market Position**: Companion-style development for Japanese SMEs (10-500 employees)

**Mission**: Eliminate Japan's multi-tier IT subcontracting structure through technology transfer and in-house development support

## Security

For security vulnerabilities: **security@agiletec.net**

Do NOT create public issues for security concerns.

## Index Files

Two generated index files provide quick reference:
- **PROJECT_INDEX.md** - Human-readable comprehensive index
- **PROJECT_INDEX.json** - Machine-readable structured data

These files reduce token usage by 94% - reference them instead of re-reading all documentation files.

## Git Workflow

- **Main Branch**: master
- **Branch Naming**: `feature/description`, `fix/description`, `docs/description`
- **Recent Updates**: All documentation translated to English (2025-11-09)

## Contact

- **Website**: https://agiletec.net (Japanese corporate site)
- **Email**: hello@agiletec.net
- **X (Twitter)**: @agiletec_inc
- **GitHub**: Organization discussions for each project

## Important Notes for Claude Code

- This is a **documentation-only repository** - no build commands, tests, or source code
- All documents are now in **English** (updated 2025-11-09)
- Japanese corporate site (agiletec.net) provides Japanese-language business information
- Actual development happens in separate repositories listed in profile/README.md
- When making changes, maintain consistency with the organization's mission to eliminate multi-tier subcontracting structures
