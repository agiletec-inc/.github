# Agiletec Inc. - Project Portfolio

**Last Updated**: 2025-11-09

---

## 🎯 Project Categories

### 1. Self-Developed Products
Products we design, develop, and maintain

### 2. Open Source Contributions
Open source projects we actively contribute to

---

## 🌟 Self-Developed Products

### Agiletec Platform - Integrated Development Foundation

**Status**: 🚧 In Development
**Repository**: Private (Turborepo monorepo)
**Mission**: Efficient development of multiple business applications

#### Overview

A Turborepo monorepo for developing and operating multiple products such as AIris Suite and FocusToday Suite on a single platform.

#### Architecture

- **Apps**: 10 applications
- **Libs**: 22 shared libraries (UI, Logger, Domain, etc.)
- **Infrastructure**: Supabase (Self-Hosted), Kong Gateway, Traefik
- **Multi-Tenancy**: Organization isolation via Row-Level Security (RLS)

#### Technology Stack

- **Monorepo**: Turborepo 2.x
- **Frontend**: Next.js 15, React 19
- **Backend**: Supabase, FastAPI (Python 3.12)
- **Database**: PostgreSQL 15
- **Infrastructure**: Docker, Traefik, Kong Gateway

#### Benefits

- **Development Efficiency**: 3-5x faster with shared libraries
- **Operational Cost**: 70% monthly cost reduction through self-hosting
- **Quality**: Consistent code quality and architecture

---

### AIris Suite - AI Phone, FAX & Storage

**Status**: 🚧 In Development (Part of Agiletec Platform)
**Mission**: Structural reform of phone operations

#### Overview

A system that eliminates the multi-tier subcontracting structure of traditional phone agency services (Company → Phone Agency → Dispatched/Subcontracted Operators), enabling companies to fully automate phone operations directly with AI.

#### Applications

| App | Description | Tech Stack |
|-----|-------------|-----------|
| **airis-dashboard** | Integrated dashboard | Next.js 15, React 19 |
| **airis-landing** | Marketing site | Next.js 15, Tailwind CSS |
| **airis-evidence-script** | Voice transcription & NLP analysis | Next.js 15, Whisper API, GPT-4 |
| **airis-auto-call** | AI auto-dialing system | Next.js 15, GPT-4o Realtime, Twilio |
| **airis-storage-smart** | Deduplication storage | Python 3.12, Next.js 15 |

#### Key Features

- 🤖 **AI Voice Response**: GPT-4o Realtime API integration
- 📞 **Call Management**: Incoming/outgoing calls via Twilio
- 📝 **Transcription**: Whisper API + NLP analysis
- 📊 **Dashboard**: Call records, analysis, reports
- 📠 **FAX Integration**: FAX send/receive, OCR analysis

#### Target Metrics

- **5-year Goal**: 1,000 company deployments
- **Cost Reduction**: 70% reduction from traditional phone agency costs
- **Uptime**: 99.9%

---

### FocusToday Suite - Task Management SaaS

**Status**: 🚧 In Development (Part of Agiletec Platform)
**Mission**: Individual and organizational productivity reform

#### Overview

A task management SaaS that eliminates complex external tool dependencies and achieves simple, autonomous time management.

#### Applications

| App | Description | Tech Stack |
|-----|-------------|-----------|
| **focustoday** | Web application | Next.js 15, React 19 |
| **focustoday-api** | Backend API | FastAPI (Python 3.12) |
| **focustoday-mobile** | Mobile app | React Native, Expo |

#### Key Features

- 📋 **Personal & Team Task Management**: Simple task and project management
- 🎯 **Concentration Maximization**: Focus mode, Pomodoro timer
- 📱 **Mobile App**: iOS/Android support
- 🔄 **Real-time Sync**: Task synchronization across teams
- 📊 **Productivity Analysis**: Visualize individual and team productivity

#### Target Metrics

