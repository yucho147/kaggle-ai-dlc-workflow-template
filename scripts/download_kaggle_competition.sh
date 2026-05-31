#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <competition-slug>" >&2
  exit 1
fi

COMPETITION="$1"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="${ROOT_DIR}/data/raw/${COMPETITION}"

if command -v uv >/dev/null 2>&1; then
  KAGGLE_CMD=(uv run kaggle)
elif command -v kaggle >/dev/null 2>&1; then
  KAGGLE_CMD=(kaggle)
else
  echo "Neither uv nor kaggle CLI is available on PATH." >&2
  echo "Install uv and run: uv sync" >&2
  exit 1
fi

if ! command -v unzip >/dev/null 2>&1; then
  echo "unzip is required to extract Kaggle competition data." >&2
  exit 1
fi

echo "Kaggle CLI:"
"${KAGGLE_CMD[@]}" --version

mkdir -p "${TARGET_DIR}"

echo "Listing files for competition: ${COMPETITION}"
"${KAGGLE_CMD[@]}" competitions files -c "${COMPETITION}"

echo "Downloading to: ${TARGET_DIR}"
"${KAGGLE_CMD[@]}" competitions download -c "${COMPETITION}" -p "${TARGET_DIR}"

zip_file="${TARGET_DIR}/${COMPETITION}.zip"
if [[ -f "${zip_file}" ]]; then
  echo "Unzipping: ${zip_file}"
  unzip -n "${zip_file}" -d "${TARGET_DIR}"
fi

echo "Done. Data directory: ${TARGET_DIR}"
