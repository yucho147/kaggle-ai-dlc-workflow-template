# Source Register

取得日は全て **2026-10-04 JST**。資料の公開・更新日が確認できないものは unknown とした。
文書の参照・要約に利用し、外部 Notebook や解法コードは移植していない。

## Sources

| ID | Type / title | URL / ref | 公開・更新日 / revision | 取得範囲 |
| --- | --- | --- | --- | --- |
| src001 | 公式 AWS adaptive AI-DLC | [AWS blog](https://aws.amazon.com/blogs/devops/open-sourcing-adaptive-workflows-for-ai-driven-development-life-cycle-ai-dlc/) | 2025-11-29 | adaptive workflow の考え方 |
| src002 | 公式 Kaggle CLI | [Repository](https://github.com/Kaggle/kaggle-cli) / [competition reference](https://github.com/Kaggle/kaggle-cli/blob/main/skills/references/competitions.md) | main、更新日 unknown | 認証、CLI 使用法。installed 版とは区別 |
| src003 | Local CLI observed | Kaggle 2.2.0 → 2.2.4 の version / help、installed argparse parsers | kaggle 2.2.4 / kagglesdk 0.1.37 | competitions / topics / kernels / datasets の構文 |
| src004 | 公式 uv dependency groups | [Docs](https://docs.astral.sh/uv/concepts/projects/dependencies/) | 更新日 unknown | optional groups と依存の分離 |
| src005 | 公式 MLflow tracking | [Quickstart](https://mlflow.org/docs/latest/ml/tracking/quickstart/) | 更新日 unknown、実機 3.12.0 | local tracking / model / artifacts。実機でも検証 |
| src006 | 公式 Codex | [Skills](https://developers.openai.com/codex/skills) / [MCP](https://developers.openai.com/codex/mcp) | 更新日 unknown | project skills / trusted config / cwd / timeout |
| src007 | 公式 Claude Code MCP | [Docs](https://code.claude.com/docs/en/mcp) | 更新日 unknown | project .mcp.json / trust / environment |
| src008 | 公式 Copilot CLI | [MCP 手順](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-mcp-servers) / [Config reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference) | 更新日 unknown | project .mcp.json と trusted folder |
| src009 | 公式 Kiro custom agent | [Configuration reference](https://kiro.dev/docs/custom-agents/configuration-reference/) | CLI 3.0 文書、更新日 unknown | file / skill resources、includeMcpJson |
| src010 | 公式 Hugging Face MCP | [Agents MCP](https://huggingface.co/docs/hub/en/agents-mcp) | 更新日 unknown | optional source の公式案内先 |
| src011 | 公式 GitHub / Astral CI actions | [Checkout](https://github.com/actions/checkout) / [Setup uv](https://github.com/astral-sh/setup-uv) | checkout v7.0.1 / setup-uv v10.1.0 | README と git ls-remote でタグ・SHA を確認 |
| src012 | Repository observed | 改訂前 commit 1f23cf401b813dbeb634b5cab087f3fcd5c4194b、全 tracked files | local checkout、dirty 改訂 | 文書、初期化、CI、MCP、baseline、report |

## Claims

| Claim | 要約 | Source IDs | Evidence | 条件 / 判断 |
| --- | --- | --- | --- | --- |
| claim001 | 工程は依頼の目的・制約に合わせる | src001、src012 | reported / inferred | 3フェーズの独自テンプレートへ応用。公式 runtime の移植ではない |
| claim002 | competition の -c / --unzip、votes sort は実機と不一致 | src003 | observed | 2.2.4 help と parser を優先。main docs は将来変化する |
| claim003 | seed と案件記録の完全一致検査は派生運用を妨げる | src012、derived project test | observed | 存在・リンク・設定・実行契約の検査へ変更 |
| claim004 | MCP overview の一覧と URL は本文取得を証明しない | src012、MCP contract tests | observed | metadata_only を明示し、規約・本文は別に取得する |
| claim005 | model と MLflow / local manifest の対応を保存できる | src005、integration test | observed | 同じ tracking URI で model URI を解決。実行依存を明示 |
| claim006 | 各 client 設定の更新は公式説明に整合する | src006〜src009 | reported | 対話起動・trust・認証は未検証 |

## Coverage / Access Failures

- 特定コンペの winner 解法調査は対象外。Discussion、Notebook、Dataset の本文・データは取得していない。
- OpenAI は公式 Docs MCP の search / fetch、他の一次資料は web search / open で取得。CLI は help と installed parser、CI action のタグは git ls-remote で確認。
- 旧 Hugging Face / Kiro の文書 URL と旧 Copilot MCP URL に取得失敗・移動があり、上記の現行案内先へ修正。
- GitHub git-ref REST URL は web tool で取得できず、公開 HTTPS の git ls-remote でタグを確認した。
- 認証付き Kaggle API、private resource、client の対話起動、GitHub-hosted CI は未実行。local smoke の成功から推測しない。

操作・取得時刻・コマンドの詳細は audit に記録する。
