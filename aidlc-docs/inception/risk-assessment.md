# Risk Assessment

| Risk | Evidence | Mitigation / result | Residual / revisit |
| --- | --- | --- | --- |
| 案件記録を seed で上書き | 旧 init / CI | missing-only、backup、new-project、派生編集 regression | backup は local。必要な記録は別に保全 |
| CLI / client 仕様が変わる | src002〜src011 | lock 更新、actual help / parser、設定整合 | dependency 更新時に再検証。対話起動は未検証 |
| Synthetic を実データ成果と誤認 | 旧 fallback | explicit mode、missing file error、provenance / tags | smoke score を業務・LB の根拠にしない |
| 前処理 leakage / 提出ずれ | 旧 baseline | fold 内 fit、OOF coverage、ID alignment | group / time / 複数予測列は別実装 |
| Archive の上書き / 資源消費 | download 境界 | path / symlink / duplicate / size / free disk 検査、既存 file 拒否 | 展開上限は既定5GiB。取得前にもサイズ確認。I/O 失敗で部分展開が残り得る |
| Metadata を本文として扱う | 旧 overview | metadata_only、ok / error / truncated、snapshot | 規約・解法・license は本文で確認 |
| Tracker / artifact の食い違い | integration test | 明示的 model dependencies、local / MLflow manifest 比較 | DB と artifact store を両方保全。別環境での再構築は未検証 |
| 文書だけ通り実装が壊れる | 旧完全一致 CI | lint / parser / protocol / end-to-end regression | GitHub-hosted CI 自体は未実行 |

ユーザーの依頼範囲内で改訂した。規約受諾、提出、外部公開、クラウド費用の発生は含めていない。
