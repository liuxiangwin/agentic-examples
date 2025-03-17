#!/bin/bash

# Prompt for user input
read -p "Enter API Key: " api_key
read -p "Enter API URL: " api_url
read -p "Enter Model Name: " model_name
read -p "Enter Namespace (default: agentic-demo): " namespace

# Default namespace if not provided
namespace=${namespace:-agentic-demo}

# Encode values in base64 (Kubernetes Secret requires base64 encoding)
export API_KEY=$(echo -n "$api_key" | base64)
export API_URL=$(echo -n "$api_url" | base64)
export MODEL_NAME=$(echo -n "$model_name" | base64)

# Ensure deploy-demo directory exists
mkdir -p deploy-demo

# Generate Secret file
cat <<EOF > deploy-demo/secret-patch.yaml
apiVersion: v1
kind: Secret
metadata:
  name: agentic-app-be-secret
data:
  API_KEY: "${API_KEY}"
  API_URL: "${API_URL}"
  MODEL_NAME: "${MODEL_NAME}"
EOF

echo "✅ Secret file 'deploy-demo/secret-patch.yaml' generated."

# Function to update namespace using sed
update_namespace() {
  local file=$1
  if [[ -f "$file" ]]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
      sed -i '' "s/namespace: [a-zA-Z0-9_-]*/namespace: ${namespace}/g" "$file"
    else
      sed -i "s/namespace: [a-zA-Z0-9_-]*/namespace: ${namespace}/g" "$file"
    fi
    echo "✅ Namespace updated in '$file'."
  else
    echo "⚠️ WARNING: '$file' not found. Skipping namespace update."
  fi
}

# Update namespace in required files
update_namespace "deploy-demo/kustomization.yaml"
update_namespace "deploy-demo/patch-crb.yaml"
