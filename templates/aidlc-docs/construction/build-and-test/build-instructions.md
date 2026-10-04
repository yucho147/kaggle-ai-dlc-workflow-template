# Build Instructions

## Environment

- Python / OS / hardware / CUDA（該当時）: TBD
- Lockfile / package version / config: TBD

## Template Setup

```bash
uv sync --locked
uv sync --locked --group research --group mcp
```

前者は文書・CLI、後者は付属 baseline と MCP。Notebook は `--group notebooks` を追加する。
プロジェクト依存は `uv add` / `uv lock` で更新し、更新理由を audit に記録する。

## Project Commands

- Build / editable install / package artifact: TBD
- Offline・Kaggle Notebook への導入: TBD
- 必要なデータと取得経路: TBD
- 起動失敗時の確認先: TBD
