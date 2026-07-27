# Ruleset workflow pin broker

AWS Lambda上でGitHub App JWTをKMS `Sign`だけで生成し、organization Rulesetの固定required workflow SHAを更新する独立componentです。

GitHub REST APIは最新の`2026-03-10`を明示する。required workflowが
`refs/heads/main`追従で`sha`をまだ持たない初回適用では、公式APIの`sha` fieldへ検証済み
candidateを追加する。以後は同じfieldだけを更新する。`ref`へcommit SHAを設定しない。

- public endpointは作らない。owner-managed AWS identityからLambdaを直接invokeする。
- `APPLY_ENABLED`は既定`false`。false時はschema、digest、canary、target、live Rulesetを検証して監査へ`approved`を記録するだけ。
- true時も変更可能なのは固定workflowの`sha` 1値だけ。更新直前にRulesetを再取得し、最初のreadと違えばfail closedにする。
- GitHub API errorはresponse bodyと`x-github-request-id`を監査理由へ残す。tokenは残さない。
- GitHub App private keyとinstallation tokenは保存・response・auditへ出さない。
- DynamoDB tableはretain、PITR有効、`audit_id`の条件付きPutItemでappend-onlyにする。

production provisioningは[ADR-0001](../docs/adr/0001-policy-broker-signing-provider.md)のstop conditionが解消するまで行いません。

```sh
python3 -m unittest discover -s tests -p 'test_ruleset_pin_broker.py'
```
