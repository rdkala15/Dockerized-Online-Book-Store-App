from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# In-memory storage (in production use a real database)
users_db = {}
orders_db = {}

# Enhanced book data with categories, descriptions, ratings
books_data = [
    {
        "id": 1,
        "title": "HTML Basics",
        "price": 199,
        "category": "Web Development",
        "rating": 4.5,
        "reviews": 128,
        "description": "Learn the fundamentals of HTML and build your first website",
        "featured": True,
        "author": "John Smith"
    },
    {
        "id": 2,
        "title": "CSS Design",
        "price": 249,
        "category": "Web Development",
        "rating": 4.7,
        "reviews": 95,
        "description": "Master CSS styling and create beautiful web designs",
        "featured": True,
        "author": "Sarah Johnson"
    },
    {
        "id": 3,
        "title": "Docker for Beginners",
        "price": 399,
        "category": "DevOps",
        "rating": 4.8,
        "reviews": 156,
        "description": "Complete guide to Docker containerization and deployment",
        "featured": True,
        "author": "Michael Chen"
    },
    {
        "id": 4,
        "title": "Python Programming",
        "price": 299,
        "category": "Programming",
        "rating": 4.6,
        "reviews": 112,
        "description": "Python basics to advanced concepts for all skill levels",
        "featured": False,
        "author": "David Brown"
    },
    {
        "id": 5,
        "title": "JavaScript Mastery",
        "price": 349,
        "category": "Web Development",
        "rating": 4.9,
        "reviews": 203,
        "description": "Complete JavaScript guide from ES6 to modern frameworks",
        "featured": True,
        "author": "Emily Davis"
    },
    {
        "id": 6,
        "title": "Kubernetes Guide",
        "price": 449,
        "category": "DevOps",
        "rating": 4.4,
        "reviews": 87,
        "description": "Production-ready Kubernetes deployment strategies",
        "featured": False,
        "author": "Robert Wilson"
    }
]

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Online Book Store API!"})

@app.route("/books")
def get_books():
    return jsonify(books_data)

@app.route("/books/featured")
def get_featured_books():
    featured = [book for book in books_data if book.get("featured", False)]
    return jsonify(featured)

@app.route("/books/categories")
def get_categories():
    categories = list(set(book["category"] for book in books_data))
    return jsonify(categories)

# Authentication endpoints
@app.route("/auth/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    
    if not username or not password or not email:
        return jsonify({"error": "Missing fields"}), 400
    
    if username in users_db:
        return jsonify({"error": "User already exists"}), 409
    
    users_db[username] = {
        "password": password,
        "email": email,
        "created_at": datetime.now().isoformat()
    }
    
    return jsonify({"message": "Registration successful", "username": username}), 201

@app.route("/auth/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if username not in users_db:
        return jsonify({"error": "User not found"}), 401
    
    if users_db[username]["password"] != password:
        return jsonify({"error": "Invalid password"}), 401
    
    return jsonify({"message": "Login successful", "username": username}), 200

@app.route("/auth/validate", methods=["POST"])
def validate_user():
    data = request.json
    username = data.get("username")
    
    if username in users_db:
        return jsonify({"valid": True, "username": username}), 200
    
    return jsonify({"valid": False}), 401

# Order endpoints
@app.route("/orders", methods=["POST"])
def create_order():
    data = request.json
    username = data.get("username")
    items = data.get("items", [])
    total = data.get("total", 0)
    
    if not username or username not in users_db:
        return jsonify({"error": "Invalid user"}), 401
    
    order_id = len(orders_db) + 1
    order = {
        "id": order_id,
        "username": username,
        "items": items,
        "total": total,
        "date": datetime.now().isoformat(),
        "status": "completed"
    }
    
    orders_db[order_id] = order
    
    return jsonify({"message": "Order created", "order": order}), 201

@app.route("/orders/<username>")
def get_orders(username):
    user_orders = [order for order in orders_db.values() if order["username"] == username]
    return jsonify(user_orders), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

