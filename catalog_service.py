import pandas as pd
import os
import logging
from ai_service import AIService

class CatalogService:
    def __init__(self):
        self.ai_service = AIService()
        self.catalog_path = None
        self._find_catalog_file()
    
    def _find_catalog_file(self):
        """Find the catalog file in uploads or use sample"""
        upload_path = os.path.join('uploads', 'catalog.xlsx')
        sample_path = 'sample_catalog.xlsx'
        
        if os.path.exists(upload_path):
            self.catalog_path = upload_path
        elif os.path.exists(sample_path):
            self.catalog_path = sample_path
        else:
            logging.warning("No catalog file found")
            self.catalog_path = None
    
    def load_catalog(self):
        """Load and process the product catalog"""
        if not self.catalog_path or not os.path.exists(self.catalog_path):
            logging.error("Catalog file not found")
            return None
        
        try:
            # Load the Excel file with explicit engine
            try:
                catalog_df = pd.read_excel(self.catalog_path, engine='openpyxl')
            except Exception as e1:
                logging.warning(f"Failed with openpyxl: {e1}, trying xlrd")
                try:
                    catalog_df = pd.read_excel(self.catalog_path, engine='xlrd')
                except Exception as e2:
                    logging.warning(f"Failed with xlrd: {e2}, trying without engine")
                    catalog_df = pd.read_excel(self.catalog_path)
            
            # Clean column names (remove extra spaces)
            catalog_df.columns = catalog_df.columns.str.strip()
            
            # Get unique symptoms from catalog
            symptoms_list = []
            if 'sintomas' in catalog_df.columns:
                for symptoms in catalog_df['sintomas'].dropna():
                    if isinstance(symptoms, str):
                        # Split by comma and clean
                        symptom_items = [s.strip() for s in symptoms.split(',')]
                        symptoms_list.extend(symptom_items)
            
            unique_symptoms = list(set(symptoms_list))
            
            logging.info(f"Loaded catalog with {len(catalog_df)} products and {len(unique_symptoms)} unique symptoms")
            
            return {
                'catalog': catalog_df,
                'symptoms': unique_symptoms
            }
            
        except Exception as e:
            logging.error(f"Error loading catalog: {str(e)}")
            return None
    
    def validate_catalog(self, file_path):
        """Validate catalog file structure"""
        try:
            df = pd.read_excel(file_path)
            required_columns = ['nombre', 'sintomas', 'beneficios', 'ingredientes', 
                              'dosis', 'modo_de_uso', 'presentacion']
            
            # Check if required columns exist (case insensitive)
            df_columns_lower = [col.lower().strip() for col in df.columns]
            missing_columns = []
            
            for col in required_columns:
                if col.lower() not in df_columns_lower:
                    missing_columns.append(col)
            
            if missing_columns:
                logging.error(f"Missing columns in catalog: {missing_columns}")
                return False
            
            return True
            
        except Exception as e:
            logging.error(f"Error validating catalog: {str(e)}")
            return False
    
    def recommend_products(self, normalized_symptoms, catalog_df, user_profile):
        """
        Find product recommendations for normalized symptoms
        Returns at least 2 products per symptom when possible
        """
        recommendations = []
        
        if not normalized_symptoms:
            return [{
                'symptom': 'Sin síntomas identificados',
                'products': [],
                'message': 'No se pudieron identificar síntomas específicos en tu descripción. Por favor, intenta describir tus síntomas de manera más específica.'
            }]
        
        for symptom in normalized_symptoms:
            products_for_symptom = self._find_products_for_symptom(symptom, catalog_df, user_profile)
            
            recommendation = {
                'symptom': symptom,
                'products': products_for_symptom,
                'message': self._get_recommendation_message(symptom, products_for_symptom)
            }
            
            recommendations.append(recommendation)
        
        return recommendations
    
    def _find_products_for_symptom(self, symptom, catalog_df, user_profile):
        """Find products that match a specific symptom"""
        matching_products = []
        
        # First, try direct symptom matching
        for idx, row in catalog_df.iterrows():
            if pd.isna(row['sintomas']):
                continue
                
            symptoms_in_product = str(row['sintomas']).lower()
            if symptom.lower() in symptoms_in_product:
                # Verificar contraindicaciones básicas
                safe_to_recommend = True
                if user_profile and 'contradiccion' in row and row['contradiccion']:
                    contraindications = str(row['contradiccion']).lower()
                    user_conditions = str(user_profile.get('condiciones_medicas', [])).lower()
                    # Verificación básica de contraindicaciones
                    if any(cond in contraindications for cond in ['diabetes', 'hipertension', 'embarazo'] if cond in user_conditions):
                        safe_to_recommend = False
                
                if safe_to_recommend:
                    product_info = self._format_product_info(row)
                    matching_products.append(product_info)
        
        # If we have fewer than 2 products, try ingredient-based matching
        if len(matching_products) < 2:
            ingredient_matches = self._find_by_ingredients(symptom, catalog_df, user_profile)
            for product in ingredient_matches:
                if product not in matching_products:
                    matching_products.append(product)
                    if len(matching_products) >= 2:
                        break
        
        # If still fewer than 2, add general wellness products
        if len(matching_products) < 2:
            wellness_products = self._find_wellness_products(catalog_df, user_profile)
            for product in wellness_products:
                if product not in matching_products:
                    matching_products.append(product)
                    if len(matching_products) >= 2:
                        break
        
        return matching_products[:3]  # Return maximum 3 products per symptom
    
    def _find_by_ingredients(self, symptom, catalog_df, user_profile):
        """Find products by analyzing ingredients for the symptom"""
        ingredient_matches = []
        
        # Common ingredient mappings for symptoms
        ingredient_mappings = {
            'dolor': ['cúrcuma', 'jengibre', 'sauce', 'árnica'],
            'inflamación': ['cúrcuma', 'jengibre', 'omega-3', 'boswellia'],
            'estrés': ['valeriana', 'manzanilla', 'passiflora', 'magnesio'],
            'cansancio': ['ginseng', 'vitamina b', 'hierro', 'coenzima q10'],
            'digestión': ['jengibre', 'probióticos', 'enzimas digestivas', 'menta']
        }
        
        relevant_ingredients = []
        for key, ingredients in ingredient_mappings.items():
            if key in symptom.lower():
                relevant_ingredients.extend(ingredients)
        
        if relevant_ingredients:
            for idx, row in catalog_df.iterrows():
                if pd.isna(row['ingredientes']):
                    continue
                    
                ingredients_text = str(row['ingredientes']).lower()
                if any(ingredient in ingredients_text for ingredient in relevant_ingredients):
                    contraindications = self.ai_service.analyze_contraindications(row, user_profile)
                    if not contraindications:
                        product_info = self._format_product_info(row)
                        ingredient_matches.append(product_info)
        
        return ingredient_matches
    
    def _find_wellness_products(self, catalog_df, user_profile):
        """Find general wellness products as fallback"""
        wellness_products = []
        wellness_keywords = ['bienestar', 'multivitamínico', 'energía', 'salud general']
        
        for idx, row in catalog_df.iterrows():
            product_text = f"{str(row.get('nombre', ''))} {str(row.get('beneficios', ''))}".lower()
            
            if any(keyword in product_text for keyword in wellness_keywords):
                contraindications = self.ai_service.analyze_contraindications(row, user_profile)
                if not contraindications:
                    product_info = self._format_product_info(row)
                    wellness_products.append(product_info)
        
        return wellness_products
    
    def _format_product_info(self, product_row):
        """Format product information for display"""
        return {
            'nombre': str(product_row.get('nombre', 'Sin nombre')),
            'beneficios': str(product_row.get('beneficios', 'Sin información')),
            'ingredientes': str(product_row.get('ingredientes', 'Sin información')),
            'dosis': str(product_row.get('dosis', 'Consultar con profesional')),
            'modo_de_uso': str(product_row.get('modo_de_uso', 'Seguir indicaciones del envase')),
            'presentacion': str(product_row.get('presentacion', 'Sin información')),
            'contradiccion': str(product_row.get('contradiccion', 'Sin contraindicaciones conocidas')),
            'condiciones_especiales': str(product_row.get('condiciones especiales', 'Ninguna')),
            'sexo': str(product_row.get('sexo', 'Ambos'))
        }
    
    def _get_recommendation_message(self, symptom, products):
        """Generate appropriate message based on products found"""
        if not products:
            return f"No se encontraron productos específicos en nuestro catálogo para '{symptom}'. Te sugerimos consultar con un profesional de la salud."
        elif len(products) == 1:
            return f"Se encontró un producto sugerido para '{symptom}'."
        else:
            return f"Se encontraron {len(products)} productos sugeridos para '{symptom}'."
