# Strategy

## Objective / Priorities

「記録を保全して再開できる」「根拠と条件がつながる」「付属実装を実行できる」を優先する。

| Hypothesis | Priority | Evidence | Minimum change / check | Status |
| --- | --- | --- | --- | --- |
| hyp001: seed と記録の分離で派生運用を続けられる | P1 | 旧 CI / init | backup と derived project regression | reviewed |
| hyp002: 用途別工程と契約で PoC 判断を具体化できる | P1 | 旧 skill / docs | 27 seed、4 skills、source / data / evaluation / PoC docs | implemented |
| hyp003: 取得を1境界にすると CLI 差と失敗を追跡できる | P1 | CLI help / 旧 MCP | actual parser、protocol、errors / snapshots | reviewed |
| hyp004: データ・fold・ID 契約で誤評価を検知できる | P1 | 旧 baseline | CSV / OOF / submission / MLflow tests と smoke | reviewed |
| hyp005: 正本から HTML を生成すると review を継続できる | P2 | 旧 renderer | tables / links / raw HTML / nav regression | reviewed |

## Scope / Next Use

今回の改善はユーザーが依頼済み。モデル性能改善や新しい競技の調査は次の案件で行う。
用途別 workflow は実案件でも確認し、質問数・判断の不足・再実行性を次の改善候補として残す。
