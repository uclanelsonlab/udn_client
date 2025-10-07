#!/bin/bash

# Docker build script for UDN Gateway Client
# This script builds and optionally pushes the Docker image

set -e

# Configuration
IMAGE_NAME="udn-gateway-client"
VERSION="2.1.0"
REGISTRY=""
TAG="${REGISTRY}${IMAGE_NAME}:${VERSION}"
LATEST_TAG="${REGISTRY}${IMAGE_NAME}:latest"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    cat << EOF
Docker Build Script for UDN Gateway Client
=========================================

Usage: $0 [OPTIONS]

Options:
    --build           Build the Docker image
    --push            Push the image to registry
    --test            Test the built image
    --clean           Clean up build artifacts
    --registry <url>  Set Docker registry URL
    --version <ver>   Set image version (default: $VERSION)
    --help            Show this help message

Examples:
    # Build the image
    $0 --build
    
    # Build and push to registry
    $0 --build --push --registry your-registry.com/
    
    # Test the image
    $0 --test
    
    # Clean up
    $0 --clean

EOF
}

# Parse command line arguments
BUILD=false
PUSH=false
TEST=false
CLEAN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --build)
            BUILD=true
            shift
            ;;
        --push)
            PUSH=true
            shift
            ;;
        --test)
            TEST=true
            shift
            ;;
        --clean)
            CLEAN=true
            shift
            ;;
        --registry)
            REGISTRY="$2/"
            TAG="${REGISTRY}${IMAGE_NAME}:${VERSION}"
            LATEST_TAG="${REGISTRY}${IMAGE_NAME}:latest"
            shift 2
            ;;
        --version)
            VERSION="$2"
            TAG="${REGISTRY}${IMAGE_NAME}:${VERSION}"
            shift 2
            ;;
        --help)
            show_usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed or not in PATH"
    exit 1
fi

# Build the image
if [ "$BUILD" = true ]; then
    print_status "Building Docker image: $TAG"
    
    # Check if Dockerfile exists
    if [ ! -f "container/Dockerfile" ]; then
        print_error "Dockerfile not found in container/ directory"
        exit 1
    fi
    
    # Build the image from the container directory
    docker build -t "$TAG" -t "$LATEST_TAG" -f container/Dockerfile .
    
    if [ $? -eq 0 ]; then
        print_success "Docker image built successfully: $TAG"
    else
        print_error "Failed to build Docker image"
        exit 1
    fi
fi

# Test the image
if [ "$TEST" = true ]; then
    print_status "Testing Docker image: $TAG"
    
    # Test basic functionality
    docker run --rm "$TAG" python udn_gateway_cli.py --help
    
    if [ $? -eq 0 ]; then
        print_success "Docker image test passed"
    else
        print_error "Docker image test failed"
        exit 1
    fi
    
    # Test with a sample command
    print_status "Testing CLI functionality..."
    docker run --rm "$TAG" python -c "from udn_gateway import UDNGatewayClient; print('Import successful')"
    
    if [ $? -eq 0 ]; then
        print_success "CLI functionality test passed"
    else
        print_error "CLI functionality test failed"
        exit 1
    fi
fi

# Push the image
if [ "$PUSH" = true ]; then
    if [ -z "$REGISTRY" ]; then
        print_warning "No registry specified. Pushing to Docker Hub."
        print_warning "Make sure you're logged in: docker login"
    fi
    
    print_status "Pushing Docker image: $TAG"
    docker push "$TAG"
    
    if [ $? -eq 0 ]; then
        print_success "Docker image pushed successfully: $TAG"
    else
        print_error "Failed to push Docker image"
        exit 1
    fi
    
    # Also push latest tag
    print_status "Pushing latest tag: $LATEST_TAG"
    docker push "$LATEST_TAG"
    
    if [ $? -eq 0 ]; then
        print_success "Latest tag pushed successfully: $LATEST_TAG"
    else
        print_error "Failed to push latest tag"
        exit 1
    fi
fi

# Clean up
if [ "$CLEAN" = true ]; then
    print_status "Cleaning up Docker build artifacts..."
    
    # Remove dangling images
    docker image prune -f
    
    # Remove unused containers
    docker container prune -f
    
    print_success "Cleanup completed"
fi

# Show image information
if [ "$BUILD" = true ] || [ "$TEST" = true ]; then
    print_status "Docker image information:"
    docker images | grep "$IMAGE_NAME" || print_warning "No images found with name: $IMAGE_NAME"
fi

print_success "Script completed successfully!"
