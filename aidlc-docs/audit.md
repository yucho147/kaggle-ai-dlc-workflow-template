# Audit Log

外部情報の取得、判断、仮定、実行の証跡を時系列で記録する。

### 2026-06-05 15:40 JST

- Actor: Codex
- Action: Codex 向け repository skills / project-scoped MCP configuration の公式仕様を確認した。
- Command / Source: OpenAI Developer Docs MCP (`https://developers.openai.com/codex/skills`, `https://developers.openai.com/codex/mcp`, `https://developers.openai.com/codex/config-basic`)
- Result: Repository skills は `.agents/skills/`、project-scoped MCP configuration は trusted project の `.codex/config.toml` が公式対応配置であることを確認した。
- Decision: Skills は既存 `.agents/skills/` を共通の正本とし、Codex 用には `.codex/config.toml` だけを追加する。
- Assumption: Codex はリポジトリルートから起動し、プロジェクトを trust して利用する。

### 2026-06-05 16:20 JST

- Actor: Codex
- Action: MCP server の起動失敗を再現し、Codex の project-scoped MCP 設定を精査した。
- Command / Source: `codex mcp list`; `uv run --group mcp ...`; `uvx arxiv-mcp-server`; OpenAI Developer Docs MCP (`https://developers.openai.com/codex/config-reference#configtoml`)
- Result: sandbox 内では既定の `~/.cache/uv` と `~/.local/share/uv/tools` が書き込み不可だった。また Kaggle / arXiv server の初期化は検証環境で約 17 秒かかり、Codex の既定 startup timeout 10 秒を超えた。書き込み可能な project-local directory を指定後、両 server で MCP initialize と tools/list が成功した。
- Decision: `.codex/config.toml` に `cwd`、`UV_CACHE_DIR`、`UV_TOOL_DIR`、startup/tool timeout を設定し、`.mcp.json` にも同じ directory 方針を反映する。
- Assumption: MCP client はリポジトリルートから project configuration を読み込む。

### 2026-06-05 16:40 JST

- Actor: User / Codex
- Action: Codex 対応の動作確認結果をドキュメントへ反映した。
- Command / Source: User confirmation; `git diff`; `UV_CACHE_DIR=.cache/uv uv run scripts/init_aidlc_docs.sh --check`
- Result: Codex で repository skills と3つの MCP server が正常に利用できることを確認した。README、Quickstart、Agent Execution Guide に Codex 対応と確認手順を明記した。
- Decision: OpenAI Codex を本テンプレートの対応 Coding Agent として明示する。
- Assumption: 動作確認日は 2026-06-05、プロジェクトを trust した Codex 環境を対象とする。

### 2026-10-04 10:42 JST — テンプレート改訂開始

- Actor: User / Codex
- Action: 全 tracked files、project concept、AI-DLC docs、スキル、scripts、baseline、client configs をレビュー。
- Source / commands: `rg --files --hidden`、`git status --short`、`git log -5`、各文書とコードの読み込み。`RTK.md` は repository に存在せず、ユーザーの参照に対応する `/Users/yuyakaneta/.claude/RTK.md` を確認。
- 外部取得: `web.run search_query/open` による Kaggle CLI 公式 repository / references、AWS adaptive AI-DLC blog、uv dependency groups、MLflow tracking、Claude MCP docs。OpenAI Docs MCP `search_openai_docs` / `fetch_openai_doc` による Codex MCP と skills の公式文書。
- URLs: https://github.com/Kaggle/kaggle-cli ; https://github.com/Kaggle/kaggle-cli/blob/main/skills/references/competitions.md ; https://aws.amazon.com/blogs/devops/open-sourcing-adaptive-workflows-for-ai-driven-development-life-cycle-ai-dlc/ ; https://docs.astral.sh/uv/concepts/projects/dependencies/ ; https://mlflow.org/docs/latest/ml/tracking/quickstart/ ; https://code.claude.com/docs/en/mcp ; https://developers.openai.com/codex/mcp ; https://developers.openai.com/codex/skills
- Commands: `UV_CACHE_DIR=.cache/uv uv run --locked kaggle --version` / `--help`、`competitions topics show/list --help`、`competitions download/files/submissions --help`、`kernels list --help`。
- Result: installed Kaggle 2.2.0。competition files/download/submissions は positional、download に `--unzip` はなく、topics sort は hot/top/new/recent/active/relevance。既存 MCP と docs の flags が実機と不一致。`topics show slug/id` と two-arg form は実機で共に対応。
- Decision: 現在の help と公式資料を区別し、未取得内容を推測しない。seed と案件記録の完全一致 CI を廃止。調査予算・評価契約・PoC 判断・明示的 synthetic mode・記録保全を追加する。
- Assumption: 今回はテンプレート保守であり、新しいコンペ参加ではない。既存 Python 3.13 と Hydra/loguru/MLflow は維持。軽微な設計は上記 construction docs に記録して進める。

### 2026-10-04 12:08 JST — 改訂と local validation

