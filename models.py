from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
import os

# Initialize db here to avoid circular imports
db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(500), nullable=False)
    sintomas = Column(Text)
    beneficios = Column(Text)
    dosis = Column(Text)
    ingredientes = Column(Text)
    modo_de_uso = Column(String(100))
    presentacion = Column(String(100))
    contradiccion = Column(Text)
    condiciones_especiales = Column(Text)
    sexo = Column(String(50))
    
    def to_dict(self):
        """Convert product to dictionary for easy JSON serialization"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'sintomas': self.sintomas or '',
            'beneficios': self.beneficios or '',
            'dosis': self.dosis or '',
            'ingredientes': self.ingredientes or '',
            'modo_de_uso': self.modo_de_uso or '',
            'presentacion': self.presentacion or '',
            'contradiccion': self.contradiccion or '',
            'condiciones_especiales': self.condiciones_especiales or '',
            'sexo': self.sexo or 'ambos'
        }
    
    def __repr__(self):
        return f'<Product {self.nombre}>'

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(100), nullable=False)
    nombre = Column(String(200))
    edad = Column(Integer)
    sexo = Column(String(20))
    peso = Column(Integer)
    condiciones_medicas = Column(Text)  # JSON string
    alergias = Column(Text)
    medicamentos = Column(Text)
    created_at = Column(db.DateTime, default=db.func.current_timestamp())
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'edad': self.edad,
            'sexo': self.sexo,
            'peso': self.peso,
            'condiciones_medicas': self.condiciones_medicas,
            'alergias': self.alergias,
            'medicamentos': self.medicamentos
        }

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(100), nullable=False)
    user_symptoms = Column(Text, nullable=False)
    recommended_products = Column(Text)  # JSON string of product IDs
    created_at = Column(db.DateTime, default=db.func.current_timestamp())
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'user_symptoms': self.user_symptoms,
            'recommended_products': self.recommended_products,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    role = Column(String(20), nullable=False, default='sales')  # 'master' or 'sales'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def is_master(self):
        """Check if user has master privileges"""
        return self.role == 'master'
    
    def is_sales(self):
        """Check if user is sales staff"""
        return self.role == 'sales'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'

class SystemLog(db.Model):
    __tablename__ = 'system_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, db.ForeignKey('users.id'), nullable=True)
    action = Column(String(100), nullable=False)
    details = Column(Text)
    ip_address = Column(String(45))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'details': self.details,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ProductMovement(db.Model):
    __tablename__ = 'product_movements'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = Column(Integer, db.ForeignKey('users.id'), nullable=True)
    action = Column(String(50), nullable=False)  # 'recommended', 'viewed', 'updated'
    session_id = Column(String(100))
    symptoms = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    product = db.relationship('Product', backref='movements')
    user = db.relationship('User', backref='product_actions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product.nombre if self.product else None,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'action': self.action,
            'session_id': self.session_id,
            'symptoms': self.symptoms,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class UnresolvedCase(db.Model):
    __tablename__ = 'unresolved_cases'
    
    id = Column(Integer, primary_key=True)
    user_symptoms = Column(Text, nullable=False)
    session_id = Column(String(100))
    user_id = Column(Integer, db.ForeignKey('users.id'), nullable=True)
    status = Column(String(20), default='pending')  # 'pending', 'reviewing', 'resolved'
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime)
    
    user = db.relationship('User', backref='unresolved_cases')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_symptoms': self.user_symptoms,
            'session_id': self.session_id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None
        }