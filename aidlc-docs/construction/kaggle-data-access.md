# Kaggle Data Access

このドキュメントは、Kaggle の Competition / Discussion / Notebook / Dataset / Submission API へのアクセスを、実験コードから分離するための設計メモである。

## 目的

- 学習・推論コードが Kaggle CLI や Web API の詳細に依存しない。
- Kaggle MCP が利用できる場合は MCP を優先する。
- MCP が未整備または不足している場合は、同じ interface の CLI adapter で代替する。
- 取得した Discussion / Notebook / Dataset 情報は要約して `aidlc-docs/` に残す。

## 境界

```text
app / research workflow
  -> KaggleGateway interface
      -> KaggleMcpAdapter
      -> KaggleCliAdapter
      -> ManualSnapshotAdapter
```

## 想定 Interface

| Method | 目的 | 出力 |
| --- | --- | --- |
| `list_competitions(search, page, sort_by)` | 技術テーマに近い competition の検索 | competition list snapshot |
| `get_competition_overview(slug)` | title、description、rules / evaluation / source links の取得 | 正規化された metadata |
| `list_files(slug)` | competition file の一覧取得 | size 付き file list |
| `download_competition(slug, output_dir)` | raw data download | local paths |
| `list_discussions(slug, sort, limit)` | recent / hot / votes / comments 順の topics 取得 | topic summaries と refs |
| `get_discussion(topic_ref)` | topic body と comments の取得 | markdown / text snapshot |
| `list_notebooks(query, slug, limit)` | 関連 notebook の検索 | notebook refs と metadata |
| `pull_notebook(ref, output_dir)` | notebook source の取得 | local paths |
| `list_datasets(search, page)` | 技術テーマに近い dataset の検索 | dataset list snapshot |
| `download_dataset(dataset_ref, output_dir)` | external dataset download | local paths |
| `list_submissions(slug)` | submission history の取得 | scores と timestamps |

## MCP 要件

Kaggle MCP server を実装する場合、まず以下の tools を優先する。

1. `kaggle_cli_version`
2. `kaggle_competitions_list`
3. `kaggle_competition_overview`
4. `kaggle_competition_files`
5. `kaggle_competition_download`
6. `kaggle_discussions_list`
7. `kaggle_discussion_get`
8. `kaggle_notebooks_search`
9. `kaggle_notebook_pull`
10. `kaggle_datasets_list`
11. `kaggle_dataset_download`
12. `kaggle_submissions_list`

各 tool は structured JSON と source reference を返す。agent は取得内容を短く要約して関連する `aidlc-docs/inception/*.md` に残し、tool call または command を `aidlc-docs/audit.md` に記録する。

## CLI fallback

MCP が使えない場合は、adapter の内側で Kaggle CLI を使う。CLI を使う前に以下を実行して記録する。

```bash
uv run kaggle --version
uv run kaggle --help
```

その後、必要に応じて以下のような command を使う。

```bash
uv run kaggle competitions files -c <competition-slug>
uv run kaggle competitions download -c <competition-slug> -p data/raw/<competition-slug>
uv run kaggle competitions topics list <competition-slug> -s hot
uv run kaggle competitions topics show <topic-ref>
uv run kaggle kernels list --search "<query>"
uv run kaggle datasets list -s "<query>"
```

## やらないこと

- training code から Kaggle CLI を直接呼ばない。
- feature code から Discussion / Notebook metadata を読まない。
- experiment tracking を Kaggle access が online であることに依存させない。

## 未決定事項

| 決定事項 | 回答 |
| --- | --- |
| MCP server の package / location | TBD |
| 認証情報の取得元 | TBD |
| cache directory | TBD |
| rate limit / retry policy | TBD |
| snapshot retention policy | TBD |
