#!/usr/bin/env bash

set -e  # Exit immediately if a command fails

# ===== CONFIG =====
IMAGE_NAME="currency-convertor"
CONTAINER_NAME="currency-convertor-app"
PORT_MAPPING="8000:8000"
# ==================

echo "🔍 Checking for existing container..."

if docker ps -a --format '{{.Names}}' | grep -Eq "^${CONTAINER_NAME}\$"; then
  echo "🛑 Stopping container: ${CONTAINER_NAME}"
  docker stop "${CONTAINER_NAME}" || true

  echo "🗑️ Removing container: ${CONTAINER_NAME}"
  docker rm "${CONTAINER_NAME}"
fi

echo "🔍 Checking for existing image..."

if docker images --format '{{.Repository}}' | grep -Eq "^${IMAGE_NAME}\$"; then
  echo "🗑️ Removing image: ${IMAGE_NAME}"
  docker rmi "${IMAGE_NAME}"
fi

echo "🐳 Building new image: ${IMAGE_NAME}"
docker build -t "${IMAGE_NAME}" .

echo "🚀 Running new container: ${CONTAINER_NAME}"
docker run -d --rm \
  --name "${CONTAINER_NAME}" \
  -p ${PORT_MAPPING} \
  "${IMAGE_NAME}"

echo "✅ Done! Container is running."
