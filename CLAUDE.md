# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is Agiletec Inc.'s **organization profile repository** - a documentation-only repository containing the company's vision, project portfolio, and policies. There is **no source code** in this repository.

**Primary Language**: Japanese with English technical terms

## Repository Purpose

This repository serves as:
1. GitHub organization profile (visible at github.com/agiletec-inc)
2. Central documentation for company philosophy and mission
3. Reference for contribution guidelines and security policies
4. Portfolio overview linking to actual development projects

## Key Documents Structure

Read documents in this order to understand the organization:

1. **profile/README.md** - Public GitHub profile introduction
2. **VISION.md** - Complete company philosophy (9,867 bytes)
   - Mission: "多重請負構造を撲滅する" (Eliminate multi-tier subcontracting)
   - Vision: "すべての企業に自社開発" (In-house development for all companies)
   - Core values: Transparency, Empowerment, Craftsmanship, Agility
3. **PROJECTS.md** - Product portfolio and tech stacks
4. **CONTRIBUTING.md** - Contribution guidelines and code standards
5. **SECURITY.md** - Security policy and vulnerability reporting

## Actual Development Projects (External)

Source code lives in separate repositories:

- **Agiletec Platform** - Private Turborepo monorepo (Next.js 15, React 19, Supabase, FastAPI)
- **AIRIS MCP Gateway** - github.com/agiletec-inc/airis-mcp-gateway (Production, MIT License)
- **FocusToday** - github.com/agiletec-inc/focustoday (Beta)
- **AIris Suite** - Private (In development)

## Documentation Standards

### Language Convention
- **Primary**: Japanese for narrative and explanations
- **Technical Terms**: English is acceptable (e.g., "Turborepo", "Docker", "API")
- **Code Examples**: English comments preferred for code standards

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

**Approach**: "伴走型開発" (Companion-style development) - collaborative development with technology transfer

## Security

For security vulnerabilities: **security@agiletec.inc** (in preparation)

Do NOT create public issues for security concerns.

## Index Files

Two generated index files provide quick reference:
- **PROJECT_INDEX.md** - Human-readable comprehensive index
- **PROJECT_INDEX.json** - Machine-readable structured data

These files reduce token usage by 94% - reference them instead of re-reading all documentation files.

## Git Workflow

- **Main Branch**: master
- **Branch Naming**: `feature/description`, `fix/description`, `docs/description`
- **Recent Focus**: Documentation synchronization and branding updates

## Contact

- **Email**: contact@agiletec.inc (in preparation)
- **X (Twitter)**: @AgiletecInc (in preparation)
- **GitHub**: Organization discussions for each project
