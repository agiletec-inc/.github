# ADR-0001: Ruleset policy brokerの署名基盤にAWS KMSを採用する

- Status: Accepted
- Date: 2026-07-27
- Owner: agiletec-inc organization owner

## Context

organization Rulesetのrequired workflow pinを更新するbrokerは、GitHub AppとしてJWTを
RS256で署名し、短命なinstallation tokenを取得する必要がある。一方、GitHub App private
keyまたはorganization write tokenをlocal Mac、GitHub Actions、Doppler、self-hosted runner、
AIris VibeOSへ置いてはならない。

現在の開発環境ではAWS credentialは未設定で、Azureはtenant-only accountでsubscriptionが
確認できない。したがって、このADRはproviderと境界を決定するが、account作成やproduction
provisioningを完了したとは扱わない。

## Decision

署名providerには、external-origin RSA signing keyを持つAWS KMSを採用する。broker runtimeは
AWS Lambdaとし、Lambda execution roleには対象key ARNへの`kms:Sign`とbroker自身のaudit出力に
必要な権限だけを与える。long-lived AWS access keyは発行しない。

GitHub Appが生成するPKCS#1 RSA private keyは、ownerが管理する一回限りの隔離import ceremonyで
PKCS#8 DERへ変換し、AWS KMSのwrapping public keyで包んでimportする。import成功、GitHub公開鍵との
署名照合、broker canary成功を確認後、平文・変換物・一時wrapping artifactを安全に破棄する。
このceremonyをlocal agent、GitHub Actions、self-hosted runnerでは実行しない。

brokerはJWTの`header.payload`を`RSASSA_PKCS1_V1_5_SHA_256`で署名する。JWTは`alg=RS256`、
`iat=now-60s`、`exp<=now+10m`、`iss=<GitHub App client ID>`に固定する。KMS key policyは
Lambda execution roleの`kms:Sign`だけを許可し、`kms:GetKeyPolicy`、export、decrypt用途をbrokerへ
与えない。

## Mutation boundary

brokerが受け付けるoperationは`ruleset-workflow-pin` v1だけで、targetは以下へ固定する。

- organization: `agiletec-inc`
- ruleset ID: `19456040`
- source repository: `agiletec-inc/github-actions`
- workflow: `.github/workflows/org-quality-gate.yml`
- ref: `refs/heads/main`

organization APIでreadしたcurrent Rulesetをcompare-and-set preconditionとし、許可するdiffは対象workflow
のSHA 1値だけとする。enforcement、conditions、bypass actors、他workflow、required checksが変わる
payloadは拒否する。AIris VibeOSはproposal admissionとstatus表示だけを行い、Lambda invoke権限、
KMS権限、GitHub tokenを持たない。

## Audit, rotation, and recovery

- CloudTrailでKMS `Sign`とLambda control-plane操作を記録する。
- broker auditにはproposal digest、before/after SHA、GitHub request ID、result、timestampを記録し、
  JWT、installation token、private keyは記録しない。
- kill switchは既定deny。provider provisioning後もdry-runとsandbox canaryが緑になるまでlive mutationを
  許可しない。
- GitHub App keyは重複期間を使ってrotateする。新keyを別KMS keyへimportし、canary後にaliasを切替え、
  旧GitHub App keyをrevokeする。
- AWS accountまたはKMS keyが利用不能な場合はmutationを停止する。local tokenへのfallbackは設けない。
- break-glass ownerはorganization ownerであり、復旧操作と監査IDを同じincident recordへ残す。

## Alternatives

### HashiCorp Vault Transit

外部RSA key importとPKCS#1 v1.5署名は可能だが、Vault cluster、unseal、backup、upgrade、Transit tokenの
運用責務が新たに必要になる。現在そのproduction ownershipがないため却下した。

### Azure Key Vault

non-exportable RSA keyは要件を満たし得るが、現在確認できるAzure accountはtenant-onlyでsubscriptionが
ない。AWS KMSより実装可能性が高い根拠がないため却下した。

### GitHub Actions secret / Doppler / self-hosted Vault

private keyを取得可能なsecretとして実行環境へ渡すため、採用済みcredential boundaryに反する。却下する。

## Provisioning stop condition

AWS account ID、region、billing owner、security contact、CloudTrail保存先がownerにより確定するまで、
KMS key import、Lambda deploy、GitHub App key生成を開始しない。これはprovider decisionの未決ではなく、
production provisioningの明示的前提条件である。

## Official references

- GitHub App private keys: https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/managing-private-keys-for-github-apps
- GitHub App JWT: https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-json-web-token-jwt-for-a-github-app
- AWS KMS imported key material: https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys-conceptual.html
- AWS KMS key wrapping/import: https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys-encrypt-key-material.html
- AWS KMS Sign API: https://docs.aws.amazon.com/kms/latest/APIReference/API_Sign.html
- Lambda execution role: https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html
- Vault Transit import/sign API: https://developer.hashicorp.com/vault/api-docs/secret/transit
