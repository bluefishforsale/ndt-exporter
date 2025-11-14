#!/usr/bin/env bash

set -e

IMAGE="bluefishforsale/ndt-speedtest-exporter"
VERSION="${1:-latest}"
DOCKERFILE="${2:-Dockerfile.optimized}"

echo "Building multi-platform image: ${IMAGE}:${VERSION} using ${DOCKERFILE}"

# Show dockerfile options
if [[ "$1" == "help" ]]; then
  echo "Usage: $0 [VERSION] [DOCKERFILE]"
  echo "  VERSION: Image tag (default: latest)"
  echo "  DOCKERFILE options:"
  echo "    Dockerfile.optimized (default) - Alpine-based, ~120MB"
  echo "    Dockerfile.minimal  - Distroless, ~50MB"
  echo "    Dockerfile          - Original, ~400MB"
  exit 0
fi

# Create buildx builder if not exists
docker buildx create --name multiplatform --use --bootstrap 2>/dev/null || true

# Build for both platforms and push
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --file "${DOCKERFILE}" \
  --tag "${IMAGE}:${VERSION}" \
  --push \
  .

echo "Successfully built and pushed: ${IMAGE}:${VERSION} using ${DOCKERFILE}"
