"""
SaludArte IA v2.0 - Versión Experimental
Sistema avanzado de recomendaciones con soporte expandido para condiciones médicas
Basado en la versión estable v1.0 (75% precisión)

NUEVAS CARACTERÍSTICAS EXPERIMENTALES:
- Reconocimiento de condiciones médicas específicas (tumores, infecciones, etc.)
- Mapeo expandido de enfermedades a productos
- Advertencias médicas cuando corresponde
- Sistema de retroalimentación de usuarios (preparado)
"""

from canatura_ai import CanaturaAI
import pandas as pd
import logging

class CanaturaAI_V2(CanaturaAI):
    """
    Versión experimental expandida del sistema SaludArte
    Hereda toda la funcionalidad estable de v1.0 y agrega nuevas capacidades
    """
    
    def __init__(self):
        super().__init__()
        self.version = "2.0-experimental"
        self.logger.info(f"✓ SaludArte IA v{self.version} inicializado")
        
        # Mapeo expandido de condiciones médicas específicas
        self.medical_conditions_mapping = self._build_medical_conditions_mapping()
        
        # Sistema de advertencias médicas
        self.medical_warnings = self._build_medical_warnings()
    
    def _build_medical_conditions_mapping(self):
        """Mapeo expandido de condiciones médicas específicas a síntomas tratables"""
        return {
            # CONDICIONES RESPIRATORIAS
            'infeccion pulmonar': ['gripa', 'respiratorio'],
            'neumonia': ['gripa', 'respiratorio'],
            'bronquitis': ['gripa', 'respiratorio'],
            'asma': ['respiratorio'],
            'tos persistente': ['gripa'],
            
            # CONDICIONES DIGESTIVAS
            'gastritis': ['acidez', 'dolor estomacal'],
            'ulcera': ['acidez', 'dolor estomacal'],
            'colitis': ['digestion', 'inflamacion'],
            'reflujo gastroesofagico': ['acidez'],
            'sindrome intestino irritable': ['digestion', 'gases'],
            
            # CONDICIONES HORMONALES/REPRODUCTIVAS
            'quistes ovaricos': ['quistes', 'ovarios'],
            'sindrome ovarios poliquisticos': ['quistes', 'ovarios'],
            'endometriosis': ['ovarios', 'dolor'],
            'menopausia': ['menopausia'],
            'sindrome premenstrual': ['ovarios'],
            'infertilidad': ['ovarios'],
            
            # CONDICIONES MUSCULOESQUELÉTICAS
            'artritis': ['artritis', 'dolor muscular'],
            'artrosis': ['artritis', 'dolor muscular'],
            'fibromialgia': ['dolor muscular', 'cansancio'],
            'lumbalgia': ['dolor muscular'],
            'cervicalgia': ['dolor muscular'],
            'contracturas': ['dolor muscular'],
            
            # CONDICIONES CARDIOVASCULARES
            'hipertension': ['presion arterial'],
            'presion alta': ['presion arterial'],
            'colesterol alto': ['colesterol'],
            'trigliceridos altos': ['colesterol'],
            'mala circulacion': ['circulacion'],
            
            # CONDICIONES NEUROLÓGICAS
            'migraña': ['dolor de cabeza'],
            'cefalea tensional': ['dolor de cabeza'],
            'insomnio cronico': ['insomnio'],
            'ansiedad': ['estres'],
            'depresion': ['estres'],
            'estres cronico': ['estres'],
            
            # CONDICIONES METABÓLICAS
            'diabetes tipo 2': ['diabetes'],
            'diabetes': ['diabetes'],
            'obesidad': ['peso'],
            'sindrome metabolico': ['diabetes', 'colesterol'],
            
            # CONDICIONES RENALES/URINARIAS
            'infeccion urinaria': ['riñones'],
            'cistitis': ['riñones'],
            'calculos renales': ['riñones'],
            'insuficiencia renal': ['riñones'],
            
            # CONDICIONES HEPÁTICAS
            'higado graso': ['higado'],
            'hepatitis': ['higado'],
            'cirrosis': ['higado'],
            
            # CONDICIONES DE LA PIEL
            'dermatitis': ['inflamacion'],
            'eczema': ['inflamacion'],
            'psoriasis': ['inflamacion'],
            'acne': ['inflamacion'],
            
            # CONDICIONES INMUNOLÓGICAS
            'defensas bajas': ['inmunidad'],
            'infecciones recurrentes': ['inmunidad'],
            'alergias': ['inmunidad'],
            'autoinmune': ['inmunidad'],
        }
    
    def _build_medical_warnings(self):
        """Sistema de advertencias médicas para condiciones serias"""
        return {
            # CONDICIONES QUE REQUIEREN SUPERVISIÓN MÉDICA URGENTE
            'criticas': [
                'tumor', 'cancer', 'carcinoma', 'metastasis',
                'infarto', 'derrame cerebral', 'embolia',
                'insuficiencia cardiaca', 'insuficiencia renal',
                'hepatitis aguda', 'pancreatitis'
            ],
            
            # CONDICIONES QUE REQUIEREN SEGUIMIENTO MÉDICO
            'supervision_medica': [
                'diabetes', 'hipertension', 'colesterol alto',
                'artritis reumatoide', 'lupus', 'esclerosis',
                'epilepsia', 'bipolaridad', 'esquizofrenia'
            ],
            
            # CONDICIONES TRATABLES CON PRODUCTOS NATURALES + SEGUIMIENTO
            'complementarias': [
                'gastritis', 'colitis', 'migraña', 'insomnio',
                'ansiedad leve', 'menopausia', 'quistes simples'
            ]
        }
    
    def detect_medical_condition(self, user_input):
        """
        Detecta condiciones médicas específicas en la entrada del usuario
        Devuelve la condición detectada y el nivel de advertencia
        """
        user_normalized = self._normalize_text(user_input)
        
        detected_condition = None
        warning_level = 'none'
        
        # Buscar condiciones médicas específicas
        for condition, symptoms in self.medical_conditions_mapping.items():
            if condition in user_normalized:
                detected_condition = condition
                
                # Determinar nivel de advertencia
                if any(critical in user_normalized for critical in self.medical_warnings['criticas']):
                    warning_level = 'critica'
                elif any(supervision in condition for supervision in self.medical_warnings['supervision_medica']):
                    warning_level = 'supervision_medica'
                elif condition in self.medical_warnings['complementarias']:
                    warning_level = 'complementaria'
                
                break
        
        return detected_condition, warning_level
    
    def find_products_for_medical_condition(self, condition, user_profile, min_products=2, max_products=2):
        """
        Encuentra productos para una condición médica específica
        """
        if condition not in self.medical_conditions_mapping:
            return []
        
        # Mapear la condición médica a síntomas tratables
        related_symptoms = self.medical_conditions_mapping[condition]
        
        # Usar el sistema existente para encontrar productos
        all_recommendations = []
        for symptom in related_symptoms:
            symptom_recommendations = self.find_products_for_symptoms(
                symptom, user_profile, min_products, max_products
            )
            all_recommendations.extend(symptom_recommendations)
        
        return all_recommendations
    
    def generate_medical_warning(self, condition, warning_level):
        """Genera advertencias médicas apropiadas según la condición"""
        
        warnings = {
            'critica': f"⚠️ IMPORTANTE: {condition.upper()} es una condición médica seria que requiere atención médica inmediata. Los productos naturales son complementarios al tratamiento médico profesional. Consulte a su médico urgentemente.",
            
            'supervision_medica': f"⚠️ NOTA MÉDICA: {condition.capitalize()} requiere seguimiento médico profesional. Los productos naturales recomendados son complementarios. Consulte con su médico antes de usar.",
            
            'complementaria': f"💡 INFORMACIÓN: {condition.capitalize()} puede beneficiarse de productos naturales como complemento. Recomendamos consultar con un profesional de la salud.",
            
            'none': ""
        }
        
        return warnings.get(warning_level, "")
    
    def find_products_for_symptoms_v2(self, user_input, user_profile=None, min_products=2, max_products=2):
        """
        Versión mejorada que maneja tanto síntomas como condiciones médicas específicas
        """
        # Primero detectar si hay una condición médica específica
        detected_condition, warning_level = self.detect_medical_condition(user_input)
        
        result = {
            'detected_condition': detected_condition,
            'warning_level': warning_level,
            'medical_warning': self.generate_medical_warning(detected_condition, warning_level),
            'recommendations': []
        }
        
        if detected_condition:
            # Si detectamos una condición médica específica
            self.logger.info(f"Condición médica detectada: {detected_condition} (nivel: {warning_level})")
            
            if warning_level == 'critica':
                # Para condiciones críticas, solo mostrar advertencia
                result['recommendations'] = []
                return result
            else:
                # Para otras condiciones, buscar productos apropiados
                recommendations = self.find_products_for_medical_condition(
                    detected_condition, user_profile, min_products, max_products
                )
                result['recommendations'] = recommendations
        else:
            # Si no hay condición médica específica, usar el sistema original
            recommendations = self.find_products_for_symptoms(
                user_input, user_profile, min_products, max_products
            )
            result['recommendations'] = recommendations
        
        return result
    
    def get_system_stats(self):
        """Estadísticas del sistema v2.0"""
        stats = super().get_system_stats() if hasattr(super(), 'get_system_stats') else {}
        
        stats.update({
            'version': self.version,
            'medical_conditions_supported': len(self.medical_conditions_mapping),
            'warning_levels': len(self.medical_warnings),
            'new_features': [
                'Condiciones médicas específicas',
                'Sistema de advertencias médicas',
                'Mapeo expandido de enfermedades'
            ]
        })
        
        return stats

# Función de conveniencia para usar la nueva versión
def create_ai_v2():
    """Crear instancia de SaludArte IA v2.0"""
    return CanaturaAI_V2()