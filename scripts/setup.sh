#!/bin/bash
# 클라우드 환경 설정 스크립트 — 저장소 루트에서 실행된다고 가정
set -e

cd "$(dirname "$0")/.."

# Python 의존성
if [ -f requirements.txt ]; then
  pip install -r requirements.txt --break-system-packages 2>/dev/null \
    || pip install -r requirements.txt
fi

# Node.js 의존성 (나중에 추가될 경우 대비)
if [ -f package-lock.json ]; then
  npm ci
elif [ -f package.json ]; then
  npm install
fi

echo "✅ setup 완료"
