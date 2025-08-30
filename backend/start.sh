#!/usr/bin/env bash
# Simple startup script for Render or other hosts
export PYTHONPATH=$(pwd)
uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1
