# ConsumeSafe 🇹🇳

A web application to check if products are on boycott lists and suggest Tunisian alternatives.

## Features

- ✅ Check products against boycott database
- 🇹🇳 Suggest Tunisian alternative products
- 🔒 Security hardened with multiple layers
- 🐳 Containerized with Docker
- ☸️ Kubernetes-ready deployment
- 🚀 CI/CD pipeline with GitHub Actions
- 🛡️ Automated security scanning

## Technology Stack

- **Backend**: Python 3.11 + Flask
- **Security**: Flask-Limiter, Flask-Talisman
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **CI/CD**: GitHub Actions
- **Security Scanning**: Bandit, Safety, Trivy

## Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone <repository-url>
cd "projet devsecops"
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Access the application**
Open your browser and navigate to: `http://localhost:5000`

### Docker

1. **Build the image**
```bash
docker build -t consumesafe .
```

2. **Run the container**
```bash
docker run -p 5000:5000 consumesafe
```

Or use Docker Compose:
```bash
docker-compose up
```

### Kubernetes Deployment

1. **Build and tag the image**
```bash
docker build -t consumesafe:latest .
```

2. **Deploy to Kubernetes**
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/network-policy.yaml
kubectl apply -f k8s/hpa.yaml
```

3. **Check deployment status**
```bash
kubectl get pods
kubectl get services
```

4. **Access the application**
```bash
kubectl get svc consumesafe-service
# Use the EXTERNAL-IP to access the app
```

## Project Structure

```
projet devsecops/
├── .github/
│   └── workflows/
│       └── ci-cd.yaml          # CI/CD pipeline
├── k8s/
│   ├── deployment.yaml         # K8s deployment & service
│   ├── network-policy.yaml     # Network security policies
│   └── hpa.yaml                # Horizontal Pod Autoscaler
├── templates/
│   └── index.html              # Frontend UI
├── app.py                      # Flask application
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Docker Compose configuration
├── test_app.py                 # Unit tests
├── SECURITY.md                 # Security documentation
├── .gitignore                  # Git ignore rules
├── .dockerignore               # Docker ignore rules
└── README.md                   # This file
```

## Security Features

### Application Level
- Rate limiting to prevent abuse
- Security headers (CSP, HSTS, etc.)
- Input validation and sanitization
- Non-root user execution

### Container Level
- Minimal base image (Python slim)
- Non-root user (UID 1000)
- Health checks
- Read-only filesystem where possible

### Kubernetes Level
- Pod security context
- Network policies
- Resource limits
- Liveness and readiness probes
- Horizontal Pod Autoscaler

### CI/CD Level
- Automated security scanning (Bandit, Safety, Trivy)
- Vulnerability detection
- Code quality checks
- Container image scanning

See [SECURITY.md](SECURITY.md) for detailed security documentation.

## Testing

Run the test suite:
```bash
pip install pytest pytest-cov
pytest --cov=app --cov-report=html
```

View coverage report:
```bash
# Open htmlcov/index.html in your browser
```

## CI/CD Pipeline

The GitHub Actions pipeline includes:

1. **Security Scanning**
   - Bandit for Python code security
   - Safety for dependency vulnerabilities

2. **Testing**
   - Unit tests with pytest
   - Code coverage reporting

3. **Build**
   - Docker image creation
   - Trivy vulnerability scanning

4. **Deploy** (on main branch)
   - Automated Kubernetes deployment
   - Rollout status verification

## API Endpoints

### `GET /`
Returns the main HTML page

### `POST /check-product`
Check if a product is on the boycott list

**Request:**
```json
{
  "product_name": "Coca-Cola"
}
```

**Response:**
```json
{
  "is_boycott": true,
  "product": {
    "name": "Coca-Cola",
    "brand": "Coca-Cola Company",
    "category": "Beverages"
  },
  "message": "⚠️ Coca-Cola is on the boycott list!",
  "alternatives": [
    {
      "name": "Boga",
      "description": "Tunisian soft drink brand, various flavors"
    }
  ]
}
```

### `GET /health`
Health check endpoint for monitoring

**Response:**
```json
{
  "status": "healthy"
}
```

## Customization

### Adding Products to Boycott List

Edit `BOYCOTT_LIST` in [app.py](app.py):
```python
BOYCOTT_LIST = [
    {"name": "Product Name", "brand": "Brand Name", "category": "Category"},
    # Add more products...
]
```

### Adding Tunisian Alternatives

Edit `TUNISIAN_ALTERNATIVES` in [app.py](app.py):
```python
TUNISIAN_ALTERNATIVES = {
    "Category": [
        {"name": "Product", "description": "Description"},
        # Add more alternatives...
    ]
}
```

## Monitoring

Access Kubernetes metrics:
```bash
# Get pod metrics
kubectl top pods

# Get deployment status
kubectl get deployment consumesafe-deployment

# Check HPA status
kubectl get hpa
```

## Troubleshooting

### Container won't start
```bash
# Check container logs
docker logs <container-id>

# Or in Kubernetes
kubectl logs <pod-name>
```

### Port already in use
```bash
# Change port in docker run command
docker run -p 8080:5000 consumesafe

# Or update PORT environment variable
docker run -e PORT=8080 -p 8080:8080 consumesafe
```

### Kubernetes deployment fails
```bash
# Check pod status
kubectl describe pod <pod-name>

# Check events
kubectl get events --sort-by='.lastTimestamp'
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and security scans
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions, please open an issue in the GitHub repository.

## Acknowledgments

- Built with Flask web framework
- Secured with industry-standard practices
- Deployed on Kubernetes for scalability
- Tunisian alternatives data sourced from local knowledge

---

**Made with ❤️ for Tunisia 🇹🇳**
