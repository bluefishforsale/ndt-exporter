#!/usr/bin/env bash

set -e

ACTION="${1:-up}"

case $ACTION in
  up)
    echo "Starting development environment..."
    docker-compose -f docker-compose.dev.yml up --build
    ;;
  down)
    echo "Stopping development environment..."
    docker-compose -f docker-compose.dev.yml down
    ;;
  logs)
    docker-compose -f docker-compose.dev.yml logs -f
    ;;
  build)
    echo "Building local image..."
    docker build --platform linux/arm64 -t ndt-test .
    ;;
  test)
    echo "Testing container locally..."
    docker run --rm -p 9140:9140 ndt-test
    ;;
  *)
    echo "Usage: $0 {up|down|logs|build|test}"
    exit 1
    ;;
esac
