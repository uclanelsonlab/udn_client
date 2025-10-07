# Docker Usage Guide for UDN Gateway Client

This guide covers how to build, run, and use the UDN Gateway Client Docker image.

## Quick Start

### 1. Build the Docker Image

```bash
# Build the image
./bin/build_docker.sh --build

# Build and test the image
./bin/build_docker.sh --build --test

# Build, test, and push to registry
./bin/build_docker.sh --build --test --push --registry your-registry.com/
```

### 2. Run the Container

```bash
# Run with help
docker run --rm udn-gateway-client:latest

# Run with your API token
docker run --rm -v $(pwd)/token.txt:/app/token.txt udn-gateway-client:latest \
  python udn_gateway_cli.py -a token.txt -u UDN970218 --all

# Run interactively
docker run -it --rm -v $(pwd):/app udn-gateway-client:latest bash
```

### 3. Use with Docker Compose

```bash
# Start services (run from container directory)
cd container && docker-compose up -d

# Run pipeline
cd container && docker-compose exec nextflow nextflow run main.nf --api_token_file token.txt --udn_id UDN970218

# Interactive development
cd container && docker-compose exec udn-gateway-dev bash

# Stop services
cd container && docker-compose down
```

## Docker Image Details

### Image Specifications

- **Base Image**: Python 3.9-slim
- **Size**: ~200MB (optimized multi-stage build)
- **User**: Non-root user (udnuser) for security
- **Health Check**: Built-in health monitoring
- **Dependencies**: All Python packages pre-installed

### Image Contents

```
/app/
├── udn_gateway/              # Python package
├── udn_gateway_cli.py        # CLI script
├── main.nf                   # Nextflow pipeline
├── modules/                  # Nextflow modules
├── bin/                      # Utility scripts
├── results/                  # Output directory
├── logs/                     # Log directory
└── reports/                  # Reports directory
```

## Usage Examples

### 1. Basic CLI Usage

```bash
# Download all files for a participant
docker run --rm \
  -v $(pwd)/token.txt:/app/token.txt \
  -v $(pwd)/results:/app/results \
  udn-gateway-client:latest \
  python udn_gateway_cli.py -a token.txt -u UDN970218 --all

# Download only VCF files
docker run --rm \
  -v $(pwd)/token.txt:/app/token.txt \
  -v $(pwd)/results:/app/results \
  udn-gateway-client:latest \
  python udn_gateway_cli.py -a token.txt -u UDN970218 --download --vcf

# Get participant info only
docker run --rm \
  -v $(pwd)/token.txt:/app/token.txt \
  udn-gateway-client:latest \
  python udn_gateway_cli.py -a token.txt -u UDN970218 --info-only
```

### 2. Nextflow Pipeline Usage

```bash
# Run with Docker profile
docker run --rm \
  -v $(pwd):/workspace \
  -v /var/run/docker.sock:/var/run/docker.sock \
  nextflow/nextflow:22.10.0 \
  nextflow run main.nf --api_token_file token.txt --udn_id UDN970218 -profile docker

# Run with local Docker
nextflow run main.nf --api_token_file token.txt --udn_id UDN970218 -profile docker
```

### 3. Development Usage

```bash
# Interactive development
docker run -it --rm \
  -v $(pwd):/app \
  -v $(pwd)/results:/app/results \
  udn-gateway-client:latest bash

# Run tests
docker run --rm \
  -v $(pwd):/app \
  udn-gateway-client:latest \
  python -m pytest tests/

# Install additional packages
docker run --rm \
  -v $(pwd):/app \
  udn-gateway-client:latest \
  pip install additional-package
```

## Docker Compose Services

### Services Overview

1. **udn-gateway-client**: Main application container
2. **udn-gateway-dev**: Development container with interactive shell
3. **nextflow**: Nextflow pipeline execution container

### Service Configuration

