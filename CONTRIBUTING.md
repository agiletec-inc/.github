# Contribution guide

agiletec-incの公開projectへのIssue・Pull Requestを歓迎します。変更対象repoのREADME、license、security policy、
contribution guideを先に確認してください。

## Issue

再現手順、期待結果、実際の結果、version・OSなど必要な環境情報を記載してください。security vulnerabilityは
public Issueへ書かず[`SECURITY.md`](./SECURITY.md)のprivate reporting channelを使ってください。

## Pull Request

- 一つの責務へ絞り、関連Issueと変更理由を示す。
- repoのformat、lint、typecheck、testを実行し、実commandと結果を書く。
- user-visible behaviorや運用境界を変える場合だけ、正本の文書を同時に更新する。
- generated file、secret、credential、customer dataをcommitしない。
- 既存codeの命名、comment密度、architectureへ合わせる。

reviewではcorrectness、security、互換性、scope、検証可能性を確認します。変更依頼へ対応後、required checksが
greenになればmaintainerがmergeします。

## License

contributionには対象repoのlicenseが適用されます。
