# E-Commerce Backend API

## Setup
1. Clone repo: `git clone [your-repo-url]`
2. Create virtual env: `python -m venv venv`
3. Activate: `.\venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run: `uvicorn app.main:app --reload`

## API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /token` - Get JWT token

### Products
- `GET /products/` - List all products
- `POST /products/` - Add product (Admin only)

### Cart
- `GET /cart/` - View cart
- `POST /cart/items` - Add to cart

### Orders
- `POST /orders/` - Place order

## Sample Requests

```bash
# Register user
curl -X POST -H "Content-Type: application/json" -d '{"email":"user@example.com","password":"string"}' http://localhost:8000/register

# Get token
curl -X POST -H "Content-Type: application/json" -d '{"username":"user@example.com","password":"string"}' http://localhost:8000/token
