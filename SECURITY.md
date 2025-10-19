# Security Policy

## 🛡️ Agiletec Inc. Security Commitment

私たちは、ユーザーとコミュニティのセキュリティを最優先事項としています。

**Philosophy**: 透明性と責任あるディスクロージャー

---

## 🔍 Supported Versions

セキュリティアップデートを提供しているバージョン：

| Project | Version | Supported |
|---------|---------|-----------|
| AIRIS MCP Gateway | 1.x.x | ✅ |
| Focus | 0.x.x (Beta) | ✅ |
| SuperClaude Framework | 1.x.x | ✅ |

---

## 🚨 Reporting a Vulnerability

### 報告方法

**重要**: セキュリティ脆弱性を公開Issueで報告しないでください。

**連絡先**:
- 📧 **Email**: security@agiletec.inc (準備中)
- 🔒 **暗号化**: PGP Key available on request

**報告内容**:
1. 脆弱性の詳細な説明
2. 影響を受けるバージョン
3. 再現手順（PoC）
4. 潜在的な影響範囲
5. 可能であれば修正案

---

### 対応プロセス

**タイムライン**:

1. **受理** (24時間以内)
   - 報告を確認し、受理通知を送信

2. **初期評価** (3営業日以内)
   - 脆弱性の深刻度を評価（CVSS v3.1）
   - 影響範囲の調査

3. **修正開発** (深刻度により)
   - Critical: 1週間以内
   - High: 2週間以内
   - Medium: 1ヶ月以内
   - Low: 次回リリース

4. **パッチリリース**
   - セキュリティパッチのリリース
   - CVE番号の取得（必要に応じて）

5. **公開** (パッチリリース後90日)
   - 脆弱性の詳細公開
   - 報告者への謝辞

---

## 🏆 Vulnerability Rewards

### 報奨金プログラム

**対象プロジェクト**:
- AIRIS MCP Gateway
- Focus
- SuperClaude Framework
- Agiletec Platform（非公開プロダクト）

**報奨金額** (現在検討中):
- **Critical**: $500 - $2,000
- **High**: $200 - $500
- **Medium**: $50 - $200
- **Low**: 謝辞のみ

**除外対象**:
- サードパーティライブラリの既知の脆弱性
- 社会工学的攻撃
- 物理的アクセスを必要とする攻撃
- DoS/DDoS攻撃

---

## 🔒 Security Best Practices

### 開発時

**秘密情報管理**:
- ✅ Infisical等のSecret Managerを使用
- ❌ `.env`ファイルをGitにコミットしない
- ❌ APIキーをコードにハードコードしない

**依存関係管理**:
- `npm audit`または`pnpm audit`を定期実行
- Dependabotを有効化
- 定期的なライブラリ更新

**認証・認可**:
- JWT token有効期限を設定
- CSRF保護を実装
- Rate limitingを導入

---

### デプロイ時

**インフラセキュリティ**:
- ✅ HTTPS/TLS強制
- ✅ 最小権限の原則（Least Privilege）
- ✅ ネットワーク分離（Docker networks）
- ✅ 定期的なセキュリティパッチ適用

**データ保護**:
- データベース暗号化（at-rest, in-transit）
- Row-Level Security（RLS）による多重テナント分離
- バックアップ暗号化

---

## 📊 Security Audit History

| Date | Auditor | Scope | Findings |
|------|---------|-------|----------|
| TBD | Internal | AIRIS Platform | TBD |
| TBD | External | MCP Gateway | TBD |

---

## 🔐 Compliance

### Standards

私たちは以下のセキュリティ標準に準拠するよう努めています：

- **OWASP Top 10** (Web Application Security)
- **CWE Top 25** (Common Weakness Enumeration)
- **NIST Cybersecurity Framework** (Infrastructure Security)

### Data Protection

- **GDPR準拠** (EU顧客向け)
- **個人情報保護法準拠** (日本国内)
- データ最小化原則

---

## 📚 Security Resources

### 学習資料

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Supabase Security Best Practices](https://supabase.com/docs/guides/auth)
- [Docker Security](https://docs.docker.com/engine/security/)

### ツール

- **Static Analysis**: ESLint security plugins
- **Dependency Scanning**: Snyk, npm audit
- **Secret Scanning**: git-secrets, TruffleHog
- **Container Scanning**: Trivy

---

## 🙏 Acknowledgments

セキュリティ研究者の方々に感謝します：

- (報告者名 - 脆弱性公開後に追加)

---

## 📞 Contact

セキュリティに関する一般的な質問：

- 📧 **Email**: security@agiletec.inc (準備中)
- 🐙 **GitHub Security Advisory**: 各プロジェクトのSecurity tab

---

**Security is a continuous journey, not a destination.**

私たちは、安全で信頼できるソフトウェアを提供するために日々努力しています。

— Agiletec Inc. Security Team
