# NDT Speedtest Exporter

M-Lab NDT speedtest exporter for Prometheus monitoring.

## Cross-Platform Development

### Local Development (M1 Mac ARM64)

```bash
# Start development environment
./dev.sh up

# View logs
./dev.sh logs

# Stop environment  
./dev.sh down

# Build and test locally
./dev.sh build
./dev.sh test
```

### Production Deployment (AMD64 Linux)

```bash
# Build optimized images (default: ~120MB)
./build.sh latest

# Build ultra-minimal images (~50MB)
./build.sh latest Dockerfile.minimal

# Build original version (~400MB)  
./build.sh latest Dockerfile

# Deploy to production host
./ndt-exporter.sh
```

## Architecture

- **Base**: Multi-stage build (golang:alpine + python:alpine)
- **Size**: 120MB optimized, 50MB minimal (vs 400MB original)  
- **Binary**: ndt7-client cross-compiled for target platform
- **Metrics**: Exposed on port 9140 at `/metrics`
- **Interval**: Default 300s, configurable via `-i`
- **Security**: Non-root user, distroless option available

## Development Workflow

1. Edit code locally on M1 Mac
2. Test with `./dev.sh up` (builds ARM64 for local testing)
3. Build production images with `./build.sh` (creates AMD64 + ARM64)
4. Deploy with existing `ndt-exporter.sh` script

## CI/CD

Automated builds via GitHub Actions:
- **Main branch pushes**: Auto-build and push `latest` tag to DockerHub
- **Git tags (v*)**: Auto-build and push versioned releases
- **Pull requests**: Build validation without publishing

Setup: See [CI Setup Guide](.github/SETUP-CI.md) for DockerHub integration.

## Metrics

- `ndt_speedtest{name="ping"}`: Round-trip time in ms
- `ndt_speedtest{name="download"}`: Download speed in Mbps  
- `ndt_speedtest{name="upload"}`: Upload speed in Mbps
- `ndt_speedtest{name="retrans"}`: Retransmissions count