- Actor: Codex、ユーザーの詳細レビュー・改訂依頼に基づく。
- Decision: 27 seed と現在の保守記録を分離。用途別 gates、source / data / evaluation / PoC judgment、backup 付き初期化、共有 CLI 境界、fold / ID 契約、run manifest、HTML と CI を改訂。
- Authorization: workspace の .agents / .codex が書込保護対象だったため、作成済み4 skills / Codex config を staging script にまとめ、sandbox 外実行の許可を取得して適用。再承認や外部公開は行っていない。
- Dependencies / commands: `UV_CACHE_DIR=.cache/uv uv lock`、`uv lock --upgrade-package kaggle --upgrade-package kagglesdk`、`uv sync --locked --group research --group mcp`。Kaggle 2.2.4、kagglesdk 0.1.37、mcp 1.27.2、MLflow 3.12.0、markdown-it-py 4.2.0、sklearn 1.8.0、pandas 2.3.3。Yanked SDK 0.1.27 を更新。
- Additional sources / acquisition: `web.run open/search_query` で Copilot MCP / config、Kiro custom agent、Hugging Face Agents MCP、GitHub checkout / Astral setup-uv の公式文書を確認。URLs は [source-register](inception/source-register.md) src008〜src011。
- Access failures: 旧 docs URL は移動・取得失敗。GitHub git-ref REST URL は web tool でアクセスできず、`git ls-remote https://github.com/actions/checkout.git 'refs/tags/v7*'` と `git ls-remote https://github.com/astral-sh/setup-uv.git refs/tags/v10.1.0` を実行して確認した。
- CI decision: checkout v7.0.1 SHA 3d3c42e5aac5ba805825da76410c181273ba90b1、setup-uv v10.1.0 SHA bec219d24cd3e171d82865faccec33120bb574f4 を固定。contents:read、persist-credentials:false。
- Validation commands: `uv run --no-sync pytest -q`（最終66件成功）、`uv run --no-sync ruff check .`、`uv run --no-sync python scripts/check_template.py`、skill-creator quick_validate.py ×4、`bash -n`、CI YAML parse。実際の uv command は UV_CACHE_DIR=.cache/uv を指定。
- Actual protocol command: `uv run --no-sync python` の asyncio / mcp.ClientSession から local stdio server を起動し initialize / list_tools / call_tool(kaggle_cli_version) を実行。2026-10-04 11:56 JST、12 tools、version / help ok=true。認証付き API ではない。
- Baseline command: `uv run --locked --group research --group mcp python -m baseline.train`。2026-10-04 12:08 JST、local run 20261004T030812209639Z-ef8af264、MLflow run 2306cd91e5424639b9a4ba8358e39215、succeeded。Resolved config、fingerprints、metric、artifacts は operations/experiment-log.md に記録。
- Failures / assumptions: test process の model URI が別 tracker を参照したため明示 URI に修正。Boolean feature の dtype 問題を補正し regression を追加。Model requirements を明示し、Hydra log を loguru へ集約。Synthetic score は環境確認用。実コンペ・業務評価は対象外。
- Not run: client の対話起動、認証付き Kaggle API、GitHub-hosted Linux CI、cloud、別環境でのモデル依存再構築。

### 2026-10-04 12:24 JST — Report と引継ぎの確認

- Command: `UV_CACHE_DIR=.cache/uv uv run python scripts/render_improvement_report.py --title 'AI-DLC テンプレート改訂レビュー — 2026-10-04'`。生成 HTML は直接編集していない。
- Browser: IAB / browser connector は利用できず、native Chrome で確認。file URL は ERR_ACCESS_DENIED。`uv run --no-sync python -m http.server 8768 --bind 127.0.0.1 --directory outputs/reports` で report directory のみ一時配信。
- Result: Chrome に生成 HTML の本文・改訂表・引継ぎ手順が表示され、Technical Research の section link 移動を確認。Desktop の閲覧確認であり、全画面幅の実機検証ではない。
- Decision: state の G2 / G3 を complete とし、新規案件と既存案件の移行方法、認証・client・hosted CI の未検証範囲を明示して引き継ぐ。

### 2026-10-04 12:30 JST — 最終確認

- Result: 最終66 tests passed in 10.20s、Ruff check / format 成功、構造0 errors、initializer 27 files / 0 missing、git diff --check 成功。
- Report: 正本から最終版を再生成し、Chrome の表示で Status: complete と G3 complete の引継ぎを確認。
- Cleanup: 一時 localhost preview server を Ctrl+C で停止。検証で生成された default MLflow DB と Hydra log は outputs 配下へ保全し、追跡 DB の ignore を補充した。
- Handoff: 改訂内容、実行証跡、移行方法、未検証範囲を生成 HTML と共通 docs に保存。

### 2026-10-04 — 用語と説明のガードレール

- Request: 一般的ではない用語が増えて後から理解できない問題への対策。
- Decision: AGENTS.md に全用途共通のルールを設け、4 skills が参照する既存の入口から適用する。各 skill への重複コピーは不要と判断。
- Assumption: 独自語の禁止リストではなく、具体的な表現、初出の説明、必要な名称の定義・引継ぎ、報告前の確認で運用する。分野ごとに一般用語が異なるため、単語の自動検出は導入しない。
- Changes: docs/07_terminology.md、問題設定の用語表、実験名の記入指示、改善レビューの確認項目。現在の記録に既存の略語と呼称の意味を追加。
- Scope: 文書の変更。用語表は既存の Problem Overview セクション経由で HTML に表示する。
- Execution: `UV_CACHE_DIR=.cache/uv uv run --no-sync python scripts/render_improvement_report.py --title 'AI-DLC テンプレート改訂レビュー — 用語と説明のガードレール'`、exit code 0。生成 HTML は直接編集していない。
