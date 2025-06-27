import pandas as pd
import json
import logging
from models import Product, UserProfile, Recommendation, db
from sqlalchemy import or_, and_, func
import re

class DatabaseService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def load_catalog_to_database(self, catalog_file_path):
        """Load catalog from Excel file into database"""
        try:
            # Read the Excel file
            df = pd.read_excel(catalog_file_path, engine='openpyxl')
            
            # Clean column names
            df.columns = df.columns.str.strip().str.lower()
            
            # Fill NaN values
            df = df.fillna('')
            
            # Clear existing products
            Product.query.delete()
            
            # Insert products
            products_added = 0
            for _, row in df.iterrows():
                product = Product(
                    nombre=str(row.get('nombre', '')),
                    sintomas=str(row.get('sintomas', '')),
                    beneficios=str(row.get('beneficios', '')),
                    dosis=str(row.get('dosis', '')),
                    ingredientes=str(row.get('ingredientes', '')),
                    modo_de_uso=str(row.get('modo_de_uso', 'INGERIBLE')),
                    presentacion=str(row.get('presentacion', '')),
                    contradiccion=str(row.get('contradiccion', '')),
                    condiciones_especiales=str(row.get('condiciones especiales', '')),
                    sexo=str(row.get('sexo', 'ambos'))
                )
                db.session.add(product)
                products_added += 1
            
            db.session.commit()
            self.logger.info(f"Successfully loaded {products_added} products to database")
            return products_added
            
        except Exception as e:
            db.session.rollback()
            self.logger.error(f"Error loading catalog to database: {e}")
            return 0
    
    def search_products_by_symptoms(self, user_symptoms, user_profile=None, limit=10):
        """Search products in database by symptoms using intelligent matching"""
        try:
            # Normalize user input
            symptoms_normalized = self._normalize_text(user_symptoms)
            
            # Extract keywords
            keywords = self._extract_keywords(symptoms_normalized)
            
            # Build search conditions
            search_conditions = []
            
            for keyword in keywords:
                # Search in symptoms, benefits, and ingredients
                search_conditions.extend([
                    Product.sintomas.ilike(f'%{keyword}%'),
                    Product.beneficios.ilike(f'%{keyword}%'),
                    Product.ingredientes.ilike(f'%{keyword}%')
                ])
            
            # Execute search with OR conditions
            if search_conditions:
                products = Product.query.filter(or_(*search_conditions)).all()
            else:
                # Fallback: return general wellness products
                products = Product.query.filter(
                    or_(
                        Product.beneficios.ilike('%energia%'),
                        Product.beneficios.ilike('%bienestar%'),
                        Product.beneficios.ilike('%salud%')
                    )
                ).limit(limit).all()
            
            # Filter by user profile constraints
            if user_profile:
                products = self._filter_by_user_profile(products, user_profile)
            
            # Score and rank products
            scored_products = self._score_products(products, keywords)
            
            # Return top results
            return scored_products[:limit]
            
        except Exception as e:
            self.logger.error(f"Error searching products: {e}")
            return []
    
    def _normalize_text(self, text):
        """Normalize Spanish text for better matching"""
        if not text:
            return ""
        
        text = text.lower()
        
        # Replace Spanish accents
        accent_map = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u',
            'ñ': 'n'
        }
        
        for accented, normal in accent_map.items():
            text = text.replace(accented, normal)
        
        return text
    
    def _extract_keywords(self, text):
        """Extract meaningful keywords from user input"""
        # Remove common Spanish stop words
        stop_words = {
            'me', 'mi', 'mis', 'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
            'de', 'del', 'en', 'con', 'por', 'para', 'que', 'como', 'muy', 'mas',
            'pero', 'si', 'no', 'yo', 'tu', 'su', 'sus', 'este', 'esta', 'estos',
            'estas', 'ese', 'esa', 'esos', 'esas', 'aquel', 'aquella', 'aquellos',
            'aquellas', 'y', 'o', 'cuando', 'donde', 'porque', 'tengo', 'siento',
            'estoy', 'soy', 'he', 'ha', 'han', 'hay', 'fue', 'ser', 'estar'
        }
        
        # Extract words (3+ characters, not stop words)
        words = re.findall(r'\b\w{3,}\b', text)
        keywords = [word for word in words if word not in stop_words]
        
        return keywords
    
    def _filter_by_user_profile(self, products, user_profile):
        """Filter products based on user profile constraints"""
        filtered_products = []
        
        for product in products:
            # Check gender restrictions
            if product.sexo and product.sexo != 'ambos' and product.sexo != user_profile.get('sexo', ''):
                continue
            
            # Check contraindications
            if product.contradiccion and user_profile.get('condiciones_medicas'):
                user_conditions = user_profile.get('condiciones_medicas', '').lower()
                contraindications = product.contradiccion.lower()
                
                # Simple check for common contraindications
                if any(condition in contraindications for condition in ['diabetes', 'hipertension', 'embarazo'] 
                       if condition in user_conditions):
                    continue
            
            filtered_products.append(product)
        
        return filtered_products
    
    def _score_products(self, products, keywords):
        """Score products based on keyword relevance"""
        scored_products = []
        
        for product in products:
            score = 0
            matches = []
            
            # Search text (symptoms + benefits + ingredients)
            search_text = f"{product.sintomas} {product.beneficios} {product.ingredientes}".lower()
            
            for keyword in keywords:
                # Count occurrences in different fields with different weights
                symptom_matches = product.sintomas.lower().count(keyword) * 3
                benefit_matches = product.beneficios.lower().count(keyword) * 2
                ingredient_matches = product.ingredientes.lower().count(keyword) * 1
                
                total_matches = symptom_matches + benefit_matches + ingredient_matches
                score += total_matches
                
                if total_matches > 0:
                    matches.append(keyword)
            
            if score > 0:
                scored_products.append({
                    'product': product,
                    'score': score,
                    'matches': matches
                })
        
        # Sort by score (highest first)
        scored_products.sort(key=lambda x: x['score'], reverse=True)
        
        return scored_products
    
    def save_user_profile(self, session_id, profile_data):
        """Save user profile to database"""
        try:
            # Check if profile exists
            existing_profile = UserProfile.query.filter_by(session_id=session_id).first()
            
            if existing_profile:
                # Update existing
                existing_profile.nombre = profile_data.get('nombre')
                existing_profile.edad = profile_data.get('edad')
                existing_profile.sexo = profile_data.get('sexo')
                existing_profile.peso = profile_data.get('peso')
                existing_profile.condiciones_medicas = json.dumps(profile_data.get('condiciones_medicas', []))
                existing_profile.alergias = profile_data.get('alergias', '')
                existing_profile.medicamentos = profile_data.get('medicamentos', '')
            else:
                # Create new
                profile = UserProfile(
                    session_id=session_id,
                    nombre=profile_data.get('nombre'),
                    edad=profile_data.get('edad'),
                    sexo=profile_data.get('sexo'),
                    peso=profile_data.get('peso'),
                    condiciones_medicas=json.dumps(profile_data.get('condiciones_medicas', [])),
                    alergias=profile_data.get('alergias', ''),
                    medicamentos=profile_data.get('medicamentos', '')
                )
                db.session.add(profile)
            
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            self.logger.error(f"Error saving user profile: {e}")
            return False
    
    def get_user_profile(self, session_id):
        """Get user profile from database"""
        try:
            profile = UserProfile.query.filter_by(session_id=session_id).first()
            if profile:
                return profile.to_dict()
            return None
        except Exception as e:
            self.logger.error(f"Error getting user profile: {e}")
            return None
    
    def save_recommendation(self, session_id, user_symptoms, recommended_products):
        """Save recommendation to database"""
        try:
            recommendation = Recommendation(
                session_id=session_id,
                user_symptoms=user_symptoms,
                recommended_products=json.dumps([p.id for p in recommended_products])
            )
            db.session.add(recommendation)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            self.logger.error(f"Error saving recommendation: {e}")
            return False
    
    def get_product_count(self):
        """Get total number of products in database"""
        try:
            return Product.query.count()
        except Exception as e:
            self.logger.error(f"Error getting product count: {e}")
            return 0