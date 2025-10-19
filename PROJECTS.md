# Agiletec Inc. - Project Portfolio

**Last Updated**: 2025-10-16

---

## 🎯 Project Categories

### 1. Self-Developed Products（自社開発プロダクト）
私たちが設計・開発・メンテナンスを行っているプロダクト

### 2. Open Source Contributions（コントリビュート先）
私たちが積極的に貢献しているオープンソースプロジェクト

---

## 🌟 Self-Developed Products

### Agiletec Platform - 統合開発基盤

**Status**: 🚧 In Development
**Repository**: Private (Turborepoモノレポ)
**Mission**: 複数ビジネスアプリケーションの効率的開発

#### 概要

AIris Suite、FocusToday Suite等の複数プロダクトを単一基盤で開発・運用するためのTurborepoモノレポ。

#### Architecture

- **Apps**: 10アプリケーション
- **Libs**: 22共有ライブラリ（UI、Logger、Domain等）
- **Infrastructure**: Supabase (Self-Hosted), Kong Gateway, Traefik
- **Multi-Tenancy**: Row-Level Security (RLS)による組織分離

#### Technology Stack

- **Monorepo**: Turborepo 2.x
- **Frontend**: Next.js 15, React 19
- **Backend**: Supabase, FastAPI (Python 3.12)
- **Database**: PostgreSQL 15
- **Infrastructure**: Docker, Traefik, Kong Gateway

#### Benefits

- **開発効率**: 共有ライブラリで3-5倍高速化
- **運用コスト**: セルフホストで月次コスト70%削減
- **品質**: 一貫したコード品質とアーキテクチャ

---

### AIris Suite - AI電話・FAX・ストレージ

**Status**: 🚧 In Development (Part of Agiletec Platform)
**Mission**: 電話業務の構造改革

#### 概要

従来の電話代行サービスの多重請負構造（企業 → 電話代行会社 → オペレーター派遣・下請け）を排除し、企業が直接AIで電話業務を完全自動化できるシステム。

#### Applications

| App | Description | Tech Stack |
|-----|-------------|-----------|
| **airis-dashboard** | 統合ダッシュボード | Next.js 15, React 19 |
| **airis-landing** | マーケティングサイト | Next.js 15, Tailwind CSS |
| **airis-evidence-script** | 音声文字起こし・NLP解析 | Next.js 15, Whisper API, GPT-4 |
| **airis-auto-call** | AI自動架電システム | Next.js 15, GPT-4o Realtime, Twilio |
| **airis-storage-smart** | 重複検出ストレージ | Python 3.12, Next.js 15 |

#### 主要機能

- 🤖 **AI音声対応**: GPT-4o Realtime API統合
- 📞 **通話管理**: Twilio連携による着信・架電
- 📝 **文字起こし**: Whisper API + NLP解析
- 📊 **ダッシュボード**: 通話記録・分析・レポート
- 📠 **FAX統合**: FAX送受信・OCR解析

#### Target Metrics

- **5年目標**: 1,000社導入
- **コスト削減**: 従来の電話代行費用から70%削減
- **稼働率**: 99.9% uptime

---

### FocusToday Suite - タスク管理SaaS

**Status**: 🚧 In Development (Part of Agiletec Platform)
**Mission**: 個人と組織の生産性改革

#### 概要

複雑な外部ツール依存を排除し、シンプルで自律的な時間管理を実現するタスク管理SaaS。

#### Applications

| App | Description | Tech Stack |
|-----|-------------|-----------|
| **focustoday** | Webアプリケーション | Next.js 15, React 19 |
| **focustoday-api** | バックエンドAPI | FastAPI (Python 3.12) |
| **focustoday-mobile** | モバイルアプリ | React Native, Expo |

#### 主要機能

- 📋 **個人・チームタスク管理**: シンプルなタスク・プロジェクト管理
- 🎯 **集中力最大化**: フォーカスモード、ポモドーロタイマー
- 📱 **モバイルアプリ**: iOS/Android対応
- 🔄 **リアルタイム同期**: チーム間でのタスク同期
- 📊 **生産性分析**: 個人・チームの生産性可視化

#### Target Metrics

- **5年目標**: 個人・組織生産性向上の標準ツールへ
- **生産性向上**: 平均30%以上のタスク完了率向上
- **継続率**: 月次継続率80%以上

---

### AIRIS MCP Gateway - 開発ツール

**Status**: ✅ Production
**Repository**: [agiletec-inc/airis-mcp-gateway](https://github.com/agiletec-inc/airis-mcp-gateway)
**Mission**: 開発環境の構造改革

#### 概要

エディタベンダーの設計による非効率な構造を排除し、開発者が環境を完全にコントロールできるMCP（Model Context Protocol）統合ゲートウェイ。

#### 主要機能

- ⚡ **トークン最適化**: 並列処理により90%削減
- 🔄 **統合管理**: 25+ MCPサーバーの一元管理
- 🧠 **インテリジェントルーティング**: 最適なMCPサーバー自動選択
- 🛡️ **エラーハンドリング**: 高度なエラー検知・リトライ機構
- 📊 **モニタリング**: パフォーマンス・コスト分析
- 🎨 **Settings UI**: サーバーON/OFF管理

#### Technology Stack

- **Language**: TypeScript
- **Backend**: FastAPI (Python)
- **Frontend**: React + Vite
- **Database**: PostgreSQL
- **Protocol**: MCP (Model Context Protocol)
- **Infrastructure**: Docker

#### Target Metrics

- **5年目標**: 10,000開発者利用
- **効率化**: トークン使用量90%削減、待ち時間80%短縮
- **採用率**: AI開発者の標準ツールへ

---

## 🤝 Open Source Contributions

### SuperClaude Framework - AI開発フレームワーク

**Status**: Active Contributor
**Repository**: [SuperClaude-Org/SuperClaude_Framework](https://github.com/SuperClaude-Org/SuperClaude_Framework)
**Role**: コントリビューター

#### 概要

AI開発ワークフローを最適化するフレームワーク。私たちは積極的にコントリビュートしています。

#### Contribution Areas

- 🐛 **Bug Fixes**: バグ修正・品質向上
- 📚 **Documentation**: ドキュメント改善・翻訳
- ✨ **Feature Additions**: 新機能の提案・実装
- 🧪 **Testing**: テストカバレッジ向上

#### Our Philosophy

オープンソースコミュニティへの貢献を通じて、技術力を高め、知見を共有します。私たちは「車輪の再発明をしない」原則に基づき、既存OSSを最大限活用し、コミュニティに還元します。

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
- ✅ Production: 本番運用中
- 🚧 Development: 開発中
- 🤝 Contributing: アクティブにコントリビュート中

---

## 🔮 Roadmap

### Q4 2025
- AIris Suite Beta Launch
- FocusToday Suite Beta Launch
- AIRIS MCP Gateway v1.0 Release

### 2026
- AIris Suite Production Launch（100社導入目標）
- FocusToday Suite Production Launch
- AIRIS MCP Gateway（1,000開発者利用目標）

### 2027-2030
- AIris Suite（1,000社導入目標）
- AIRIS MCP Gateway（10,000開発者利用目標）
- FocusToday Suite（標準ツールとしての地位確立）

---

## 🤝 Get Involved

### For Users
各プロダクトのREADMEを参照してください。

### For Developers
- [CONTRIBUTING.md](./CONTRIBUTING.md) - 貢献ガイドライン
- [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) - 行動規範

### For Partners
- Email: contact@agiletec.inc (準備中)

---

**"すべての企業に自社開発。多重請負構造を、終わらせる。"**

— Agiletec Inc.
