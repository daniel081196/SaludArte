import pandas as pd
import re
from difflib import SequenceMatcher
import logging

class SmartSearchService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.catalog_df = None
        self.load_catalog()
    
    def load_catalog(self):
        """Load the Canatura catalog"""
        try:
            # Try to load the main catalog
            catalog_file = "PLANTILLA CATALOGO CON INGREDIENTES.xlsx"
            try:
                self.catalog_df = pd.read_excel(catalog_file, engine='openpyxl')
            except:
                try:
                    self.catalog_df = pd.read_excel(catalog_file, engine='xlrd')
                except:
                    # Use sample catalog as fallback
                    self.catalog_df = pd.read_excel("sample_catalog.xlsx", engine='openpyxl')
            
            # Clean and normalize
            self.catalog_df = self.catalog_df.fillna('')
            self.catalog_df.columns = self.catalog_df.columns.str.strip().str.lower()
            
            # Normalize text columns for better searching
            for col in ['sintomas', 'beneficios', 'ingredientes']:
                if col in self.catalog_df.columns:
                    self.catalog_df[f'{col}_norm'] = self.catalog_df[col].apply(self.normalize_text)
            
            self.logger.info(f"Loaded catalog with {len(self.catalog_df)} products")
            
        except Exception as e:
            self.logger.error(f"Error loading catalog: {e}")
            self.catalog_df = None
    
    def normalize_text(self, text):
        """Normalize Spanish text for better matching"""
        if not isinstance(text, str):
            return ""
        
        text = text.lower()
        
        # Replace Spanish accents
        accent_map = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u', 'ñ': 'n'
        }
        for accented, normal in accent_map.items():
            text = text.replace(accented, normal)
        
        return text
    
    def search_products_by_symptoms(self, user_symptoms, user_profile=None, min_products=5):
        """Main search function for finding products by symptoms"""
        if self.catalog_df is None or len(self.catalog_df) == 0:
            return []
        
        try:
            # Normalize user input
            symptoms_normalized = self.normalize_text(user_symptoms)
            
            # Extract keywords
            keywords = self.extract_keywords(symptoms_normalized)
            
            # Score products
            scored_products = self.score_products(keywords)
            
            # Filter by user profile
            if user_profile:
                scored_products = self.filter_by_profile(scored_products, user_profile)
            
            # Ensure minimum products and variety
            final_products = self.ensure_variety(scored_products, min_products)
            
            return final_products
            
        except Exception as e:
            self.logger.error(f"Error in product search: {e}")
            return []
    
    def extract_keywords(self, text):
        """Extract meaningful keywords from user input"""
        # Spanish stop words
        stop_words = {
            'me', 'mi', 'mis', 'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
            'de', 'del', 'en', 'con', 'por', 'para', 'que', 'como', 'muy', 'mas',
            'pero', 'si', 'no', 'yo', 'tu', 'su', 'sus', 'este', 'esta', 'estos',
            'estas', 'ese', 'esa', 'esos', 'esas', 'y', 'o', 'cuando', 'donde',
            'tengo', 'siento', 'estoy', 'soy', 'he', 'ha', 'han', 'hay', 'fue'
        }
        
        # Extract words (3+ characters, not stop words)
        words = re.findall(r'\b\w{3,}\b', text)
        keywords = [word for word in words if word not in stop_words]
        
        # Add common symptom variations
        symptom_expansions = {
            'dolor': ['dolor', 'duele', 'dolencia', 'molestia'],
            'cabeza': ['cabeza', 'cefalea', 'migrana'],
            'estres': ['estres', 'tension', 'ansiedad', 'nervios'],
            'cansancio': ['cansancio', 'fatiga', 'agotamiento'],
            'dormir': ['dormir', 'sueno', 'insomnio', 'descanso'],
            'articulaciones': ['articulaciones', 'articular', 'huesos'],
            'estomago': ['estomago', 'gastrico', 'digestivo']
        }
        
        expanded_keywords = keywords.copy()
        for keyword in keywords:
            if keyword in symptom_expansions:
                expanded_keywords.extend(symptom_expansions[keyword])
        
        return list(set(expanded_keywords))
    
    def score_products(self, keywords):
        """Score products based on keyword matches"""
        scored_products = []
        
        for idx, product in self.catalog_df.iterrows():
            score = 0
            matches = []
            
            # Search in symptoms (highest weight)
            if 'sintomas_norm' in self.catalog_df.columns:
                for keyword in keywords:
                    count = product['sintomas_norm'].count(keyword)
                    if count > 0:
                        score += count * 5
                        matches.append(f"Síntoma: {keyword}")
            
            # Search in benefits (medium weight)
            if 'beneficios_norm' in self.catalog_df.columns:
                for keyword in keywords:
                    count = product['beneficios_norm'].count(keyword)
                    if count > 0:
                        score += count * 3
                        matches.append(f"Beneficio: {keyword}")
            
            # Search in ingredients (lower weight)
            if 'ingredientes_norm' in self.catalog_df.columns:
                for keyword in keywords:
                    count = product['ingredientes_norm'].count(keyword)
                    if count > 0:
                        score += count * 1
                        matches.append(f"Ingrediente: {keyword}")
            
            # Fuzzy matching for similar terms
            for keyword in keywords:
                all_text = f"{product.get('sintomas', '')} {product.get('beneficios', '')}".lower()
                words_in_product = re.findall(r'\b\w{4,}\b', all_text)
                
                for word in words_in_product:
                    similarity = SequenceMatcher(None, keyword, word).ratio()
                    if similarity > 0.8:
                        score += 2
                        matches.append(f"Similar: {word}")
            
            if score > 0:
                scored_products.append({
                    'product_data': product,
                    'score': score,
                    'matches': matches
                })
        
        # Sort by score
        scored_products.sort(key=lambda x: x['score'], reverse=True)
        return scored_products
    
    def filter_by_profile(self, scored_products, user_profile):
        """Filter products based on user profile constraints"""
        filtered = []
        
        for item in scored_products:
            product = item['product_data']
            
            # Check gender restrictions
            if 'sexo' in product and product['sexo']:
                if product['sexo'].lower() not in ['ambos', 'todos'] and product['sexo'].lower() != user_profile.get('sexo', '').lower():
                    continue
            
            # Check contraindications
            if 'contradiccion' in product and product['contradiccion']:
                contraindications = self.normalize_text(product['contradiccion'])
                user_conditions = self.normalize_text(str(user_profile.get('condiciones_medicas', [])))
                
                # Basic contraindication checking
                danger_words = ['diabetes', 'hipertension', 'embarazo', 'lactancia']
                if any(word in contraindications and word in user_conditions for word in danger_words):
                    continue
            
            filtered.append(item)
        
        return filtered
    
    def ensure_variety(self, scored_products, min_products):
        """Ensure product variety and minimum count"""
        if not scored_products:
            # Return general wellness products if no matches
            return self.get_wellness_products(min_products)
        
        # Remove duplicate product bases
        seen_bases = set()
        varied_products = []
        
        for item in scored_products:
            product = item['product_data']
            # Extract base name (remove sizes, counts)
            base_name = re.sub(r'C/\d+|\d+\s*(GRS|ML|CAPS)', '', product.get('nombre', '')).strip()
            
            if base_name not in seen_bases:
                seen_bases.add(base_name)
                varied_products.append(self.format_product_recommendation(item))
        
        # Ensure minimum products
        if len(varied_products) < min_products:
            additional = self.get_wellness_products(min_products - len(varied_products))
            varied_products.extend(additional)
        
        return varied_products[:min_products * 2]  # Return up to double minimum for variety
    
    def get_wellness_products(self, count):
        """Get general wellness products as fallback"""
        try:
            wellness_keywords = ['energia', 'bienestar', 'salud', 'vitaminas', 'natural']
            wellness_products = []
            
            for idx, product in self.catalog_df.iterrows():
                all_text = f"{product.get('beneficios', '')} {product.get('nombre', '')}".lower()
                if any(keyword in all_text for keyword in wellness_keywords):
                    wellness_products.append({
                        'product_data': product,
                        'score': 1,
                        'matches': ['Producto de bienestar general']
                    })
            
            # Format and return
            formatted = [self.format_product_recommendation(item) for item in wellness_products[:count]]
            return formatted
            
        except Exception as e:
            self.logger.error(f"Error getting wellness products: {e}")
            return []
    
    def format_product_recommendation(self, scored_item):
        """Format product data for recommendation display"""
        product = scored_item['product_data']
        
        return {
            'nombre': product.get('nombre', 'Producto Natural'),
            'beneficios': product.get('beneficios', 'Beneficios para la salud natural'),
            'dosis': product.get('dosis', 'Consultar con especialista'),
            'modo_de_uso': product.get('modo_de_uso', 'INGERIBLE'),
            'presentacion': product.get('presentacion', 'Suplemento natural'),
            'ingredientes': product.get('ingredientes', 'Ingredientes naturales'),
            'puntuacion': scored_item['score'],
            'coincidencias': scored_item['matches']
        }