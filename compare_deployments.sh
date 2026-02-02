#!/bin/bash

CLOUD_RUN_URL="https://fastapi-ml-service-271681543917.us-central1.run.app"
FUNCTION_URL="https://us-central1-mlops-krutika-feb2024.cloudfunctions.net/predict-ml"

echo "=========================================="
echo "Cloud Run vs Cloud Functions Comparison"
echo "=========================================="
echo ""

echo "Testing Cloud Run (Warm)..."
for i in {1..5}; do
  curl -s -w "Request $i: %{time_total}s\n" -o /dev/null \
    -X POST "$CLOUD_RUN_URL/predict" \
    -H "Content-Type: application/json" \
    -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
done

echo ""
echo "Testing Cloud Function (Warm)..."
for i in {1..5}; do
  curl -s -w "Request $i: %{time_total}s\n" -o /dev/null \
    -X POST "$FUNCTION_URL" \
    -H "Content-Type: application/json" \
    -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
done

echo ""
echo "=========================================="
echo "Test Complete!"
echo "=========================================="
