#!/bin/bash
set -e
PROJECT_ID=$(gcloud config get project)
REGION="us-central1"
SERVICE_NAME="zoo-tour-agent"
IMAGE="gcr.io/$PROJECT_ID/$SERVICE_NAME"
echo "Deploying Zoo Tour Guide Agent..."
gcloud builds submit . --tag "$IMAGE" --project "$PROJECT_ID"
gcloud run deploy "$SERVICE_NAME" --image "$IMAGE" --platform managed --region "$REGION" --allow-unauthenticated --port 8080 --memory 1Gi --set-env-vars "ZOO_MCP_URL=$ZOO_MCP_URL,GOOGLE_GENAI_USE_VERTEXAI=1,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$REGION" --project "$PROJECT_ID"
AGENT_URL=$(gcloud run services describe "$SERVICE_NAME" --region "$REGION" --project "$PROJECT_ID" --format "value(status.url)")
echo "Agent deployed: $AGENT_URL"
