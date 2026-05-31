#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<EOF
Usage: $(basename "$0") [--force] [--check]

  (no flags)  Copy template files to aidlc-docs/. Skip files that already exist.
  --force     Overwrite existing files in aidlc-docs/ with template versions.
  --check     Report differences between templates/aidlc-docs/ and aidlc-docs/.
              Exits with code 1 if they differ. Does not modify any files.
EOF
  exit 1
}

FORCE=false
CHECK=false

for arg in "$@"; do
  case "$arg" in
    --force) FORCE=true ;;
    --check) CHECK=true ;;
    *) usage ;;
  esac
done

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE_DIR="${ROOT_DIR}/templates/aidlc-docs"
TARGET_DIR="${ROOT_DIR}/aidlc-docs"

if [[ ! -d "${TEMPLATE_DIR}" ]]; then
  echo "Template directory not found: ${TEMPLATE_DIR}" >&2
  exit 1
fi

if [[ "${CHECK}" == true ]]; then
  if diff -rq "${TEMPLATE_DIR}" "${TARGET_DIR}" > /dev/null 2>&1; then
    echo "OK: templates/aidlc-docs and aidlc-docs are identical."
    exit 0
  else
    echo "DIFF: templates/aidlc-docs and aidlc-docs differ:"
    diff -rq "${TEMPLATE_DIR}" "${TARGET_DIR}" || true
    exit 1
  fi
fi

mkdir -p "${TARGET_DIR}"

find "${TEMPLATE_DIR}" -type d | while read -r dir; do
  rel="${dir#${TEMPLATE_DIR}}"
  mkdir -p "${TARGET_DIR}${rel}"
done

find "${TEMPLATE_DIR}" -type f | while read -r file; do
  rel="${file#${TEMPLATE_DIR}/}"
  target="${TARGET_DIR}/${rel}"

  if [[ -e "${target}" ]] && [[ "${FORCE}" == false ]]; then
    echo "skip existing: ${target#${ROOT_DIR}/}"
  else
    cp "${file}" "${target}"
    if [[ "${FORCE}" == true ]] && [[ -e "${target}" ]]; then
      echo "overwritten: ${target#${ROOT_DIR}/}"
    else
      echo "created: ${target#${ROOT_DIR}/}"
    fi
  fi
done

echo "aidlc-docs initialized at ${TARGET_DIR#${ROOT_DIR}/}"

