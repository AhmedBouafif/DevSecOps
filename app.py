from flask import Flask, render_template, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import os

app = Flask(__name__)

# Security: Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Security: HTTPS enforcement and security headers
Talisman(app, 
         force_https=False,  # Set to True in production
         strict_transport_security=True,
         content_security_policy={
             'default-src': "'self'",
             'style-src': ["'self'", "'unsafe-inline'"],
             'script-src': ["'self'", "'unsafe-inline'"],
             'img-src': ["'self'", "https://upload.wikimedia.org", "data:"]
         })

# Boycott list - products to avoid
BOYCOTT_LIST = [
    {"name": "Coca-Cola", "brand": "Coca-Cola Company", "category": "Beverages"},
    {"name": "Pepsi", "brand": "PepsiCo", "category": "Beverages"},
    {"name": "Nestle", "brand": "Nestle", "category": "Food"},
    {"name": "McDonald's", "brand": "McDonald's Corporation", "category": "Fast Food"},
    {"name": "Starbucks", "brand": "Starbucks Corporation", "category": "Coffee"},
    {"name": "KFC", "brand": "Yum! Brands", "category": "Fast Food"},
    {"name": "Burger King", "brand": "Restaurant Brands International", "category": "Fast Food"},
]

# Tunisian alternative products
TUNISIAN_ALTERNATIVES = {
    "Beverages": [
        {"name": "Boga", "description": "Tunisian soft drink brand, various flavors"},
        {"name": "Safia", "description": "Tunisian mineral water"},
        {"name": "Ain Garci", "description": "Tunisian natural mineral water"},
        {"name": "Melliti", "description": "Tunisian natural juice brand"}
    ],
    "Food": [
        {"name": "Délice", "description": "Tunisian dairy products"},
        {"name": "Vitalait", "description": "Tunisian dairy and food products"},
        {"name": "Carthage", "description": "Tunisian food products"}
    ],
    "Fast Food": [
        {"name": "Maison Zaytouna", "description": "Tunisian traditional food restaurant"},
        {"name": "El Mella", "description": "Local Tunisian fast food chain"},
        {"name": "Mlaoui Express", "description": "Tunisian traditional sandwiches"}
    ],
    "Coffee": [
        {"name": "Café Bon", "description": "Tunisian coffee brand"},
        {"name": "Boncolac Café", "description": "Tunisian coffee products"},
        {"name": "Al Mazraa", "description": "Tunisian coffee shops"}
    ]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check-product', methods=['POST'])
@limiter.limit("10 per minute")
def check_product():
    """Check if a product is on the boycott list"""
    try:
        data = request.get_json()
        product_name = data.get('product_name', '').strip().lower()
        
        if not product_name:
            return jsonify({'error': 'Product name is required'}), 400
        
        # Check if product is on boycott list
        is_boycott = False
        boycott_info = None
        
        for product in BOYCOTT_LIST:
            if product_name in product['name'].lower() or product_name in product['brand'].lower():
                is_boycott = True
                boycott_info = product
                break
        
        if is_boycott:
            # Get Tunisian alternatives for the category
            alternatives = TUNISIAN_ALTERNATIVES.get(boycott_info['category'], [])
            
            return jsonify({
                'is_boycott': True,
                'product': boycott_info,
                'message': f"⚠️ {boycott_info['name']} is on the boycott list!",
                'alternatives': alternatives
            })
        else:
            return jsonify({
                'is_boycott': False,
                'message': f"✓ '{product_name}' is not on the boycott list.",
                'alternatives': []
            })
    
    except Exception as e:
        app.logger.error(f"Error checking product: {str(e)}")
        return jsonify({'error': 'An error occurred processing your request'}), 500

@app.route('/health')
def health():
    """Health check endpoint for Kubernetes"""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    # Security: Don't run in debug mode in production
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
