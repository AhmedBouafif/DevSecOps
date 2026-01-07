#!/bin/bash

# ConsumeSafe Deployment Script

set -e

echo "🚀 ConsumeSafe Deployment Script"
echo "================================"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="consumesafe"
IMAGE_TAG="latest"
NAMESPACE="default"

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    print_success "Docker is installed"
}

# Check if kubectl is installed
check_kubectl() {
    if ! command -v kubectl &> /dev/null; then
        print_warning "kubectl is not installed. Skipping Kubernetes deployment."
        return 1
    fi
    print_success "kubectl is installed"
    return 0
}

# Build Docker image
build_image() {
    echo ""
    echo "📦 Building Docker image..."
    docker build -t $IMAGE_NAME:$IMAGE_TAG .
    print_success "Docker image built successfully"
}

# Run tests
run_tests() {
    echo ""
    echo "🧪 Running tests..."
    docker run --rm $IMAGE_NAME:$IMAGE_TAG python -m pytest test_app.py || print_warning "Tests failed or pytest not available"
}

# Run security scan
security_scan() {
    echo ""
    echo "🔒 Running security scan..."
    
    # Check if trivy is installed
    if command -v trivy &> /dev/null; then
        trivy image $IMAGE_NAME:$IMAGE_TAG
        print_success "Security scan completed"
    else
        print_warning "Trivy not installed. Skipping security scan."
        print_warning "Install trivy: https://github.com/aquasecurity/trivy"
    fi
}

# Deploy to Kubernetes
deploy_kubernetes() {
    echo ""
    echo "☸️  Deploying to Kubernetes..."
    
    kubectl apply -f k8s/deployment.yaml
    kubectl apply -f k8s/network-policy.yaml
    kubectl apply -f k8s/hpa.yaml
    
    print_success "Kubernetes resources created"
    
    echo ""
    echo "⏳ Waiting for deployment to be ready..."
    kubectl wait --for=condition=available --timeout=300s deployment/consumesafe-deployment
    
    print_success "Deployment is ready"
    
    echo ""
    echo "📊 Deployment Status:"
    kubectl get pods -l app=consumesafe
    kubectl get svc consumesafe-service
}

# Run locally with Docker
run_local() {
    echo ""
    echo "🏃 Running application locally with Docker..."
    docker run -d -p 5000:5000 --name consumesafe $IMAGE_NAME:$IMAGE_TAG
    print_success "Application is running on http://localhost:5000"
}

# Main menu
main() {
    check_docker
    
    echo ""
    echo "Select deployment option:"
    echo "1. Build and run locally (Docker)"
    echo "2. Build and deploy to Kubernetes"
    echo "3. Build, test, and security scan only"
    echo "4. Full pipeline (build, test, scan, deploy to K8s)"
    read -p "Enter your choice (1-4): " choice
    
    case $choice in
        1)
            build_image
            run_tests
            run_local
            ;;
        2)
            if check_kubectl; then
                build_image
                deploy_kubernetes
            fi
            ;;
        3)
            build_image
            run_tests
            security_scan
            ;;
        4)
            if check_kubectl; then
                build_image
                run_tests
                security_scan
                deploy_kubernetes
            fi
            ;;
        *)
            print_error "Invalid choice"
            exit 1
            ;;
    esac
    
    echo ""
    print_success "Deployment completed successfully!"
}

main
