import os
import json
import logging
from openai import OpenAI

class AIService:
    def __init__(self):
        """Initialize OpenAI client"""
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
        
    def normalize_symptoms(self, user_input, catalog_symptoms):
        """
        Uses GPT-4o to map user input to the closest matching symptoms in the catalog.
        Returns a list of catalog symptom names.
        """
        try:
            # Create a comprehensive prompt for Spanish symptom analysis
            prompt = f"""
            Eres un asistente médico especializado en productos naturales de Canatura.
            
            El usuario describe sus síntomas así: "{user_input}"
            
            Analiza esta descripción y determina qué síntomas del catálogo oficial corresponden.
            
            Lista de síntomas disponibles en el catálogo:
            {', '.join(catalog_symptoms)}
            
            INSTRUCCIONES IMPORTANTES:
            1. Solo puedes usar síntomas que estén EXACTAMENTE en la lista del catálogo
            2. Si no encuentras coincidencias exactas, busca sinónimos o términos relacionados
            3. Interpreta expresiones coloquiales en español (ej: "me siento mal del estómago" = "dolor abdominal")
            4. Si no hay ninguna coincidencia, devuelve una lista vacía
            5. Devuelve máximo 5 síntomas más relevantes
            
            Responde SOLO con un JSON en este formato:
            {{"sintomas_encontrados": ["síntoma1", "síntoma2"]}}
            """
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            symptoms_found = result.get('sintomas_encontrados', [])
            
            # Validate that returned symptoms are actually in the catalog
            validated_symptoms = [s for s in symptoms_found if s in catalog_symptoms]
            
            logging.info(f"User input: {user_input}")
            logging.info(f"AI found symptoms: {symptoms_found}")
            logging.info(f"Validated symptoms: {validated_symptoms}")
            
            return validated_symptoms
            
        except Exception as e:
            logging.error(f"Error in AI symptom normalization: {str(e)}")
            # Usar búsqueda inteligente directa como método principal
            return self._enhanced_symptom_matching(user_input, catalog_symptoms)
    
    def _enhanced_symptom_matching(self, user_input, catalog_symptoms):
        """Búsqueda inteligente de síntomas sin APIs externas"""
        import re
        from difflib import SequenceMatcher
        
        user_input_lower = user_input.lower()
        
        # Mapeos completos de síntomas en español
        symptom_mappings = {
            'dolor': ['dolor', 'duele', 'dolencia', 'molestia', 'malestar'],
            'cabeza': ['cabeza', 'cefalea', 'migraña', 'migrana'],
            'estómago': ['estómago', 'estomago', 'gastrico', 'abdominal'],
            'estrés': ['estrés', 'estres', 'tensión', 'ansiedad', 'nervios'],
            'cansancio': ['cansancio', 'fatiga', 'agotamiento', 'debilidad'],
            'sueño': ['sueño', 'dormir', 'insomnio', 'descanso'],
            'articulaciones': ['articulaciones', 'articular', 'rodillas', 'huesos'],
            'digestión': ['digestión', 'digestivo', 'intestinal'],
            'inflamación': ['inflamación', 'hinchazón', 'hinchado'],
            'energía': ['energía', 'vitalidad', 'fuerza'],
            'músculos': ['músculos', 'muscular', 'calambres']
        }
        
        scored_matches = []
        
        for catalog_symptom in catalog_symptoms:
            catalog_lower = catalog_symptom.lower().strip()
            score = 0
            
            # Coincidencia exacta
            if catalog_lower in user_input_lower:
                score += 10
            
            # Coincidencia de palabras
            for word in catalog_lower.split():
                if len(word) > 3 and word in user_input_lower:
                    score += 5
            
            # Verificar mapeos
            for mapped_symptom, variations in symptom_mappings.items():
                if mapped_symptom in catalog_lower:
                    for variation in variations:
                        if variation in user_input_lower:
                            score += 4
            
            if score > 0:
                scored_matches.append((catalog_symptom, score))
        
        # Ordenar y retornar los mejores
        scored_matches.sort(key=lambda x: x[1], reverse=True)
        result = [match[0] for match in scored_matches[:8]]
        
        logging.info(f"Enhanced matching found: {result}")
        return result
    
    def _fallback_symptom_matching(self, user_input, catalog_symptoms):
        """
        Fallback method for symptom matching using simple keyword search
        """
        user_lower = user_input.lower()
        matches = []
        
        # Common Spanish symptom keywords mapping
        keyword_mapping = {
            'dolor': ['dolor'],
            'cabeza': ['dolor de cabeza', 'cefalea'],
            'estomago': ['dolor abdominal', 'gastritis'],
            'espalda': ['dolor de espalda'],
            'cansado': ['fatiga', 'cansancio'],
            'estres': ['estrés', 'ansiedad'],
            'inflamacion': ['inflamación'],
            'gripe': ['gripe', 'resfriado'],
            'tos': ['tos'],
            'fiebre': ['fiebre'],
            'insomnio': ['insomnio'],
            'digestion': ['digestión', 'indigestión']
        }
        
        for keyword, related_symptoms in keyword_mapping.items():
            if keyword in user_lower:
                for symptom in catalog_symptoms:
                    if any(related in symptom.lower() for related in related_symptoms):
                        if symptom not in matches:
                            matches.append(symptom)
        
        return matches[:3]  # Return max 3 matches
    
    def analyze_contraindications(self, product, user_profile):
        """
        Analyze if a product has contraindications for the user profile
        """
        contraindications = []
        
        # Check diabetes contraindications
        if user_profile.get('diabetes') and product.get('contradiccion'):
            contraindication_text = str(product['contradiccion']).lower()
            if 'diabetes' in contraindication_text or 'diabético' in contraindication_text:
                contraindications.append('diabetes')
        
        # Check hypertension contraindications
        if user_profile.get('hypertension') and product.get('contradiccion'):
            contraindication_text = str(product['contradiccion']).lower()
            if 'hipertensión' in contraindication_text or 'presión alta' in contraindication_text:
                contraindications.append('hipertension')
        
        # Check pregnancy contraindications
        if user_profile.get('pregnancy') and product.get('contradiccion'):
            contraindication_text = str(product['contradiccion']).lower()
            if 'embarazo' in contraindication_text or 'embarazada' in contraindication_text:
                contraindications.append('embarazo')
        
        # Check gender-specific products
        if product.get('sexo') and product['sexo'].lower() != 'ambos':
            user_gender = user_profile.get('gender', '').lower()
            product_gender = product['sexo'].lower()
            if (product_gender == 'masculino' and user_gender == 'femenino') or \
               (product_gender == 'femenino' and user_gender == 'masculino'):
                contraindications.append('genero')
        
        return contraindications
