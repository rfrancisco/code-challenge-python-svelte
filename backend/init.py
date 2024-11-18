import os
from datetime import datetime
from src.app import app, db, User, Expense
from werkzeug.security import generate_password_hash

# Remove the database if it exists
if os.path.isfile("instance/expenses.db"):
    os.remove("instance/expenses.db")

# Create and initialize database with some test data
with app.app_context():
    # Create the tables
    db.create_all()

    # Add example users
    user1 = User(firstname='john', lastname='doe', username='john', password=generate_password_hash('pass'))
    user2 = User(firstname='jane', lastname='doe', username='jane', password=generate_password_hash('pass'))    
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    # Add example expenses
    expense1 = Expense(description='Groceries', amount=50.5, category='Food', date=datetime(2024, 11, 17).date(), user_id=user1.id)
    expense2 = Expense(description='Coffee', amount=5.0, category='Food', date=datetime(2024, 11, 14).date(), user_id=user1.id)
    expense3 = Expense(description='Electricity', amount=100.0, category='Home', date=datetime(2024, 11, 17).date(), user_id=user2.id)
    expense4 = Expense(description='Tires', amount=100.0, category='Car', date=datetime(2024, 11, 15).date(), user_id=user2.id)
    expense5 = Expense(description='Inspection', amount=837.0, category='Car', date=datetime(2024, 11, 15).date(), user_id=user2.id)
    expense6 = Expense(description='Wine', amount=12.99, category='Food', date=datetime(2024, 11, 16).date(), user_id=user2.id)
    db.session.add(expense1)
    db.session.add(expense2)
    db.session.add(expense3)
    db.session.add(expense4)
    db.session.add(expense5)
    db.session.add(expense6)
    db.session.commit()

    print("Database created and initialized with some test data.")
