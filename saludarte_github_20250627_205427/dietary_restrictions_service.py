import pandas as pd
import logging
import re

class DietaryRestrictionsService:
    """
    Servicio para manejar restricciones alimentarias según síntomas
    Usa el archivo de restricciones alimentarias de SaludArte
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.restrictions_df = None
        self.load_dietary_restrictions()
    
    def load_dietary_restrictions(self):
        """Cargar archivo de restricciones alimentarias"""
        try:
            self.restrictions_df = pd.read_excel('Restricciones_Alimentarias_Completa_SaludArte.xlsx')
            self.restrictions_df = self.restrictions_df.fillna('')
            
            # Limpiar nombres de columnas
            self.restrictions_df.columns = self.restrictions_df.columns.str.strip()
            
            self.logger.info(f"✓ Restricciones alimentarias cargadas: {len(self.restrictions_df)} condiciones")
            
        except Exception as e:
            self.logger.error(f"Error cargando restricciones alimentarias: {e}")
            self.restrictions_df = None
    
    def get_dietary_recommendations(self, detected_symptoms, user_profile=None):
        """
        Obtener sugerencias alimentarias según síntomas detectados
        """
        if self.restrictions_df is None:
            return None
        
        dietary_advice = {
            'restrictions': [],
            'recommendations': [],
            'warnings': [],
            'medication_interactions': []
        }
        
        # Mapeo de síntomas a problemas de salud
        symptom_to_condition = {
            'dolor': ['gastritis', 'colitis', 'artritis'],
            'nauseas': ['gastritis', 'higado graso'],
            'estres': ['hipertension arterial', 'ansiedad'],
            'insomnio': ['ansiedad', 'estres'],
            'diabetes': ['diabetes'],
            'hipertension': ['hipertension arterial'],
            'dolor_articular': ['artritis', 'osteoporosis'],
            'digestivo': ['gastritis', 'colitis'],
            'fatiga': ['anemia', 'diabetes', 'tiroides'],
            'sobrepeso': ['diabetes', 'higado graso'],
            'colesterol': ['higado graso', 'hipertension arterial']
        }
        
        # Buscar condiciones relacionadas con los síntomas
        relevant_conditions = set()
        for symptom in detected_symptoms:
            if symptom in symptom_to_condition:
                relevant_conditions.update(symptom_to_condition[symptom])
        
        # Agregar condiciones del perfil del usuario
        if user_profile:
            if user_profile.get('diabetes', False):
                relevant_conditions.add('diabetes')
            if user_profile.get('hypertension', False):
                relevant_conditions.add('hipertension arterial')
        
        # Buscar restricciones para cada condición
        for condition in relevant_conditions:
            restriction_info = self._find_restriction_by_condition(condition)
            if restriction_info:
                dietary_advice['restrictions'].append({
                    'condition': condition.title(),
                    'avoid_foods': restriction_info['avoid_foods'],
                    'recommended_foods': restriction_info['recommended_foods'],
                    'clinical_justification': restriction_info['clinical_justification'],
                    'mexican_examples_avoid': restriction_info['mexican_examples_avoid'],
                    'warnings': restriction_info['warnings'],
                    'medication_interactions': restriction_info['medication_interactions']
                })
        
        return dietary_advice if dietary_advice['restrictions'] else None
    
    def _find_restriction_by_condition(self, condition):
        """Buscar restricciones para una condición específica"""
        condition_lower = condition.lower()
        
        for _, row in self.restrictions_df.iterrows():
            problem_symptom = str(row['Problema/Síntoma']).lower()
            
            # Buscar coincidencias exactas o parciales
            if (condition_lower in problem_symptom or 
                any(keyword in problem_symptom for keyword in condition_lower.split())):
                
                return {
                    'avoid_foods': str(row.get('Alimentos NO recomendados', '')),
                    'recommended_foods': str(row.get('Alimentos SÍ recomendados', '')),
                    'clinical_justification': str(row.get('Justificación clínica', '')),
                    'mexican_examples_avoid': str(row.get('Ejemplos mexicanos NO recomendados', '')),
                    'warnings': str(row.get('Observaciones/Advertencias', '')),
                    'medication_interactions': str(row.get('Restricciones por medicamentos', ''))
                }
        
        return None
    
    def format_dietary_advice_for_display(self, dietary_advice):
        """Formatear consejos alimentarios para mostrar en la receta"""
        if not dietary_advice or not dietary_advice['restrictions']:
            return ""
        
        formatted_advice = []
        
        for restriction in dietary_advice['restrictions']:
            advice_section = f"\n🍽️ **RECOMENDACIONES ALIMENTARIAS para {restriction['condition']}:**\n"
            
            # Alimentos a evitar
            if restriction['avoid_foods']:
                advice_section += f"\n❌ **EVITAR:**\n{restriction['avoid_foods']}\n"
            
            # Alimentos recomendados
            if restriction['recommended_foods']:
                advice_section += f"\n✅ **CONSUMIR:**\n{restriction['recommended_foods']}\n"
            
            # Ejemplos mexicanos a evitar
            if restriction['mexican_examples_avoid']:
                advice_section += f"\n🇲🇽 **Ejemplos mexicanos a evitar:**\n{restriction['mexican_examples_avoid']}\n"
            
            # Advertencias importantes
            if restriction['warnings']:
                advice_section += f"\n⚠️ **IMPORTANTE:**\n{restriction['warnings']}\n"
            
            # Interacciones con medicamentos
            if restriction['medication_interactions']:
                advice_section += f"\n💊 **Interacciones medicamentosas:**\n{restriction['medication_interactions']}\n"
            
            formatted_advice.append(advice_section)
        
        return "\n".join(formatted_advice)
    
    def format_dietary_advice_for_whatsapp(self, dietary_advice):
        """Formatear consejos alimentarios para WhatsApp"""
        if not dietary_advice or not dietary_advice['restrictions']:
            return ""
        
        whatsapp_text = "\n🍽️ RECOMENDACIONES ALIMENTARIAS:\n\n"
        
        for restriction in dietary_advice['restrictions']:
            whatsapp_text += f"📋 {restriction['condition']}:\n"
            
            if restriction['avoid_foods']:
                whatsapp_text += f"❌ Evitar: {restriction['avoid_foods']}\n"
            
            if restriction['recommended_foods']:
                whatsapp_text += f"✅ Consumir: {restriction['recommended_foods']}\n"
            
            if restriction['warnings']:
                whatsapp_text += f"⚠️ Importante: {restriction['warnings']}\n"
            
            whatsapp_text += "\n"
        
        return whatsapp_text