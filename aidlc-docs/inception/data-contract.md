# Data Contract

## Maintenance Inputs

- 対象: local repository 文書・コード、空の seed、公式資料、CLI help。
- 外部のコンペデータや個人・業務データは使わない。
- 案件記録は seed と独立。reset は local backup を先に作る。
- 欠落補充は既存ファイルを変更しない。fresh project は独自ファイルを含めて backup へ移す。

## Smoke Dataset

- `data.mode=synthetic`、sklearn.make_classification、1,000 rows × 20 numeric features。
- Seed 42、target は binary label 0 / 1、row ID は 0〜999。
- Fingerprint: `e32beae901edd99eb707cab4eb3d42acd6194d56142653c3b2b61162a3777413`。
- 同じ generator と環境の確認用。業務上の代表性を持つ dataset ではない。

## CSV / Output Contract of the Demo

- CSV mode は train_file / target を必須にし、指定ファイル欠落で停止する。
- 空・重複列名、target の欠損・非有限値、ID の欠損・重複を検査する。
- ID は文字列として読み、先頭ゼロを保全。特徴の欠損は fold 内で補完、未知 category は許容する。
- Test の必要特徴列を検査。target / ID 以外を特徴とするため、案件では利用可能時点と除外列を先に確定する。
- 提出は sample submission と ID、1予測列を必須とし、test ID と sample ID の集合・件数を照合して整列する。
- Label / binary probability を明示し、NaN / inf と probability の範囲を検査する。
- 出力は一意の `outputs/runs/<local_run_id>/`。今回の synthetic smoke は submission を作らない。

## Leakage / Scope

Imputation / encoding は sklearn Pipeline 内で各 train fold に fit する。
付属例は小規模 tabular classification。Group / time split、regression、複数列出力等は案件契約に合わせて実装する。
重複 entity や時系列への適用可否を、今回の smoke で実証したとは扱わない。
