from datetime import datetime
import re
from os import getenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

# configure app
app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY="secret_sauce",
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True,
    SQLALCHEMY_DATABASE_URI="sqlite:///expenses.db",
)

# configure login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

# configure cors
frontend_url = getenv("FRONTEND_URL", "*")
cors = CORS(
    app,
    resources={r"*": {"origins": frontend_url}},
    expose_headers=["Content-Type"],
    supports_credentials=True,
)

# configure database
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    expenses = db.relationship("Expense", backref="owner", lazy=True)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

# configure endpoints
@login_manager.user_loader
def user_loader(user_id: int):
    return User.query.filter_by(id=user_id).first()

@app.route("/api", methods=["GET"])
def home():
    return "Code Challenge API"

@app.route("/api/health", methods=["GET"])
def get_health():
    return "ok"

# auth related endpoints
@app.route("/api/signin", methods=["POST"])
def signin():
    data = request.json
    
    # Perform validations
    if not data.get("username"):
        return jsonify(message=f"'username' is required"), 400

    if not data.get("password"):
        return jsonify(message=f"'password' is required"), 400

    username = data.get("username")
    password = data.get("password")

    # Perform signin
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify(message=f"Signin performed successfully"), 200

    return jsonify(message=f"Signin failed. Check your credentials"), 400

@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json()
    
    # Perform validations
    if not data.get("firstname"):
        return jsonify(message=f"'firstname' is required"), 400

    if not data.get("lastname"):
        return jsonify(message=f"'lastname' is required"), 400

    if not data.get("username"):
        return jsonify(message=f"'username' is required"), 400

    if not data.get("password"):
        return jsonify(message=f"'password' is required"), 400

    firstname = data.get("firstname")
    lastname = data.get("lastname")
    username = data.get("username")
    password = data.get("password")

    if len(firstname) < 2:
        return jsonify(message="First name must be at least 2 characters long"), 400

    if len(lastname) < 2:
        return jsonify(message="Last name must be at least 2 characters long"), 400

    if len(username) < 3:
        return jsonify(message="Username must be at least 3 characters long"), 400
    
    if len(password) < 3:
        return jsonify(message="Password must be at least 3 characters long"), 400
    
    if not re.match(r"^[a-zA-Z0-9_.-]+$", username):
        return jsonify(message="Username can only contain letters, numbers, dots, underscores, and hyphens"), 400

    if User.query.filter_by(username=username).first():
        return jsonify(message="Username already taken"), 400

    # Create user
    user = User(firstname=firstname, lastname=lastname, username=username, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()

    return jsonify(message="User created successfully"), 201

@app.route("/api/signout", methods=["GET"])
def signout():
    logout_user()
    return jsonify(message=f"Signout performed successfully"), 200

@app.route("/api/user-info", methods=["GET"])
def user_data():
    if current_user.is_authenticated == False:
        return jsonify(message=f"User is not authenticated"), 400

    user = User.query.filter_by(id=current_user.id).first()
    return jsonify({"firstname": user.firstname, "lastname": user.lastname, "username": user.username})

# expenses related endpoints
@app.route("/api/expenses", methods=["GET"])
@login_required
def get_expenses():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        "id": expense.id,
        "description": expense.description,
        "amount": expense.amount,
        "category": expense.category,
        "date": expense.date.isoformat()
    } for expense in expenses]), 200

@app.route("/api/expenses/<int:id>", methods=["GET"])
@login_required
def get_expense(id):
    expense = Expense.query.filter_by(id=id, user_id=current_user.id).first()
    return jsonify({
        "id": expense.id,
        "description": expense.description,
        "amount": expense.amount,
        "category": expense.category,
        "date": expense.date.isoformat()
    }), 200

@app.route("/api/expenses", methods=["POST"])
@login_required
def create_expense():
    data = request.get_json()

    # Perform validations
    if not data.get("description"):
        return jsonify(message=f"'description' is required"), 400

    if not data.get("amount"):
        return jsonify(message=f"'amount' is required"), 400

    if not data.get("category"):
        return jsonify(message=f"'category' is required"), 400

    if not data.get("date"):
        return jsonify(message=f"'date' is required"), 400

    description = data.get("description")
    amount = data.get("amount")
    category = data.get("category")
    date = datetime.strptime(data.get("date"), "%Y-%m-%d").date()

    if len(description) < 3:
        return jsonify(message="Description must be at least 3 characters long"), 400
    
    if len(category) < 3:
        return jsonify(message="Category must be at least 3 characters long"), 400
    
    if amount < 0:
        return jsonify(message="Amount must be a positive number"), 400

    # Create expense
    expense = Expense(description=description, amount=amount, category=category, date=date, user_id=current_user.id)
    db.session.add(expense)
    db.session.commit()

    return jsonify(message="Expense created successfully"), 201

@app.route("/api/expenses/<int:id>", methods=["PUT"])
@login_required
def update_expense(id):
    data = request.get_json()
    expense = Expense.query.filter_by(id=id, user_id=current_user.id).first()

    # Perform validations
    if not expense:
        return jsonify(message="Expense not found"), 404

    if not data.get("description"):
        return jsonify(message=f"'description' is required"), 400

    if not data.get("amount"):
        return jsonify(message=f"'amount' is required"), 400

    if not data.get("category"):
        return jsonify(message=f"'category' is required"), 400

    if not data.get("date"):
        return jsonify(message=f"'date' is required"), 400

    description = data.get("description")
    amount = data.get("amount")
    category = data.get("category")
    date = datetime.strptime(data.get("date"), "%Y-%m-%d").date()

    if len(description) < 3:
        return jsonify(message="Description must be at least 3 characters long"), 400
    
    if len(category) < 3:
        return jsonify(message="Category must be at least 3 characters long"), 400
    
    if amount < 0:
        return jsonify(message="Amount must be a positive number"), 400

    # Update expense
    expense.description = description
    expense.amount = amount
    expense.category = category
    expense.date = date
    db.session.commit()

    return jsonify(message="Expense updated successfully"), 200

@app.route("/api/expenses/<int:id>", methods=["DELETE"])
@login_required
def delete_expense(id):
    expense = Expense.query.filter_by(id=id, user_id=current_user.id).first()

    # Perform validations
    if not expense:
        return jsonify(message="Expense not found"), 404

    # Delete expense
    db.session.delete(expense)
    db.session.commit()

    return jsonify(message="Expense deleted successfully"), 200

if __name__ == "__main__":
    app.run(debug=True)
