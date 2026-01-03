from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    accepted_terms = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.email}>"
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    category = db.Column(db.String(50))
    image = db.Column(db.Text)   # base64
    stress_score = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)