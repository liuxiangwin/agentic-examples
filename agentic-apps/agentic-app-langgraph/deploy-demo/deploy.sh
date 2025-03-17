#!/bin/bash

# Prompt for user input
read -p "Enter API Key: " api_key
read -p "Enter API URL: " api_url
read -p "Enter Model Name: " model_name
read -p "Enter Namespace (default: agentic-demo): " namespace

# Default namespace if not provided
namespace=${namespace:-agentic-demo}

# Encode values in base64 for Kubernetes Secret
export API_KEY=$(echo -n "$api_key" | base64)
export API_URL=$(echo -n "$api_url" | base64)
export MODEL_NAME=$(echo -n "$model_name" | base64)

# Generate Secret file using envsubst
envsubst < deploy-demo/secret-patch.yaml.tmpl > deploy-demo/secret-patch.yaml
# Replace namespace in `kustomization.yaml` and `patch-crb.yaml`
sed -i "s/namespace: .*/namespace: ${namespace}/" deploy-demo/kustomization.yaml
sed -i "s/namespace: .*/namespace: ${namespace}/" deploy-demo/patch-crb.yaml