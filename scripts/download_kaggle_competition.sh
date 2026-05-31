#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <competition-slug>" >&2
  exit 1
fi

COMPETITION="$1"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="${ROOT_DIR}/data/raw/${COMPETITION}"

if ! command -v kaggle >/dev/null 2>&1; then
  echo "kaggle CLI is not installed or not on PATH." >&2
  exit 1
fi

echo "Kaggle CLI:"
kaggle --version

mkdir -p "${TARGET_DIR}"

echo "Listing files for competition: ${COMPETITION}"
kaggle competitions files -c "${COMPETITION}"

echo "Downloading to: ${TARGET_DIR}"
kaggle competitions download -c "${COMPETITION}" -p "${TARGET_DIR}"

zip_file="${TARGET_DIR}/${COMPETITION}.zip"
if [[ -f "${zip_file}" ]]; then
  echo "Unzipping: ${zip_file}"
  unzip -n "${zip_file}" -d "${TARGET_DIR}"
fi

echo "Done. Data directory: ${TARGET_DIR}"

