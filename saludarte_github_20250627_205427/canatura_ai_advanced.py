"""
SaludArte IA Avanzada - Sistema Expandido
Capacidades médicas avanzadas + Detección mejorada de síntomas
Basado en la versión estable v1.0 con mejoras significativas
"""

from canatura_ai import CanaturaAI
import pandas as pd
import logging
import re

class CanaturaAI_Advanced(CanaturaAI):
    """
    Versión avanzada del sistema SaludArte con:
    1. Capacidades médicas avanzadas
    2. Detección mejorada de síntomas múltiples y complejos
    3. Análisis contextual profundo
    4. Sistema de advertencias inteligente
    """
    
    def __init__(self):
        super().__init__()
        self.version = "Advanced-1.0"
        self.logger.info(f"✓ SaludArte IA {self.version} inicializado")
        
        # Mapeo expandido de condiciones médicas
        self.medical_conditions = self._build_advanced_medical_mapping()
        
        # Sistema de advertencias médicas
        self.medical_warnings = self._build_warning_system()
        
        # Patrones complejos de síntomas
        self.complex_symptom_patterns = self._build_complex_patterns()
        
        # Análisis contextual avanzado
        self.contextual_analyzers = self._build_contextual_analyzers()
    
    def _build_advanced_medical_mapping(self):
        """Mapeo avanzado de condiciones médicas específicas"""
        return {
            # SISTEMA RESPIRATORIO
            'infeccion_pulmonar': {
                'keywords': ['infección pulmonar', 'neumonía', 'bronquitis', 'pulmones infectados'],
                'symptoms': ['gripa', 'respiratorio'],
                'warning_level': 'medica_urgente',
                'description': 'Infección del sistema respiratorio que requiere atención médica'
            },
            'asma': {
                'keywords': ['asma', 'asmático', 'dificultad respirar', 'broncoespasmo'],
                'symptoms': ['respiratorio', 'gripa'],
                'warning_level': 'supervision_medica',
                'description': 'Condición respiratoria crónica'
            },
            
            # SISTEMA DIGESTIVO
            'gastritis_cronica': {
                'keywords': ['gastritis crónica', 'gastritis severa', 'úlcera gástrica'],
                'symptoms': ['acidez', 'dolor estomacal'],
                'warning_level': 'supervision_medica',
                'description': 'Inflamación crónica del estómago'
            },
            'colitis_ulcerosa': {
                'keywords': ['colitis ulcerosa', 'enfermedad inflamatoria intestinal'],
                'symptoms': ['digestion', 'inflamacion'],
                'warning_level': 'supervision_medica',
                'description': 'Enfermedad inflamatoria intestinal crónica'
            },
            
            # SISTEMA CARDIOVASCULAR
            'hipertension_arterial': {
                'keywords': ['hipertensión', 'presión alta', 'hipertensión arterial'],
                'symptoms': ['presion arterial'],
                'warning_level': 'supervision_medica',
                'description': 'Presión arterial elevada persistente'
            },
            'arritmia_cardiaca': {
                'keywords': ['arritmia', 'palpitaciones', 'corazón irregular'],
                'symptoms': ['circulacion'],
                'warning_level': 'medica_urgente',
                'description': 'Alteración del ritmo cardíaco'
            },
            
            # SISTEMA ENDOCRINO
            'diabetes_tipo2': {
                'keywords': ['diabetes tipo 2', 'diabetes mellitus', 'glucosa alta'],
                'symptoms': ['diabetes'],
                'warning_level': 'supervision_medica',
                'description': 'Trastorno metabólico del azúcar en sangre'
            },
            'hipotiroidismo': {
                'keywords': ['hipotiroidismo', 'tiroides lenta', 'hormona tiroidea baja'],
                'symptoms': ['cansancio', 'metabolismo'],
                'warning_level': 'supervision_medica',
                'description': 'Deficiencia de hormonas tiroideas'
            },
            
            # SISTEMA NERVIOSO
            'ansiedad_generalizada': {
                'keywords': ['ansiedad generalizada', 'trastorno de ansiedad', 'ataques de pánico'],
                'symptoms': ['estres', 'ansiedad'],
                'warning_level': 'complementaria',
                'description': 'Trastorno de ansiedad persistente'
            },
            'depresion_mayor': {
                'keywords': ['depresión mayor', 'depresión clínica', 'trastorno depresivo'],
                'symptoms': ['estres', 'cansancio'],
                'warning_level': 'supervision_medica',
                'description': 'Trastorno del estado de ánimo'
            },
            
            # SISTEMA MUSCULOESQUELÉTICO
            'artritis_reumatoide': {
                'keywords': ['artritis reumatoide', 'artritis autoinmune'],
                'symptoms': ['artritis', 'dolor articular'],
                'warning_level': 'supervision_medica',
                'description': 'Enfermedad autoinmune de las articulaciones'
            },
            'fibromialgia': {
                'keywords': ['fibromialgia', 'dolor muscular crónico'],
                'symptoms': ['dolor muscular', 'cansancio'],
                'warning_level': 'complementaria',
                'description': 'Síndrome de dolor muscular generalizado'
            },
            
            # CONDICIONES CRÍTICAS
            'tumor_maligno': {
                'keywords': ['tumor maligno', 'cáncer', 'carcinoma', 'neoplasia'],
                'symptoms': [],
                'warning_level': 'critica_urgente',
                'description': 'Crecimiento celular anormal maligno'
            },
            'infarto_miocardio': {
                'keywords': ['infarto', 'ataque cardíaco', 'dolor pecho severo'],
                'symptoms': [],
                'warning_level': 'emergencia_medica',
                'description': 'Emergencia cardiovascular grave'
            }
        }
    
    def _build_warning_system(self):
        """Sistema de advertencias médicas por niveles"""
        return {
            'emergencia_medica': {
                'message': '🚨 EMERGENCIA MÉDICA: Esta condición requiere atención médica INMEDIATA. Acuda al servicio de urgencias más cercano.',
                'show_products': False,
                'priority': 1
            },
            'critica_urgente': {
                'message': '⚠️ CONDICIÓN CRÍTICA: Esta condición requiere evaluación médica urgente. Consulte a un médico especialista inmediatamente.',
                'show_products': False,
                'priority': 2
            },
            'medica_urgente': {
                'message': '🏥 ATENCIÓN MÉDICA URGENTE: Esta condición requiere tratamiento médico profesional. Los productos naturales son solo complementarios.',
                'show_products': True,
                'priority': 3
            },
            'supervision_medica': {
                'message': '👩‍⚕️ SUPERVISIÓN MÉDICA: Esta condición requiere seguimiento médico. Los productos recomendados son complementarios al tratamiento.',
                'show_products': True,
                'priority': 4
            },
            'complementaria': {
                'message': '💡 TRATAMIENTO COMPLEMENTARIO: Esta condición puede beneficiarse de productos naturales como complemento. Se recomienda consultar con un profesional.',
                'show_products': True,
                'priority': 5
            }
        }
    
    def _build_complex_patterns(self):
        """Patrones complejos para detectar síntomas múltiples y contextuales"""
        return {
            'sindrome_metabolico': {
                'pattern': ['diabetes', 'colesterol', 'presion arterial', 'obesidad'],
                'min_symptoms': 2,
                'condition': 'síndrome metabólico',
                'warning': 'supervision_medica'
            },
            'menopausia_completa': {
                'pattern': ['sofocos', 'menopausia', 'insomnio', 'cambios hormonales'],
                'min_symptoms': 2,
                'condition': 'síndrome menopáusico',
                'warning': 'complementaria'
            },
            'estres_cronico': {
                'pattern': ['estres', 'ansiedad', 'insomnio', 'cansancio'],
                'min_symptoms': 3,
                'condition': 'estrés crónico',
                'warning': 'complementaria'
            },
            'sindrome_dolor_cronico': {
                'pattern': ['dolor muscular', 'dolor articular', 'cansancio', 'insomnio'],
                'min_symptoms': 3,
                'condition': 'síndrome de dolor crónico',
                'warning': 'supervision_medica'
            }
        }
    
    def _build_contextual_analyzers(self):
        """Analizadores contextuales avanzados"""
        return {
            'intensidad_dolor': {
                'leve': ['molestia', 'ligero', 'poco', 'leve'],
                'moderado': ['dolor', 'molesto', 'incómodo'],
                'severo': ['mucho dolor', 'insoportable', 'muy fuerte', 'intenso']
            },
            'frecuencia_sintoma': {
                'ocasional': ['a veces', 'ocasional', 'de vez en cuando'],
                'frecuente': ['frecuente', 'seguido', 'regular'],
                'constante': ['siempre', 'constante', 'todo el tiempo', 'crónico']
            },
            'duracion_sintoma': {
                'agudo': ['repentino', 'súbito', 'desde ayer', 'desde hoy'],
                'subagudo': ['desde hace días', 'esta semana'],
                'cronico': ['desde hace meses', 'años', 'crónico', 'siempre']
            }
        }
    
    def analyze_symptoms_advanced(self, user_input, user_profile=None):
        """
        Análisis avanzado de síntomas con detección de condiciones médicas
        """
        result = {
            'detected_symptoms': [],
            'medical_condition': None,
            'warning_level': None,
            'warning_message': '',
            'context_analysis': {},
            'recommendations': [],
            'complex_patterns': []
        }
        
        # 1. Detectar condiciones médicas específicas
        detected_condition = self._detect_medical_condition(user_input)
        if detected_condition:
            condition_info = self.medical_conditions[detected_condition]
            result['medical_condition'] = detected_condition
            result['warning_level'] = condition_info['warning_level']
            result['warning_message'] = self.medical_warnings[condition_info['warning_level']]['message']
            
            # Si es emergencia o crítica, no buscar productos
            if condition_info['warning_level'] in ['emergencia_medica', 'critica_urgente']:
                return result
        
        # 2. Detectar síntomas individuales (método mejorado)
        detected_symptoms = self._detect_symptoms_enhanced(user_input)
        result['detected_symptoms'] = detected_symptoms
        
        # 3. Análisis contextual avanzado
        result['context_analysis'] = self._analyze_context_advanced(user_input)
        
        # 4. Detectar patrones complejos
        complex_patterns = self._detect_complex_patterns(detected_symptoms)
        result['complex_patterns'] = complex_patterns
        
        # 5. Generar recomendaciones si es apropiado
        if not detected_condition or self.medical_warnings[result['warning_level']]['show_products']:
            # Usar síntomas de la condición médica o síntomas detectados
            symptoms_to_use = []
            if detected_condition:
                symptoms_to_use = self.medical_conditions[detected_condition]['symptoms']
            else:
                symptoms_to_use = detected_symptoms
            
            if symptoms_to_use:
                recommendations = self.find_products_for_symptoms(
                    ' '.join(symptoms_to_use), user_profile, 2, 2
                )
                result['recommendations'] = recommendations
        
        return result
    
    def _detect_medical_condition(self, user_input):
        """Detectar condiciones médicas específicas en el texto"""
        user_normalized = self._normalize_text(user_input)
        
        for condition, info in self.medical_conditions.items():
            for keyword in info['keywords']:
                if keyword.lower() in user_normalized:
                    self.logger.info(f"Condición médica detectada: {condition}")
                    return condition
        
        return None
    
    def _detect_symptoms_enhanced(self, user_input):
        """Detección mejorada de síntomas múltiples"""
        # Usar el método base mejorado
        base_symptoms = self._detect_symptoms(user_input)
        
        # Agregar detección de síntomas emocionales y contextuales
        emotional_symptoms = self._detect_emotional_symptoms(user_input)
        contextual_symptoms = self._detect_contextual_symptoms(user_input)
        
        # Combinar todos los síntomas detectados
        all_symptoms = list(set(base_symptoms + emotional_symptoms + contextual_symptoms))
        
        return all_symptoms
    
    def _detect_emotional_symptoms(self, user_input):
        """Detectar síntomas emocionales y psicológicos"""
        user_normalized = self._normalize_text(user_input)
        detected = []
        
        emotional_patterns = {
            'estres': [
                'estresado', 'me siento estresado', 'mucho estrés', 'presión emocional',
                'agobiado', 'abrumado', 'tensión emocional', 'sobrecargado'
            ],
            'ansiedad': [
                'ansioso', 'nervioso', 'preocupado', 'inquieto', 'angustiado',
                'ataques de pánico', 'miedo constante', 'nervios alterados'
            ],
            'tristeza': [
                'triste', 'deprimido', 'melancólico', 'sin ánimo', 'desanimado',
                'bajón emocional', 'estado de ánimo bajo'
            ],
            'irritabilidad': [
                'irritable', 'malhumorado', 'enojado', 'molesto', 'irascible',
                'mal genio', 'humor cambiante'
            ]
        }
        
        for symptom, patterns in emotional_patterns.items():
            if any(pattern in user_normalized for pattern in patterns):
                detected.append(symptom)
        
        return detected
    
    def _detect_contextual_symptoms(self, user_input):
        """Detectar síntomas basados en contexto específico"""
        user_normalized = self._normalize_text(user_input)
        detected = []
        
        contextual_patterns = {
            'insomnio_severo': [
                'no puedo dormir nada', 'insomnio total', 'no he dormido en días',
                'desvelo completo', 'sin dormir'
            ],
            'dolor_intenso': [
                'dolor insoportable', 'muchísimo dolor', 'dolor severo',
                'dolor muy fuerte', 'no aguanto el dolor'
            ],
            'fatiga_cronica': [
                'cansancio extremo', 'agotamiento total', 'sin energía para nada',
                'fatiga constante', 'siempre cansado'
            ]
        }
        
        for symptom, patterns in contextual_patterns.items():
            if any(pattern in user_normalized for pattern in patterns):
                # Mapear a síntomas base
                if 'insomnio' in symptom:
                    detected.append('insomnio')
                elif 'dolor' in symptom:
                    detected.append('dolor')
                elif 'fatiga' in symptom or 'cansancio' in symptom:
                    detected.append('cansancio')
        
        return detected
    
    def _analyze_context_advanced(self, user_input):
        """Análisis contextual avanzado del texto"""
        context = {
            'intensidad': 'moderado',
            'frecuencia': 'ocasional',
            'duracion': 'agudo',
            'urgencia': 'normal'
        }
        
        user_normalized = self._normalize_text(user_input)
        
        # Analizar intensidad
        for level, keywords in self.contextual_analyzers['intensidad_dolor'].items():
            if any(keyword in user_normalized for keyword in keywords):
                context['intensidad'] = level
                break
        
        # Analizar frecuencia
        for freq, keywords in self.contextual_analyzers['frecuencia_sintoma'].items():
            if any(keyword in user_normalized for keyword in keywords):
                context['frecuencia'] = freq
                break
        
        # Analizar duración
        for dur, keywords in self.contextual_analyzers['duracion_sintoma'].items():
            if any(keyword in user_normalized for keyword in keywords):
                context['duracion'] = dur
                break
        
        # Detectar urgencia
        urgency_keywords = ['urgente', 'inmediato', 'ahora', 'rápido', 'ya']
        if any(keyword in user_normalized for keyword in urgency_keywords):
            context['urgencia'] = 'alta'
        
        return context
    
    def _detect_complex_patterns(self, detected_symptoms):
        """Detectar patrones complejos de síntomas"""
        detected_patterns = []
        
        for pattern_name, pattern_info in self.complex_symptom_patterns.items():
            matching_symptoms = [s for s in detected_symptoms if s in pattern_info['pattern']]
            
            if len(matching_symptoms) >= pattern_info['min_symptoms']:
                detected_patterns.append({
                    'pattern': pattern_name,
                    'condition': pattern_info['condition'],
                    'matching_symptoms': matching_symptoms,
                    'warning': pattern_info['warning']
                })
        
        return detected_patterns
    
    def get_system_stats_advanced(self):
        """Estadísticas del sistema avanzado"""
        return {
            'version': self.version,
            'medical_conditions_supported': len(self.medical_conditions),
            'warning_levels': len(self.medical_warnings),
            'complex_patterns': len(self.complex_symptom_patterns),
            'contextual_analyzers': len(self.contextual_analyzers),
            'capabilities': [
                'Detección de condiciones médicas específicas',
                'Análisis contextual avanzado',
                'Detección de síntomas emocionales',
                'Patrones complejos de síntomas',
                'Sistema de advertencias médicas',
                'Recomendaciones contextuales'
            ]
        }

# Función para crear la instancia avanzada
def create_advanced_ai():
    """Crear instancia de SaludArte IA Avanzada"""
    return CanaturaAI_Advanced()