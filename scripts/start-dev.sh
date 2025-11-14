#!/bin/bash
echo "🚀 Starting Development Environment..."
export ENV_FILE=env.development
docker compose down
docker compose up --build
