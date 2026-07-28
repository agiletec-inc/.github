# Organization quality gate契約

organization required workflowは全repoへ同じgateを適用する。stack detectionがNode、Bun、Python、Rust、Swiftの
該当jobを選び、secret scan、feature flag check、final aggregatorは常に実行する。

repo別の例外機構は設けない。native CIを持つrepoでもgeneric stack jobを実行し、単一で均一なgateを優先する。
`org-quality-gate.yml` / `quality-gate.yml`へrepo名条件やopt-out inputを再導入しない。
