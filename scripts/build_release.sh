#!/usr/bin/env bash
set -euo pipefail

RELEASE_DIR="release"
ARCHIVE_NAME="farfor_release.tar.gz"

rm -rf "$RELEASE_DIR" "$ARCHIVE_NAME"
mkdir -p "$RELEASE_DIR"

rsync -av \
  --exclude '.git' \
  --exclude '.venv' \
  --exclude '__pycache__' \
  --exclude '*.pyc' \
  --exclude '.pytest_cache' \
  --exclude 'app/static/uploads/*' \
  ./ "$RELEASE_DIR/"

tar -czf "$ARCHIVE_NAME" -C "$RELEASE_DIR" .

echo "Release archive created: $ARCHIVE_NAME"
