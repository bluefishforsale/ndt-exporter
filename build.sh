#!/usr/bin/env bash

set -e

IMAGE="bluefishforsale/ndt-speedtest-exporter"
VERSION="${1:-latest}"

echo "Building multi-platform image: ${IMAGE}:${VERSION}"

# Create buildx builder if not exists
docker buildx create --name multiplatform --use --bootstrap 2>/dev/null || true

# Build for both platforms and push
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag "${IMAGE}:${VERSION}" \
  --push \
  .

echo "Successfully built and pushed: ${IMAGE}:${VERSION}"
