# Contributing to Agiletec Inc.

私たちAgiletec Inc.のビジョンに共感し、貢献していただきありがとうございます。

## 🎯 Our Mission

**多重請負構造を撲滅する。**

私たちは、日本のIT業界の構造的非効率を解決し、すべての企業が自社開発力を持つ未来を実現します。

---

## 🤝 How to Contribute

### 1. オープンソースプロジェクトへの貢献

#### 自社開発プロジェクト

Agiletec Inc.が開発・メンテナンスしているオープンソースプロジェクト：

- **[AIRIS MCP Gateway](https://github.com/agiletec-inc/airis-mcp-gateway)** - MCP統合ゲートウェイ
- **[FocusToday](https://github.com/agiletec-inc/focustoday)** - タスク管理SaaS

#### コントリビュート先

私たちが積極的に貢献しているオープンソースプロジェクト：

- **[SuperClaude Framework](https://github.com/SuperClaude-Org/SuperClaude_Framework)** - AI開発フレームワーク

各プロジェクトの`CONTRIBUTING.md`を参照してください。

---

### 2. Issue報告

バグ報告や機能提案は、各プロジェクトのIssueで受け付けています。

**良いIssueの例**:
- 再現手順が明確
- 期待される動作と実際の動作の説明
- 環境情報（OS, バージョン等）

---

### 3. Pull Request

**貢献の流れ**:

1. **Fork**: プロジェクトをFork
2. **Branch**: `feature/your-feature-name`ブランチを作成
3. **Implement**: コード変更を実装
4. **Test**: テストを追加・実行
5. **Commit**: [Conventional Commits](https://www.conventionalcommits.org/)に従う
6. **Push**: 自分のForkにPush
7. **PR**: 本家リポジトリにPull Request作成

**Commit Message Format**:
```
feat: add new API endpoint for user management
fix: correct authentication token validation
docs: update README installation section
chore: update dependencies
refactor: simplify error handling logic
```

---

### 4. Code Standards

#### General Principles
- **SOLID**: Single Responsibility, Open/Closed, Liskov Substitution
- **DRY**: Don't Repeat Yourself
- **YAGNI**: You Aren't Gonna Need It
- **KISS**: Keep It Simple, Stupid

#### TypeScript/JavaScript
- ESLint + Prettier設定に従う
- 型定義は明示的に
- コメントはWHYを説明（WHATではなく）

#### Python
- Black + Ruff設定に従う
- Type hints必須（Python 3.12+）
- Docstrings（Google Style）

---

### 5. Documentation

**必須ドキュメント**:
- `README.md`: プロジェクト概要、インストール方法
- `ARCHITECTURE.md`: 技術的アーキテクチャ（複雑なプロジェクトのみ）
- `CHANGELOG.md`: バージョン履歴
- Inline Comments: 複雑なロジックの説明

**ドキュメント原則**:
- 日本語優先（技術用語は英語可）
- 例を含める
- 最新状態を保つ

---

## 💡 Contribution Ideas

### Beginner-Friendly
- ドキュメント誤字修正
- サンプルコード追加
- 翻訳（英語⇄日本語）
- テストカバレッジ向上

### Intermediate
- バグ修正
- 新機能実装
- パフォーマンス改善
- リファクタリング

### Advanced
- アーキテクチャ改善
- セキュリティ強化
- スケーラビリティ対応
- 新プロダクト提案

---

## 🛡️ Security

セキュリティ脆弱性を発見した場合は、**公開Issueを作成せず**、直接ご連絡ください：

📧 **security@agiletec.inc** (準備中)

詳細は[SECURITY.md](./SECURITY.md)を参照してください。

---

## 📋 Code Review Process

1. **自動チェック**: CI/CD（lint, test, build）が通ること
2. **Code Review**: メンテナーが1-3営業日以内にレビュー
3. **Feedback**: 修正依頼がある場合はコメント
4. **Approval**: 承認後にマージ

**レビュー基準**:
- コードの品質
- テストの網羅性
- ドキュメントの明確さ
- ビジョンとの整合性

---

## 🌟 Recognition

貢献者は以下で認識されます：
- プロジェクトの`CONTRIBUTORS.md`に記載
- リリースノートで感謝の意を表明
- 大きな貢献には特別な謝辞

---

## 🤔 Questions?

不明点があれば、遠慮なくご連絡ください：

- **GitHub Discussions**: 各プロジェクトのDiscussions
- **Email**: contact@agiletec.inc (準備中)
- **X (Twitter)**: [@AgiletecInc](https://twitter.com/AgiletecInc) (準備中)

---

## 📄 License

貢献されたコードは、各プロジェクトのライセンス（通常はMIT License）に従います。

---

**ご協力ありがとうございます！**

「すべての企業に自社開発。」のビジョン実現に向けて、共に前進しましょう。

— Agiletec Inc. Team
