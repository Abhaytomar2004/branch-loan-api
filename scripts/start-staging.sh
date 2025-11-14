#!/bin/bash
echo "🚀 Starting Staging Environment..."
export ENV_FILE=env.staging
docker compose down
docker compose up --build
