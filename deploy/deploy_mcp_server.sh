#!/bin/bash
set -e
PROJECT_ID=$(gcloud config get project)
REGION="us-central1"
SERVICE_NAME="zoo-mcp-server"
IMAGE="gcr.io/$PROJECT_ID/$SERVICE_NAME"
echo "Deploying Zoo MCP Server..."
gcloud builds submit . --tag "$IMAGE" --project "$PROJECT_ID"
gcloud run deploy "$SERVICE_NAME" --image "$IMAGE" --platform managed --region "$REGION" --allow-unauthenticated --port 8080 --memory 512Mi --project "$PROJECT_ID"
MCP_URL=$(gcloud run services describe "$SERVICE_NAME" --region "$REGION" --project "$PROJECT_ID" --format "value(status.url)")
echo "MCP Server deployed: $MCP_URL"
echo "MCP endpoint: $MCP_URL/mcp"
