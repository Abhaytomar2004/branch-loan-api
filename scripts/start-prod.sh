#!/bin/bash
echo "🚀 Starting Production Environment..."
export ENV_FILE=env.production  
docker compose down
docker compose up --build