- **5-year Goal**: Become standard tool for individual/organizational productivity improvement
- **Productivity Improvement**: 30%+ average task completion rate improvement
- **Retention Rate**: 80%+ monthly retention

---

### AIRIS MCP Gateway - Development Tool

**Status**: ✅ Production
**Repository**: [agiletec-inc/airis-mcp-gateway](https://github.com/agiletec-inc/airis-mcp-gateway)
**Mission**: Structural reform of development environments

#### Overview

An integrated MCP (Model Context Protocol) gateway that eliminates inefficiencies from editor vendor designs, giving developers complete control over their environment.

#### Key Features

- ⚡ **Token Optimization**: 90% reduction through parallel processing
- 🔄 **Integrated Management**: Centralized management of 25+ MCP servers
- 🧠 **Intelligent Routing**: Automatic selection of optimal MCP servers
- 🛡️ **Error Handling**: Advanced error detection and retry mechanisms
- 📊 **Monitoring**: Performance and cost analysis
- 🎨 **Settings UI**: Server ON/OFF management

#### Technology Stack

- **Language**: TypeScript
- **Backend**: FastAPI (Python)
- **Frontend**: React + Vite
- **Database**: PostgreSQL
- **Protocol**: MCP (Model Context Protocol)
- **Infrastructure**: Docker

#### Target Metrics

- **5-year Goal**: 10,000 developer users
- **Efficiency**: 90% token usage reduction, 80% wait time reduction
- **Adoption**: Become standard tool for AI developers

---

## 🤝 Open Source Contributions

### SuperClaude Framework - AI Development Framework

**Status**: Active Contributor
**Repository**: [SuperClaude-Org/SuperClaude_Framework](https://github.com/SuperClaude-Org/SuperClaude_Framework)
**Role**: Contributor

#### Overview

A framework that optimizes AI development workflows. We actively contribute to this project.

#### Contribution Areas

- 🐛 **Bug Fixes**: Bug fixes and quality improvements
- 📚 **Documentation**: Documentation improvements and translations
- ✨ **Feature Additions**: Proposing and implementing new features
- 🧪 **Testing**: Improving test coverage

#### Our Philosophy

We enhance our technical skills and share knowledge through contributions to open source communities. Based on the principle of "don't reinvent the wheel," we maximize use of existing OSS and give back to the community.

---

## 📊 Project Status Summary

| Project | Status | Type | License | Public |
|---------|--------|------|---------|--------|
| Agiletec Platform | 🚧 Development | Internal | Proprietary | Private |
| AIris Suite | 🚧 Development | Self-Developed | Proprietary | Private |
| FocusToday Suite | 🚧 Development | Self-Developed | Proprietary | Private |
| AIRIS MCP Gateway | ✅ Production | Self-Developed | MIT | Public |
| SuperClaude Framework | 🤝 Contributing | Contribution | MIT | Public |

**Legend**:
- ✅ Production: In production
- 🚧 Development: Under development
- 🤝 Contributing: Actively contributing

---

## 🔮 Roadmap

### Q4 2025
- AIris Suite Beta Launch
- FocusToday Suite Beta Launch
- AIRIS MCP Gateway v1.0 Release

### 2026
- AIris Suite Production Launch (100 company deployment goal)
- FocusToday Suite Production Launch
- AIRIS MCP Gateway (1,000 developer user goal)

### 2027-2030
- AIris Suite (1,000 company deployment goal)
- AIRIS MCP Gateway (10,000 developer user goal)
- FocusToday Suite (establish position as standard tool)

---

## 🤝 Get Involved

### For Users
Please refer to each product's README.

### For Developers
- [CONTRIBUTING.md](./CONTRIBUTING.md) - Contribution guidelines
- [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) - Code of conduct

### For Partners
- Email: hello@agiletec.net

---

**"In-house development for every company. End the multi-tier subcontracting structure."**

— Agiletec Inc.
