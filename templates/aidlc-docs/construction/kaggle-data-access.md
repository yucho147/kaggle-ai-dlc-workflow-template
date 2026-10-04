# Kaggle Data Access

Kaggle を使用する案件で記入する。取得境界は `tools/kaggle-mcp/server.py` または CLI wrapper でよい。
Training に MCP client や抽象 gateway を組み込む必要はない。

## Configuration

- Competition / dataset / notebook refs: TBD
- MCP / CLI / 手動の経路と選択理由: TBD
- CLI version / help 確認日時: TBD
- 認証方式（秘密値を記載しない）: TBD
- 保存先 / dataset revision / fingerprint: TBD
- 調査上限・pagination・timeout: TBD

## Retrieval Contract

- 一覧 metadata、URL、取得した本文を区別する。
- Tool の `ok` / `error` / `truncated` を確認する。
- 本文の source ID、snapshot、要約を `../inception/source-register.md` に記録する。
- Cache が失われても、判断の根拠は docs に残す。
- 外部 Notebook は license・依存・前提を確認するまで実行しない。
- Download のサイズ・保存先を確認し、必要な file のみ取得する。

## CLI Examples

実機の help を優先する。テンプレートで確認した Kaggle 2.2 系の例:

```bash
uv run kaggle --version
uv run kaggle --help
uv run kaggle competitions files <competition>
uv run kaggle competitions download <competition> -p data/raw/<competition>
uv run kaggle competitions topics list <competition> -s top
uv run kaggle competitions topics show <competition> <topic-id>
uv run kaggle kernels list --competition <competition>
```

Sort・format・paging は command ごとに異なる。Discussion と leaderboard は別の証拠。
取得と提出は別工程。規約受諾・外部への提出はユーザーの指示に従う。
