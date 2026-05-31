#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE_DIR="${ROOT_DIR}/templates/aidlc-docs"
TARGET_DIR="${ROOT_DIR}/aidlc-docs"

if [[ ! -d "${TEMPLATE_DIR}" ]]; then
  echo "Template directory not found: ${TEMPLATE_DIR}" >&2
  exit 1
fi

mkdir -p "${TARGET_DIR}"

find "${TEMPLATE_DIR}" -type d | while read -r dir; do
  rel="${dir#${TEMPLATE_DIR}}"
  mkdir -p "${TARGET_DIR}${rel}"
done

find "${TEMPLATE_DIR}" -type f | while read -r file; do
  rel="${file#${TEMPLATE_DIR}/}"
  target="${TARGET_DIR}/${rel}"

  if [[ -e "${target}" ]]; then
    echo "skip existing: ${target#${ROOT_DIR}/}"
  else
    cp "${file}" "${target}"
    echo "created: ${target#${ROOT_DIR}/}"
  fi
done

echo "aidlc-docs initialized at ${TARGET_DIR#${ROOT_DIR}/}"

