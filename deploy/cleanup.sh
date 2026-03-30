#!/bin/bash
PROJECT_ID=$(gcloud config get project)
REGION="us-central1"
gcloud run services delete zoo-mcp-server --region "$REGION" --project "$PROJECT_ID" --quiet
gcloud run services delete zoo-tour-agent --region "$REGION" --project "$PROJECT_ID" --quiet
echo "Cleanup complete."