```yaml
# Main service
udn-gateway-client:
  image: udn-gateway-client:latest
  volumes:
    - .:/app
    - ./results:/app/results
  environment:
    - PYTHONPATH=/app

# Development service
udn-gateway-dev:
  image: udn-gateway-client:latest
  command: ["bash"]
  stdin_open: true
  tty: true

# Nextflow service
nextflow:
  image: nextflow/nextflow:22.10.0
  volumes:
    - .:/workspace
    - /var/run/docker.sock:/var/run/docker.sock
```

## Registry Integration

### Push to Registry

```bash
# Push to Docker Hub
./bin/build_docker.sh --build --push --registry ""

# Push to private registry
./bin/build_docker.sh --build --push --registry "your-registry.com/"

# Push with specific version
./bin/build_docker.sh --build --push --version "2.1.0" --registry "your-registry.com/"
```

### Pull from Registry

```bash
# Pull from Docker Hub
docker pull udn-gateway-client:latest

# Pull from private registry
docker pull your-registry.com/udn-gateway-client:latest

# Use in Nextflow
nextflow run main.nf --api_token_file token.txt --udn_id UDN970218 -profile docker
```

## Security Considerations

### Non-Root User

The container runs as a non-root user (`udnuser`) for security:

```dockerfile
RUN useradd -m -u 1000 udnuser && \
    chown -R udnuser:udnuser /app
USER udnuser
```

### Volume Mounts

Always mount volumes with appropriate permissions:

```bash
# Correct volume mounting
docker run --rm \
  -v $(pwd)/token.txt:/app/token.txt:ro \
  -v $(pwd)/results:/app/results \
  udn-gateway-client:latest
```

### Health Checks

The container includes health checks:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python udn_gateway_cli.py --help > /dev/null || exit 1
```

## Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   # Fix volume permissions
   chmod 755 results/
   chmod 644 token.txt
   ```

2. **Container Not Found**
   ```bash
   # Build the image first
   ./bin/build_docker.sh --build
   ```

3. **Volume Mount Issues**
   ```bash
   # Use absolute paths
   docker run --rm \
     -v /absolute/path/to/token.txt:/app/token.txt \
     udn-gateway-client:latest
   ```

4. **Network Issues**
   ```bash
   # Check Docker daemon
   docker info
   
   # Restart Docker service
   sudo systemctl restart docker
   ```

### Debug Mode

```bash
# Run with debug output
docker run --rm \
  -v $(pwd)/token.txt:/app/token.txt \
  udn-gateway-client:latest \
  python udn_gateway_cli.py -a token.txt -u UDN970218 --verbose

# Check container logs
docker logs udn-gateway-client

# Inspect container
docker inspect udn-gateway-client
```

## Performance Optimization

### Resource Limits

```bash
# Set resource limits
docker run --rm \
  --memory="4g" \
  --cpus="2" \
  -v $(pwd)/token.txt:/app/token.txt \
  udn-gateway-client:latest
```

### Multi-Stage Build

The Dockerfile uses multi-stage builds for optimization:

```dockerfile
# Builder stage
FROM python:3.9-slim as builder
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.9-slim
COPY --from=builder /root/.local /root/.local
```

## Integration with CI/CD

### GitHub Actions

```yaml
name: Build and Push Docker Image
on:
  push:
    tags: ['v*']
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build Docker image
        run: ./bin/build_docker.sh --build --test --push
```

### GitLab CI

```yaml
build_image:
  stage: build
  script:
    - ./bin/build_docker.sh --build --test --push --registry $CI_REGISTRY/
```

## Best Practices

1. **Always use specific tags** in production
2. **Mount volumes read-only** when possible
3. **Use multi-stage builds** for smaller images
4. **Implement health checks** for monitoring
5. **Run as non-root user** for security
6. **Use .dockerignore** to exclude unnecessary files
7. **Regularly update base images** for security patches

## Support

For Docker-related issues:
- Check container logs: `docker logs <container_name>`
- Inspect container: `docker inspect <container_name>`
- Test image: `./bin/build_docker.sh --test`
- Clean up: `./bin/build_docker.sh --clean`
