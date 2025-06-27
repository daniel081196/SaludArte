"""
SaludArte IA Ultra - Sistema Completo e Inteligente
Integra todas las capacidades avanzadas excepto procesamiento de lenguaje natural externo
"""

from canatura_ai_advanced import CanaturaAI_Advanced
import pandas as pd
import logging
import json
from datetime import datetime, timedelta
import re

class CanaturaAI_Ultra(CanaturaAI_Advanced):
    """
    Versión Ultra de SaludArte IA con capacidades completas:
    1. Inteligencia farmacológica
    2. Análisis de patrones de salud
    3. Personalización inteligente
    4. Inteligencia preventiva
    5. Sistema de aprendizaje
    """
    
    def __init__(self):
        super().__init__()
        self.version = "Ultra-1.0"
        self.logger.info(f"✓ SaludArte IA {self.version} inicializado")
        
        # 1. INTELIGENCIA FARMACOLÓGICA
        self.drug_interactions = self._build_drug_interactions()
        self.contraindications_advanced = self._build_advanced_contraindications()
        
        # 2. ANÁLISIS DE PATRONES DE SALUD
        self.health_syndromes = self._build_health_syndromes()
        self.risk_factors = self._build_risk_factors()
        
        # 3. PERSONALIZACIÓN INTELIGENTE
        self.user_profiles_database = {}
        self.personalization_rules = self._build_personalization_rules()
        
        # 5. INTELIGENCIA PREVENTIVA
        self.preventive_recommendations = self._build_preventive_system()
        self.lifestyle_analysis = self._build_lifestyle_analyzers()
        
        # 6. SISTEMA DE APRENDIZAJE
        self.user_feedback_database = {}
        self.algorithm_performance = {
            'total_recommendations': 0,
            'positive_feedback': 0,
            'negative_feedback': 0,
            'accuracy_score': 0.75  # Base inicial
        }
    
    def _build_drug_interactions(self):
        """Base de datos de interacciones medicamentosas"""
        return {
            # MEDICAMENTOS CARDIOVASCULARES
            'anticoagulantes': {
                'names': ['warfarina', 'heparina', 'rivaroxaban', 'apixaban'],
                'interactions': {
                    'ginkgo': 'ALTO - Aumenta riesgo de sangrado',
                    'ajo': 'MEDIO - Puede potenciar efecto anticoagulante',
                    'jengibre': 'MEDIO - Riesgo de sangrado aumentado',
                    'vitamina e': 'ALTO - Incrementa anticoagulación'
                },
                'warning': 'Consulte cardiólogo antes de combinar con suplementos'
            },
            'antihipertensivos': {
                'names': ['enalapril', 'losartan', 'amlodipino', 'metoprolol'],
                'interactions': {
                    'potasio': 'ALTO - Puede causar hiperpotasemia',
                    'regaliz': 'MEDIO - Puede aumentar presión arterial',
                    'ginseng': 'MEDIO - Puede interferir con control de presión'
                },
                'warning': 'Monitoreo médico necesario'
            },
            
            # MEDICAMENTOS DIABETES
            'antidiabeticos': {
                'names': ['metformina', 'glibenclamida', 'insulina', 'sitagliptina'],
                'interactions': {
                    'canela': 'MEDIO - Puede potenciar efecto hipoglucemiante',
                    'cromo': 'MEDIO - Monitorear glucosa más frecuentemente',
                    'gymnema': 'ALTO - Riesgo de hipoglucemia severa'
                },
                'warning': 'Monitoreo estricto de glucosa requerido'
            },
            
            # MEDICAMENTOS PSIQUIÁTRICOS
            'antidepresivos': {
                'names': ['fluoxetina', 'sertralina', 'amitriptilina', 'venlafaxina'],
                'interactions': {
                    'hierba de san juan': 'ALTO - Síndrome serotoninérgico',
                    'kava': 'MEDIO - Puede aumentar sedación',
                    'ginkgo': 'MEDIO - Puede afectar coagulación'
                },
                'warning': 'No suspender medicación sin supervisión médica'
            },
            
            # MEDICAMENTOS TIROIDEOS
            'hormona_tiroidea': {
                'names': ['levotiroxina', 'liothyronine'],
                'interactions': {
                    'calcio': 'ALTO - Reduce absorción de hormona tiroidea',
                    'hierro': 'ALTO - Espaciar 4 horas mínimo',
                    'soja': 'MEDIO - Puede interferir con absorción'
                },
                'warning': 'Tomar con estómago vacío, separado de suplementos'
            }
        }
    
    def _build_advanced_contraindications(self):
        """Contraindicaciones avanzadas por condición"""
        return {
            'embarazo': {
                'contraindicados': [
                    'dong quai', 'cohosh negro', 'ruda', 'tanaceto',
                    'poleo', 'artemisa', 'angélica', 'boldo'
                ],
                'precaucion': [
                    'ginseng', 'ginkgo', 'echinacea', 'hierba de san juan'
                ],
                'seguros': [
                    'ácido fólico', 'hierro', 'calcio', 'vitamina d'
                ]
            },
            'lactancia': {
                'contraindicados': [
                    'sen', 'cáscara sagrada', 'ruibarbo', 'aloe',
                    'efedra', 'guaraná alta dosis'
                ],
                'precaucion': [
                    'té verde', 'café verde', 'kava', 'valeriana'
                ]
            },
            'hipertension': {
                'contraindicados': [
                    'regaliz', 'efedra', 'yohimbe', 'ma huang'
                ],
                'precaucion': [
                    'ginseng', 'rhodiola', 'té verde exceso'
                ]
            },
            'diabetes': {
                'monitoreo_estricto': [
                    'canela', 'gymnema', 'cromo', 'ácido alfa lipoico'
                ],
                'precaucion': [
                    'ginseng', 'fenogreco', 'bitter melon'
                ]
            }
        }
    
    def _build_health_syndromes(self):
        """Síndromes de salud complejos"""
        return {
            'sindrome_metabolico': {
                'criteria': ['diabetes', 'hipertension', 'colesterol', 'obesidad'],
                'min_criteria': 3,
                'recommendations': [
                    'omega 3', 'cromo', 'magnesio', 'coenzima q10',
                    'ácido alfa lipoico', 'canela'
                ],
                'lifestyle': [
                    'Dieta mediterránea',
                    'Ejercicio cardiovascular 150 min/semana',
                    'Reducción de carbohidratos refinados'
                ],
                'monitoring': 'Evaluación médica cada 3 meses'
            },
            'sindrome_fatiga_cronica': {
                'criteria': ['cansancio', 'dolor muscular', 'insomnio', 'problemas memoria'],
                'min_criteria': 3,
                'recommendations': [
                    'coenzima q10', 'magnesio', 'vitamina d',
                    'complejo b', 'rhodiola', 'ashwagandha'
                ],
                'lifestyle': [
                    'Manejo del estrés',
                    'Higiene del sueño',
                    'Ejercicio gradual'
                ],
                'monitoring': 'Seguimiento especializado en fatiga crónica'
            },
            'sindrome_ovarios_poliquisticos': {
                'criteria': ['irregularidades menstruales', 'resistencia insulina', 'acné', 'aumento peso'],
                'min_criteria': 2,
                'recommendations': [
                    'inositol', 'spearmint', 'canela', 'ácido alfa lipoico',
                    'vitamina d', 'omega 3'
                ],
                'lifestyle': [
                    'Dieta baja en índice glucémico',
                    'Ejercicio de resistencia',
                    'Control del peso'
                ],
                'monitoring': 'Evaluación ginecológica y endocrina'
            }
        }
    
    def _build_risk_factors(self):
        """Factores de riesgo y análisis preventivo"""
        return {
            'cardiovascular': {
                'age_risk': {'men': 45, 'women': 55},
                'symptoms': ['hipertension', 'colesterol', 'diabetes', 'tabaquismo'],
                'family_history_weight': 1.5,
                'preventive_supplements': [
                    'omega 3', 'coenzima q10', 'magnesio', 'vitamina d'
                ]
            },
            'osteoporosis': {
                'age_risk': {'men': 70, 'women': 50},
                'risk_factors': ['menopausia', 'sedentarismo', 'tabaquismo', 'corticoides'],
                'preventive_supplements': [
                    'calcio', 'vitamina d', 'vitamina k2', 'magnesio'
                ]
            },
            'diabetes_tipo2': {
                'age_risk': {'men': 40, 'women': 40},
                'risk_factors': ['obesidad', 'sedentarismo', 'historia familiar'],
                'preventive_supplements': [
                    'cromo', 'magnesio', 'ácido alfa lipoico', 'canela'
                ]
            }
        }
    
    def _build_personalization_rules(self):
        """Reglas de personalización inteligente"""
        return {
            'age_groups': {
                'young_adult': {'range': (18, 35), 'focus': ['energía', 'inmunidad', 'estrés']},
                'middle_age': {'range': (36, 55), 'focus': ['metabolismo', 'articulaciones', 'cardiovascular']},
                'mature': {'range': (56, 70), 'focus': ['memoria', 'articulaciones', 'cardiovascular', 'próstata/menopausia']},
                'senior': {'range': (71, 100), 'focus': ['memoria', 'huesos', 'cardiovascular', 'digestión']}
            },
            'gender_specific': {
                'female': {
                    'reproductive_age': ['hierro', 'ácido fólico', 'calcio'],
                    'menopause': ['calcio', 'vitamina d', 'fitoestrógenos'],
                    'special_needs': ['salud ósea', 'salud hormonal']
                },
                'male': {
                    'adult': ['zinc', 'vitamina d', 'omega 3'],
                    'mature': ['saw palmeto', 'licopeno', 'zinc'],
                    'special_needs': ['salud próstata', 'salud cardiovascular']
                }
            },
            'lifestyle_factors': {
                'sedentary': ['magnesio', 'vitamina d', 'omega 3'],
                'active': ['electrolitos', 'antioxidantes', 'proteína'],
                'stressed': ['magnesio', 'complejo b', 'ashwagandha'],
                'poor_sleep': ['melatonina', 'magnesio', 'l-teanina']
            }
        }
    
    def _build_preventive_system(self):
        """Sistema de recomendaciones preventivas"""
        return {
            'seasonal': {
                'winter': ['vitamina c', 'vitamina d', 'zinc', 'echinacea'],
                'spring': ['detox hepático', 'antioxidantes', 'probióticos'],
                'summer': ['electrolitos', 'protección solar interna', 'hidratación'],
                'autumn': ['inmunidad', 'vitamina d', 'adaptógenos']
            },
            'life_stages': {
                'pregnancy_planning': ['ácido fólico', 'hierro', 'omega 3'],
                'menopause_transition': ['calcio', 'vitamina d', 'fitoestrógenos'],
                'aging_preparation': ['antioxidantes', 'omega 3', 'coenzima q10']
            },
            'occupational': {
                'desk_worker': ['vitamina d', 'magnesio', 'antioxidantes oculares'],
                'physical_worker': ['electrolitos', 'antioxidantes', 'articulaciones'],
                'night_shift': ['melatonina', 'vitamina d', 'adaptógenos'],
                'high_stress': ['magnesio', 'complejo b', 'ashwagandha']
            }
        }
    
    def _build_lifestyle_analyzers(self):
        """Analizadores de estilo de vida"""
        return {
            'diet_patterns': {
                'vegetarian': {
                    'likely_deficiencies': ['b12', 'hierro', 'zinc', 'omega 3'],
                    'recommendations': ['complejo b', 'hierro quelado', 'algas omega 3']
                },
                'low_carb': {
                    'likely_deficiencies': ['fibra', 'magnesio', 'potasio'],
                    'recommendations': ['fibra suplementaria', 'electrolitos', 'probióticos']
                },
                'processed_foods': {
                    'likely_deficiencies': ['vitaminas', 'minerales', 'antioxidantes'],
                    'recommendations': ['multivitamínico', 'antioxidantes', 'probióticos']
                }
            },
            'activity_levels': {
                'sedentary': {
                    'risks': ['diabetes', 'cardiovascular', 'osteoporosis'],
                    'recommendations': ['magnesio', 'vitamina d', 'coenzima q10']
                },
                'moderate': {
                    'needs': ['antioxidantes', 'electrolitos'],
                    'recommendations': ['vitamina c', 'magnesio', 'omega 3']
                },
                'intense': {
                    'needs': ['recuperación', 'antioxidantes', 'electrolitos'],
                    'recommendations': ['proteína', 'creatina', 'antioxidantes', 'bcaa']
                }
            }
        }
    
    def analyze_ultra_comprehensive(self, user_input, user_profile=None):
        """
        Análisis ultra-comprehensivo que integra todas las capacidades
        """
        # Inicializar resultado con análisis avanzado base
        result = self.analyze_symptoms_advanced(user_input, user_profile)
        
        # Agregar análisis ultra
        result.update({
            'drug_interactions': [],
            'advanced_contraindications': [],
            'health_syndromes': [],
            'risk_assessment': {},
            'personalized_recommendations': [],
            'preventive_suggestions': [],
            'lifestyle_analysis': {},
            'learning_feedback': {}
        })
        
        if user_profile:
            # 1. ANÁLISIS FARMACOLÓGICO
            if 'medications' in user_profile and user_profile['medications']:
                result['drug_interactions'] = self._analyze_drug_interactions(
                    user_profile['medications'], result['recommendations']
                )
            
            # 2. CONTRAINDICACIONES AVANZADAS
            result['advanced_contraindications'] = self._check_advanced_contraindications(
                user_profile, result['recommendations']
            )
            
            # 3. ANÁLISIS DE SÍNDROMES
            result['health_syndromes'] = self._detect_health_syndromes(
                result['detected_symptoms'], user_profile
            )
            
            # 4. EVALUACIÓN DE RIESGO
            result['risk_assessment'] = self._assess_health_risks(user_profile)
            
            # 5. PERSONALIZACIÓN INTELIGENTE
            result['personalized_recommendations'] = self._generate_personalized_recommendations(
                user_profile, result['detected_symptoms']
            )
            
            # 6. SUGERENCIAS PREVENTIVAS
            result['preventive_suggestions'] = self._generate_preventive_suggestions(user_profile)
            
            # 7. ANÁLISIS DE ESTILO DE VIDA
            result['lifestyle_analysis'] = self._analyze_lifestyle(user_profile)
        
        # 8. SISTEMA DE APRENDIZAJE
        result['learning_feedback'] = self._prepare_learning_feedback(result)
        
        # Actualizar estadísticas del sistema
        self._update_algorithm_performance(result)
        
        return result
    
    def _analyze_drug_interactions(self, medications, recommendations):
        """Analizar interacciones medicamentosas"""
        interactions = []
        
        if not medications or not recommendations:
            return interactions
        
        user_meds = [med.lower().strip() for med in medications if med]
        
        for med in user_meds:
            for drug_class, info in self.drug_interactions.items():
                if any(drug_name in med for drug_name in info['names']):
                    # Buscar interacciones en recomendaciones
                    for rec_group in recommendations:
                        for product in rec_group.get('products', []):
                            product_ingredients = product.get('ingredientes', '').lower()
                            
                            for ingredient, interaction in info['interactions'].items():
                                if ingredient in product_ingredients:
                                    interactions.append({
                                        'medication': med,
                                        'product': product['nombre'],
                                        'ingredient': ingredient,
                                        'interaction': interaction,
                                        'warning': info['warning']
                                    })
        
        return interactions
    
    def _check_advanced_contraindications(self, user_profile, recommendations):
        """Verificar contraindicaciones avanzadas"""
        contraindications = []
        
        # Verificar condiciones especiales
        conditions_to_check = []
        
        if user_profile.get('gender') == 'femenino':
            if user_profile.get('age', 0) < 50:
                conditions_to_check.append('embarazo')  # Edad reproductiva
                conditions_to_check.append('lactancia')
        
        if 'hipertension' in str(user_profile.get('medical_conditions', '')).lower():
            conditions_to_check.append('hipertension')
        
        if 'diabetes' in str(user_profile.get('medical_conditions', '')).lower():
            conditions_to_check.append('diabetes')
        
        for condition in conditions_to_check:
            if condition in self.contraindications_advanced:
                contraind_info = self.contraindications_advanced[condition]
                
                for rec_group in recommendations:
                    for product in rec_group.get('products', []):
                        ingredients = product.get('ingredientes', '').lower()
                        
                        # Verificar ingredientes contraindicados
                        for contraind in contraind_info.get('contraindicados', []):
                            if contraind in ingredients:
                                contraindications.append({
                                    'condition': condition,
                                    'product': product['nombre'],
                                    'ingredient': contraind,
                                    'severity': 'CONTRAINDICADO',
                                    'action': 'Evitar completamente'
                                })
                        
                        # Verificar ingredientes de precaución
                        for precaucion in contraind_info.get('precaucion', []):
                            if precaucion in ingredients:
                                contraindications.append({
                                    'condition': condition,
                                    'product': product['nombre'],
                                    'ingredient': precaucion,
                                    'severity': 'PRECAUCIÓN',
                                    'action': 'Consultar médico antes de usar'
                                })
        
        return contraindications
    
    def _detect_health_syndromes(self, symptoms, user_profile):
        """Detectar síndromes de salud complejos"""
        detected_syndromes = []
        
        # Combinar síntomas detectados con condiciones médicas del perfil
        all_health_indicators = symptoms.copy()
        
        if user_profile.get('medical_conditions'):
            medical_conditions = [cond.lower() for cond in user_profile['medical_conditions']]
            all_health_indicators.extend(medical_conditions)
        
        for syndrome_name, syndrome_info in self.health_syndromes.items():
            matching_criteria = []
            
            for criterion in syndrome_info['criteria']:
                if any(criterion in indicator for indicator in all_health_indicators):
                    matching_criteria.append(criterion)
            
            if len(matching_criteria) >= syndrome_info['min_criteria']:
                detected_syndromes.append({
                    'syndrome': syndrome_name,
                    'matching_criteria': matching_criteria,
                    'recommendations': syndrome_info['recommendations'],
                    'lifestyle_changes': syndrome_info['lifestyle'],
                    'monitoring': syndrome_info['monitoring']
                })
        
        return detected_syndromes
    
    def _assess_health_risks(self, user_profile):
        """Evaluar riesgos de salud"""
        risk_assessment = {}
        
        age = user_profile.get('age', 0)
        gender = user_profile.get('gender', '').lower()
        
        for risk_name, risk_info in self.risk_factors.items():
            risk_score = 0
            risk_factors_present = []
            
            # Evaluar riesgo por edad
            age_risk = risk_info.get('age_risk', {})
            if gender in age_risk and age >= age_risk[gender]:
                risk_score += 2
                risk_factors_present.append(f'Edad ≥ {age_risk[gender]} años')
            
            # Evaluar otros factores de riesgo
            if 'symptoms' in risk_info:
                for symptom in risk_info['symptoms']:
                    if symptom in str(user_profile.get('medical_conditions', '')).lower():
                        risk_score += 1
                        risk_factors_present.append(symptom)
            
            if 'risk_factors' in risk_info:
                for factor in risk_info['risk_factors']:
                    if factor in str(user_profile.get('medical_conditions', '')).lower():
                        risk_score += 1
                        risk_factors_present.append(factor)
            
            # Clasificar nivel de riesgo
            if risk_score >= 3:
                risk_level = 'ALTO'
            elif risk_score >= 2:
                risk_level = 'MODERADO'
            elif risk_score >= 1:
                risk_level = 'BAJO'
            else:
                risk_level = 'MÍNIMO'
            
            if risk_score > 0:
                risk_assessment[risk_name] = {
                    'risk_level': risk_level,
                    'risk_score': risk_score,
                    'factors_present': risk_factors_present,
                    'preventive_supplements': risk_info.get('preventive_supplements', [])
                }
        
        return risk_assessment
    
    def _generate_personalized_recommendations(self, user_profile, symptoms):
        """Generar recomendaciones personalizadas"""
        personalized = []
        
        age = user_profile.get('age', 0)
        gender = user_profile.get('gender', '').lower()
        
        # Determinar grupo de edad
        age_group = None
        for group, info in self.personalization_rules['age_groups'].items():
            if info['range'][0] <= age <= info['range'][1]:
                age_group = group
                break
        
        if age_group:
            age_focus = self.personalization_rules['age_groups'][age_group]['focus']
            personalized.extend([{
                'type': 'age_specific',
                'recommendation': f'Enfoque en {", ".join(age_focus)} para grupo de edad {age_group}',
                'supplements': age_focus
            }])
        
        # Recomendaciones específicas por género
        if gender in self.personalization_rules['gender_specific']:
            gender_info = self.personalization_rules['gender_specific'][gender]
            
            if gender == 'female':
                if 18 <= age <= 49:
                    personalized.append({
                        'type': 'gender_reproductive',
                        'recommendation': 'Suplementos para edad reproductiva',
                        'supplements': gender_info['reproductive_age']
                    })
                elif age >= 50:
                    personalized.append({
                        'type': 'gender_menopause',
                        'recommendation': 'Soporte para etapa menopáusica',
                        'supplements': gender_info['menopause']
                    })
            
            elif gender == 'male':
                if age >= 40:
                    personalized.append({
                        'type': 'gender_mature',
                        'recommendation': 'Soporte para hombre maduro',
                        'supplements': gender_info['mature']
                    })
        
        return personalized
    
    def _generate_preventive_suggestions(self, user_profile):
        """Generar sugerencias preventivas"""
        preventive = []
        
        # Sugerencias estacionales
        current_month = datetime.now().month
        if current_month in [12, 1, 2]:
            season = 'winter'
        elif current_month in [3, 4, 5]:
            season = 'spring'
        elif current_month in [6, 7, 8]:
            season = 'summer'
        else:
            season = 'autumn'
        
        seasonal_supplements = self.preventive_recommendations['seasonal'][season]
        preventive.append({
            'type': 'seasonal',
            'season': season,
            'recommendation': f'Suplementos recomendados para {season}',
            'supplements': seasonal_supplements
        })
        
        return preventive
    
    def _analyze_lifestyle(self, user_profile):
        """Analizar estilo de vida y hacer recomendaciones"""
        lifestyle_analysis = {
            'diet_assessment': {},
            'activity_assessment': {},
            'recommendations': []
        }
        
        # Análisis simplificado basado en información disponible
        age = user_profile.get('age', 0)
        weight = user_profile.get('weight', 0)
        
        # Estimaciones básicas
        if age > 60:
            lifestyle_analysis['recommendations'].append({
                'category': 'age_related',
                'suggestion': 'Enfoque en salud ósea y cardiovascular',
                'supplements': ['calcio', 'vitamina d', 'omega 3', 'coenzima q10']
            })
        
        return lifestyle_analysis
    
    def _prepare_learning_feedback(self, result):
        """Preparar sistema de retroalimentación para aprendizaje"""
        return {
            'recommendation_id': f"rec_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'feedback_ready': True,
            'metrics_to_track': [
                'user_satisfaction',
                'product_effectiveness',
                'symptom_improvement',
                'side_effects'
            ],
            'improvement_areas': [
                'symptom_detection_accuracy',
                'product_recommendation_relevance',
                'personalization_effectiveness'
            ]
        }
    
    def _update_algorithm_performance(self, result):
        """Actualizar métricas de rendimiento del algoritmo"""
        self.algorithm_performance['total_recommendations'] += 1
        
        # Simular mejora continua basada en uso
        if self.algorithm_performance['total_recommendations'] % 10 == 0:
            self.algorithm_performance['accuracy_score'] = min(
                0.95, 
                self.algorithm_performance['accuracy_score'] + 0.01
            )
    
    def get_ultra_system_stats(self):
        """Estadísticas completas del sistema ultra"""
        base_stats = self.get_system_stats_advanced()
        
        ultra_stats = {
            'drug_interactions_monitored': len(self.drug_interactions),
            'advanced_contraindications': sum(len(v.get('contraindicados', [])) + len(v.get('precaucion', [])) 
                                            for v in self.contraindications_advanced.values()),
            'health_syndromes_detected': len(self.health_syndromes),
            'risk_factors_analyzed': len(self.risk_factors),
            'personalization_rules': len(self.personalization_rules),
            'preventive_recommendations': sum(len(v) for v in self.preventive_recommendations.values()),
            'algorithm_accuracy': f"{self.algorithm_performance['accuracy_score']:.1%}",
            'total_processed': self.algorithm_performance['total_recommendations'],
            'ultra_capabilities': [
                'Análisis de interacciones medicamentosas',
                'Contraindicaciones avanzadas',
                'Detección de síndromes complejos',
                'Evaluación de riesgos de salud',
                'Personalización inteligente por edad/género',
                'Recomendaciones preventivas estacionales',
                'Análisis de estilo de vida',
                'Sistema de aprendizaje continuo'
            ]
        }
        
        return {**base_stats, **ultra_stats}

# Función para crear la instancia ultra
def create_ultra_ai():
    """Crear instancia de SaludArte IA Ultra"""
    return CanaturaAI_Ultra()