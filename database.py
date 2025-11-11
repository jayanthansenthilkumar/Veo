"""
Database models and configuration for Gen AI Platform
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication and tracking"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    generations = db.relationship('Generation', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Generation(db.Model):
    """Generation history model"""
    __tablename__ = 'generations'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    type = db.Column(db.String(20), nullable=False)  # 'image', 'video', 'music'
    prompt = db.Column(db.Text, nullable=False)
    parameters = db.Column(db.Text)  # JSON string of generation parameters
    output_path = db.Column(db.String(500))
    status = db.Column(db.String(20), default='pending')  # 'pending', 'processing', 'completed', 'failed'
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    
    def __repr__(self):
        return f'<Generation {self.type} - {self.id[:8]}>'
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'type': self.type,
            'prompt': self.prompt,
            'parameters': self.parameters,
            'output_path': self.output_path,
            'status': self.status,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class Settings(db.Model):
    """Application settings model"""
    __tablename__ = 'settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Setting {self.key}>'

def init_db():
    """Initialize database and create all tables"""
    db.create_all()
    print("Database initialized successfully!")
