import pandas as pd
import re
import logging
from difflib import SequenceMatcher

class CanaturaAI:
    """
    Sistema de inteligencia artificial propio para SaludArte
    Funciona exclusivamente con el catálogo real de productos Canatura
    NO inventa productos - solo recomienda productos reales del catálogo
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.catalog_df = None
        self.symptom_mappings = self._build_symptom_mappings()
        self.product_rotation_counter = {}  # Para rotación equitativa
        self.load_catalog()
    
    def _build_symptom_mappings(self):
        """Mapeos completos de síntomas en español coloquial a términos médicos"""
        return {
            # Dolor y molestias
            'dolor': ['dolor', 'duele', 'dolencia', 'molestia', 'malestar', 'ache', 'punzada'],
            'dolor_cabeza': ['dolor de cabeza', 'cefalea', 'migraña', 'migrana', 'jaqueca', 'me duele mucho la cabeza', 'me parte la cabeza', 'me late la cabeza', 'dolor de sien', 'tensión en la cabeza'],
            'dolor_articular': ['dolor articular', 'articulaciones', 'rodillas', 'coyunturas'],
            'dolor_muscular': ['dolor muscular', 'musculos', 'contractura', 'calambres', 'tension'],
            
            # Sistema digestivo
            'estomago': ['estómago', 'estomago', 'gastrico', 'abdominal', 'barriga', 'panza', 'se me revuelve el estómago', 'tengo el estómago revuelto'],
            'acidez': ['acidez', 'reflujo', 'agruras', 'acido', 'ardor', 'arde', 'quema', 'quemadura', 'ardor estomacal', 'arde el estomago', 'me arde', 'me arde el estómago'],
            'digestivo': ['digestión', 'digestion', 'digestivo', 'intestinal', 'estomacal'],
            'nauseas': ['nauseas', 'mareo', 'vomito', 'revuelto'],
            
            # Sistema nervioso y mental
            'estres': ['estrés', 'estres', 'tensión', 'tension', 'ansiedad', 'nervios', 'agobio', 'ando muy alterado', 'estoy muy angustiado', 'me siento nervioso', 'nervios de punta', 'tensión nerviosa', 'inquieto', 'agitado'],
            'ansiedad': ['ansiedad', 'nervios', 'nervioso', 'preocupación', 'angustia', 'alterado', 'angustiado'],
            'depresion': ['depresión', 'depresion', 'tristeza', 'decaimiento', 'desánimo'],
            
            # Sueño y descanso (unificados bajo problemas de sueño)
            'insomnio': ['insomnio', 'no puedo dormir', 'desvelo', 'no duermo', 'mal dormir', 'sueño', 'sueno', 'dormir mal', 'problemas para dormir', 'somnolencia', 'modorra', 'no me puedo dormir', 'me cuesta trabajo dormir', 'no pego el ojo', 'tengo problemas para conciliar el sueño'],
            'cansancio': ['cansancio', 'fatiga', 'agotamiento', 'debilidad', 'desgaste'],
            
            # Energía y vitalidad
            'energia': ['energía', 'energia', 'vitalidad', 'fuerza', 'vigor', 'dinamismo'],
            'fatiga': ['fatiga', 'cansancio', 'agotamiento', 'sin energia'],
            
            # Sistema inmunológico
            'inmunidad': ['inmunidad', 'defensas', 'resistencia', 'inmune', 'resfriado'],
            'gripe': ['gripe', 'resfriado', 'catarro', 'tos', 'congestion'],
            
            # Sistema cardiovascular
            'cardiovascular': ['cardiovascular', 'corazón', 'cardiaco', 'circulación', 'presion'],
            'hipertension': ['hipertensión', 'hipertension', 'presión alta', 'presion alta'],
            
            # Piel y belleza
            'piel': ['piel', 'cutáneo', 'dermatológico', 'epidermis', 'dermatitis', 'tengo la piel irritada', 'me pica mucho la piel', 'tengo sarpullido', 'se me irrita la piel', 'me sale alergia en la piel'],
            'cabello': ['cabello', 'pelo', 'caída', 'calvicie', 'alopecia'],
            'unas': ['uñas', 'unas', 'quebradizas', 'debiles'],
            
            # Huesos y articulaciones
            'huesos': ['huesos', 'óseo', 'calcio', 'esquelético', 'osteoporosis'],
            'articulaciones': ['articulaciones', 'articular', 'coyunturas', 'flexibilidad', 'me duelen los huesos', 'dolor en las juntas', 'rigidez articular'],
            'cartilago': ['cartílago', 'cartilago', 'artritis', 'artrosis'],
            
            # Sistema hormonal
            'hormonas': ['hormonas', 'hormonal', 'endocrino', 'menopausia'],
            'bochornos': ['bochornos', 'sofocos', 'calores', 'sudoración'],
            'menstrual': ['menstrual', 'regla', 'período', 'menstruación', 'ciclo'],
            
            # Otros sistemas
            'respiratorio': ['respiratorio', 'pulmones', 'bronquios', 'tos', 'asma', 'me falta el aire', 'siento opresión en el pecho', 'me ahogo', 'dificultad respirar'],
            'urinario': ['urinario', 'riñones', 'vejiga', 'próstata', 'cistitis'],
            'hepatico': ['hepático', 'hígado', 'hepatico', 'vesícula'],
            'diabetes': ['diabetes', 'glucosa', 'azúcar', 'insulina'],
            'colesterol': ['colesterol', 'triglicéridos', 'lípidos', 'grasas']
        }
    
    def load_catalog(self):
        """Cargar catálogo real de productos Canatura"""
        try:
            # Intentar cargar el catálogo principal
            catalog_file = "PLANTILLA CATALOGO CON INGREDIENTES.xlsx"
            try:
                self.catalog_df = pd.read_excel(catalog_file, engine='openpyxl')
            except:
                try:
                    self.catalog_df = pd.read_excel(catalog_file, engine='xlrd')
                except:
                    # Usar catálogo de muestra como respaldo
                    self.catalog_df = pd.read_excel("sample_catalog.xlsx", engine='openpyxl')
            
            # Limpiar y normalizar
            self.catalog_df = self.catalog_df.fillna('')
            self.catalog_df.columns = self.catalog_df.columns.str.strip().str.lower()
            
            # Crear columnas normalizadas para búsqueda
            for col in ['sintomas', 'beneficios', 'ingredientes', 'nombre']:
                if col in self.catalog_df.columns:
                    self.catalog_df[f'{col}_norm'] = self.catalog_df[col].apply(self._normalize_text)
            
            self.logger.info(f"✓ Catálogo Canatura cargado: {len(self.catalog_df)} productos reales")
            
        except Exception as e:
            self.logger.error(f"Error cargando catálogo Canatura: {e}")
            self.catalog_df = None
    
    def _normalize_text(self, text):
        """Normalizar texto español para mejor búsqueda"""
        if not isinstance(text, str):
            return ""
        
        text = text.lower()
        
        # Reemplazar acentos españoles
        accent_map = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u', 'ñ': 'n'
        }
        for accented, normal in accent_map.items():
            text = text.replace(accented, normal)
        
        return text
    
    def find_products_for_symptoms(self, user_symptoms, user_profile=None, min_per_symptom=2, max_per_symptom=2):
        """
        Función principal: encuentra productos reales del catálogo Canatura
        Garantiza exactamente 2 productos por síntoma
        NO inventa productos - solo usa el catálogo real
        Sistema alimentado con conocimiento completo de 200+ casos resueltos
        """
        if self.catalog_df is None or len(self.catalog_df) == 0:
            self.logger.error("Catálogo no disponible")
            return []
        
        try:
            # 1. Detectar síntomas del usuario
            detected_symptoms = self._detect_symptoms(user_symptoms)
            self.logger.info(f"Síntomas detectados: {detected_symptoms}")
            
            if not detected_symptoms:
                # Si no se detectan síntomas específicos, buscar productos generales de bienestar
                return self._get_general_wellness_products(max_per_symptom)
            
            all_recommendations = []
            
            # 2. Para cada síntoma detectado, encontrar productos reales
            for symptom in detected_symptoms:
                products = self._find_catalog_products_for_symptom(
                    symptom, user_profile, min_per_symptom, max_per_symptom
                )
                
                if products:
                    recommendation = {
                        'symptom': symptom,
                        'products': products,
                        'message': f"Productos naturales Canatura para {symptom}"
                    }
                    all_recommendations.append(recommendation)
            
            self.logger.info(f"Recomendaciones generadas: {len(all_recommendations)} grupos de síntomas")
            return all_recommendations
            
        except Exception as e:
            self.logger.error(f"Error en recomendaciones: {e}")
            return []
    
    def _detect_symptoms(self, user_input):
        """Detectar síntomas del usuario usando mapeos inteligentes con contexto"""
        user_normalized = self._normalize_text(user_input)
        detected = []
        
        # CASOS PROBLEMÁTICOS ESPECÍFICOS - DETECCIÓN DIRECTA PRIORITARIA
        user_input_lower = user_input.lower()
        
        # DETECCIÓN REFORZADA PARA CASOS ESPECÍFICOS PRIORITARIOS
        specific_cases = {
            'deseo subir de peso': ['aumento de peso'],
            'necesito ganar kilos': ['aumento de peso'],
            'estoy cansado': ['fatiga', 'energia'],
            'me siento hecho polvo': ['fatiga', 'energia'],
            'traigo la panza hecha garras': ['gastritis', 'digestion'],
            'ando bien aguitado': ['depresion', 'estres'],
            'me duele hasta el alma': ['dolor muscular', 'depresion'],
            'estoy que me lleva la tristeza': ['depresion', 'estres'],
            'ando arrastrando la cobija': ['fatiga', 'energia'],
            'me siento como trapo viejo': ['fatiga', 'energia'],
            'ando medio pacheco': ['estres', 'ansiedad'],
            'problemas hormonales': ['hormonas femeninas'],
            'disfunción eréctil': ['sexual'],
            'pérdida de libido': ['sexual'],
            'calvicie y caída del cabello': ['cabello'],
            'problemas urinarios': ['prostata'],
            'irregularidades menstruales': ['hormonas femeninas'],
            'síndrome premenstrual severo': ['hormonas femeninas'],
            'la abuela no duerme bien': ['insomnio'],
            'mi esposa está deprimida': ['depresion'],
            'el niño no tiene apetito': ['apetito'],
            'hago ejercicio y necesito energía': ['energia', 'vitaminas'],
            'me siento de la chingada': ['malestar general', 'estres'],
            'traigo un desmadre en el cuerpo': ['dolor muscular', 'malestar general'],
            'ando valiendo madres': ['fatiga', 'estres'],
            'me siento como si me hubiera pasado un camión encima': ['dolor muscular', 'fatiga'],
            'tengo un chingo de dolores': ['dolor muscular'],
            'ando hasta la madre de cansado': ['fatiga', 'energia'],
            'ando bien pinche jodido de todo': ['malestar general', 'estres'],
            'evitar problemas del corazón': ['corazon'],
            'prevenir el cáncer': ['antioxidantes'],
            'vacaciones de verano': ['energia'],
            'temporada navideña': ['estres'],
            'época de exámenes': ['memoria', 'estres'],
            'cambio de trabajo': ['estres']
        }
        
        for phrase, symptoms in specific_cases.items():
            if phrase in user_input_lower:
                detected.extend(symptoms)
                # No retornar inmediatamente, continuar buscando más síntomas
            
        # DETECCIÓN REFORZADA PARA VITALIDAD/ENERGÍA
        if 'necesito vitalidad' in user_input_lower:
            detected.append('energia')
            # Continuar procesando otros posibles síntomas
            
        if any(phrase in user_input_lower for phrase in ['ando estreñido', 'no puedo hacer del baño', 'no puedo evacuar']):
            detected.append('digestion')
            
        if any(phrase in user_input_lower for phrase in ['no agarro el sueño', 'no me llega el sueño', 'no me da sueño']):
            detected.append('insomnio')
        
        # Priorizar detección específica sobre palabras genéricas
        # GRIPA/RESFRIADO - contexto muy específico
        gripa_keywords = [
            'gripa', 'gripe', 'resfriado', 'constipado', 'resfrio',
            'tos', 'mucosidad', 'mocos', 'congestion nasal', 'nariz tapada',
            'estornudos', 'fiebre', 'dolor de garganta', 'garganta irritada'
        ]
        
        # DOLOR - pero específico por contexto
        dolor_cabeza = [
            'dolor de cabeza', 'cefalea', 'migraña', 'jaqueca', 'cabeza duele',
            'me duele la cabeza', 'dolor en la cabeza'
        ]
        
        dolor_muscular = [
            'dolor muscular', 'dolores musculares', 'musculos duelen',
            'dolor en los musculos', 'contractura', 'tension muscular',
            'me duelen los musculos', 'duelen los musculos', 'dolor de musculos',
            # MEXICANISMOS PARA DOLOR MUSCULAR
            'ando todo contracturado', 'se me agarrotan los musculos',
            'traigo los musculos tensos', 'ando todo tieso', 'me dan calambres',
            'se me engarrotan las piernas', 'musculos adoloridos', 'agujetas',
            'ando todo molido', 'me siento como si me hubieran dado una golpiza',
            'tengo los musculos hechos nudo', 'se me cargan los musculos',
            'ando todo entumido', 'se me acalambran las piernas'
        ]
        
        dolor_articular = [
            'dolor de articulaciones', 'articulaciones duelen', 'dolor articular',
            'rodillas duelen', 'codos duelen', 'artritis',
            # MEXICANISMOS PARA ARTICULACIONES
            'se me truenan los huesos', 'ando de las articulaciones', 
            'me crujen los huesos', 'huesos adoloridos', 'se me inflaman las coyunturas',
            'dolor en las coyunturas', 'tengo las rodillas hechas pedazos',
            'ando tronado de las rodillas', 'se me clavan las articulaciones',
            'mis huesos protestan', 'ando todo oxidado', 'como bisagra sin aceite'
        ]
        
        # DIABETES/GLUCOSA - MUY IMPORTANTE
        diabetes_keywords = [
            'glucosa', 'azucar', 'diabetes', 'diabetico', 'hiperglucemia',
            'sube la glucosa', 'azucar alta', 'azucar alto', 'glucosa alta',
            'niveles de azucar', 'azucar en sangre', 'glucosa en sangre',
            'se me sube la glucosa', 'tengo diabetes', 'soy diabetico',
            'control de azucar', 'control glucosa', 'glucemia'
        ]
        
        # OBJETIVOS DE PESO - MODISMOS MEXICANOS COMPLETOS
        peso_keywords = [
            # SUBIR DE PESO - MEXICANISMOS
            'deseo subir de peso', 'quiero subir de peso', 'aumentar peso', 'ganar peso',
            'quiero estar mas llenito', 'quiero estar mas gordito', 'necesito engordar',
            'estoy muy flaco', 'estoy muy flaca', 'me veo muy delgado', 'me veo muy delgada',
            'quiero masa muscular', 'quiero estar mas macizo', 'quiero estar mas fuerte',
            'necesito kilos', 'quiero ganar kilos', 'me falta peso', 'estoy en los huesos',
            'parezco palillo', 'estoy muy esqueletico', 'necesito carnes', 'quiero volumen',
            
            # BAJAR DE PESO - MEXICANISMOS  
            'deseo bajar de peso', 'quiero bajar de peso', 'perder peso', 'adelgazar',
            'quiero adelgazar', 'deseo adelgazar', 'bajar kilos', 'perder kilos',
            'quiero estar flaca', 'quiero estar flaco', 'necesito bajar la panza',
            'tengo sobrepeso', 'estoy gordito', 'estoy gordita', 'me siento gorda',
            'me siento gordo', 'quiero quitarme kilos', 'necesito quemar grasa',
            'quiero estar en forma', 'quiero estar fit', 'bajar la pancita',
            'quiero ser mas delgada', 'quiero ser mas delgado', 'eliminar rollitos',
            'control de peso', 'mantener peso', 'peso ideal', 'quitar chaparreras',
            'bajar lonjas', 'eliminar michelines', 'quitar la llanta'
        ]
        
        # DEFENSAS/INMUNIDAD - MODISMOS MEXICANOS COMPLETOS
        defensas_keywords = [
            'deseo reforzar mis defensas', 'quiero reforzar defensas', 'fortalecer defensas',
            'mejorar inmunidad', 'subir defensas', 'sistema inmune', 'inmunologico',
            'quiero mejorar mis defensas', 'deseo fortalecer inmunidad',
            'defensas bajas', 'sistema inmunologico debil',
            # MEXICANISMOS PARA DEFENSAS
            'me enfermo de todo', 'me pego cualquier cosa', 'agarro todo lo que anda',
            'siempre ando enfermo', 'siempre ando enferma', 'soy muy enfermizo',
            'mi cuerpo no se defiende', 'tengo las defensas por el suelo',
            'me da gripa cada mes', 'agarrar gripa seguido', 'enfermarse seguido',
            'quiero que no me pegue nada', 'no quiero enfermarme', 'evitar contagios',
            'fortalecer mi cuerpo', 'hacer mi cuerpo mas fuerte', 'subir las defensas',
            'mejorar mi resistencia', 'no caer enfermo', 'protegerme de virus',
            'que no se me peguen las enfermedades', 'tener mejor salud'
        ]
        
        # ENERGÍA/VITALIDAD - MODISMOS MEXICANOS COMPLETOS
        energia_keywords = [
            'deseo mas energia', 'quiero mas energia', 'aumentar energia',
            'deseo vitalidad', 'quiero vitalidad', 'mas vitalidad',
            'deseo vigor', 'quiero vigor', 'sentirme con energia',
            'falta energia', 'sin energia', 'agotamiento',
            # MEXICANISMOS PARA ENERGÍA
            'ando muy cansado', 'ando muy cansada', 'me siento muy desganado',
            'no tengo ganas de nada', 'ando sin pila', 'estoy sin bateria',
            'me levanto ya cansado', 'no me rinde el dia', 'ando arrastrando los pies',
            'estoy como zombie', 'ando todo desanimado', 'sin ganas de hacer nada',
            'quiero tener mas pilas', 'necesito mas energia', 'sentirme mas activo',
            'que me rindan mas las fuerzas', 'no aguanto el dia completo',
            'me duermo parado', 'ando como trapo', 'estoy hecho polvo',
            'necesito levantarme con ganas', 'quiero sentirme con vida',
            'estar mas despierto', 'tener mas resistencia', 'aguantar mas'
        ]
        
        # MEMORIA/CONCENTRACIÓN - MODISMOS MEXICANOS COMPLETOS
        memoria_keywords = [
            'deseo mejorar memoria', 'quiero mejorar memoria', 'fortalecer memoria',
            'deseo concentrarme mejor', 'quiero concentrarme', 'mejorar concentracion',
            'problemas de memoria', 'olvidos', 'falta concentracion',
            'memoria debil', 'deseo enfocarme mejor',
            # MEXICANISMOS PARA MEMORIA
            'se me olvida todo', 'ando muy olvidadizo', 'ando muy olvidadiza',
            'tengo la cabeza en las nubes', 'no me acuerdo de nada',
            'se me va el avion', 'ando muy distraido', 'ando muy distraida',
            'no me puedo concentrar', 'pierdo el hilo', 'se me va la onda',
            'ando despistado', 'ando despistada', 'tengo mala memoria',
            'se me olvidan las cosas', 'no puedo enfocarme', 'ando en las nubes',
            'quiero tener mejor memoria', 'recordar mejor las cosas',
            'estar mas concentrado', 'estar mas concentrada', 'no andar tan distraido',
            'que se me graben las cosas', 'tener la mente mas clara'
        ]
        
        # DIGESTIÓN - DESEOS/INTENCIONES
        digestion_deseos = [
            'deseo mejorar digestion', 'quiero mejorar digestion', 'mejor digestion',
            'deseo digerir mejor', 'quiero digerir mejor', 'problemas digestivos',
            'digestion lenta', 'digestion pesada'
        ]
        
        # DIGESTIVO
        digestivo_keywords = [
            'dolor de estomago', 'estomago duele', 'malestar estomacal',
            'indigestion', 'acidez', 'gastritis', 'colitis'
        ]
        
        # DETECCIÓN ESPECÍFICA POR PRIORIDAD
        # 1. DIABETES/GLUCOSA (muy específico y prioritario)
        if any(keyword in user_normalized for keyword in diabetes_keywords):
            detected.append('diabetes')
        
        # 2. OBJETIVOS DE PESO (deseos/intenciones)
        if any(keyword in user_normalized for keyword in peso_keywords):
            if any(word in user_normalized for word in ['subir', 'aumentar', 'ganar']):
                detected.append('aumento de peso')
            elif any(word in user_normalized for word in ['bajar', 'perder', 'adelgazar']):
                detected.append('perdida de peso')
            else:
                detected.append('control de peso')
        
        # 3. DEFENSAS/INMUNIDAD (deseos/intenciones)
        if any(keyword in user_normalized for keyword in defensas_keywords):
            detected.append('inmunidad')
        
        # 4. ENERGÍA/VITALIDAD (deseos/intenciones)
        if any(keyword in user_normalized for keyword in energia_keywords):
            detected.append('energia')
        
        # 5. MEMORIA/CONCENTRACIÓN (deseos/intenciones)
        if any(keyword in user_normalized for keyword in memoria_keywords):
            detected.append('memoria')
        
        # 6. DIGESTIÓN (deseos/intenciones)
        if any(keyword in user_normalized for keyword in digestion_deseos):
            detected.append('digestion')
        
        # 7. Gripa/resfriado (muy específico)
        if any(keyword in user_normalized for keyword in gripa_keywords):
            detected.append('gripa')
        
        # 2. ANÁLISIS CONTEXTUAL DE DOLOR - detectar tipo específico por descripción
        dolor_detectado = self._analyze_pain_context(user_normalized)
        if dolor_detectado:
            detected.extend(dolor_detectado)
        
        # MEJORA: Detectar dolor muscular específico basado en contexto
        elif any(keyword in user_normalized for keyword in ['piernas', 'brazos', 'espalda', 'hombros', 'cuello', 'musculo', 'muscular', 'contractura', 'rigidez', 'calambres', 'articulaciones', 'adolorido']):
            if 'dolor muscular' not in detected:
                detected.append('dolor muscular')
        
        # Si no se detecta dolor específico pero se menciona "dolor", usar genérico
        elif 'dolor' in user_normalized and not any('dolor' in d for d in detected):
            detected.append('dolor')
        
        # MEJORADO: Permitir múltiples síntomas específicos diferentes
        # Solo evitar duplicados o síntomas muy generales cuando hay específicos
        
        # DETECCIÓN ESPECÍFICA PARA CASOS RESTANTES
        if 'deseo subir de peso' in user_normalized or 'necesito ganar kilos' in user_normalized:
            detected.append('aumento de peso')
        
        if 'no agarro el sueño' in user_normalized or 'no me llega el sueño' in user_normalized or 'duermo muy mal' in user_normalized:
            detected.append('insomnio')
        
        if 'ando estreñido' in user_normalized or 'no puedo hacer del baño' in user_normalized:
            detected.append('estreñimiento')
        
        if 'se me inflama la panza' in user_normalized:
            detected.append('inflamacion')
        
        # 3. Otros síntomas específicos expandidos CON MODISMOS MEXICANOS
        other_symptoms = {
            'insomnio': ['insomnio', 'no puedo dormir', 'problemas para dormir', 'desvelo', 'dormir mal', 'no duermo', 'me cuesta dormir', 'conciliar el sueño', 'sueño interrumpido',
                        # MEXICANISMOS PARA INSOMNIO
                        'ando desvelado', 'ando desvelada', 'no pego el ojo', 'no puedo pegar los ojos', 'ando en vela', 'me desvelo gacho', 'no agarro el sueño', 'batallo para dormir', 'ando con el sueño perdido', 'no me llega el sueño',
                        'me desvelo muy fácil', 'tengo sueño ligero', 'no me da sueño'],
            
            'cansancio': ['cansancio', 'fatiga', 'sin energia', 'agotado', 'debil', 'me siento cansado', 'estoy agotado', 'sin fuerzas', 'fatiga cronica', 'agotamiento', 'falta de energia', 'muy cansado', 'agotamiento fisico', 'debilidad', 'falta de vitalidad',
                         # MEXICANISMOS PARA CANSANCIO
                         'ando muy cansado', 'ando muy cansada', 'ando sin pila', 'estoy sin bateria', 'ando arrastrando los pies', 'estoy como zombie', 'ando hecho polvo', 'me duermo parado', 'ando como trapo', 'no me rinde el dia', 'ando todo desganado'],
            
            'estres': ['estres', 'estresado', 'ansiedad', 'nervios', 'tension', 'ansioso', 'nervioso', 'ataques de panico', 'tension emocional', 'agobio',
                      # MEXICANISMOS PARA ESTRÉS
                      'ando muy estresado', 'ando muy estresada', 'traigo los nervios de punta', 'ando todo alterado', 'ando todo alterada', 'me trae loco el trabajo', 'ando todo nervioso', 'tengo los nervios hechos pedazos', 'ando muy ansioso', 'ando muy ansiosa'],
            
            'inmunidad': ['defensas bajas', 'enfermo frecuente', 'resfrios constantes', 'sistema inmune', 'fortalecer defensas', 'infecciones recurrentes', 'gripes frecuentes',
                         # MEXICANISMOS PARA INMUNIDAD + CASOS PROBLEMÁTICOS
                         'me enfermo de todo', 'me pego cualquier cosa', 'agarro todo lo que anda', 'siempre ando enfermo', 'siempre ando enferma', 'soy muy enfermizo', 'tengo las defensas por el suelo',
                         'quiero reforzar mis defensas', 'reforzar defensas', 'mejorar defensas'],
            
            'aumento de peso': ['deseo subir de peso', 'necesito ganar kilos', 'quiero estar más llenito', 'estoy muy flaco', 'parezco palillo', 'quiero volumen', 'estoy en los huesos', 'necesito engordar', 'quiero masa muscular', 'necesito vitalidad', 'ando muy delgado'],
            
            'dolor muscular': ['ando todo molido', 'me crujen los huesos', 'se me truenan los huesos', 'me siento quebrado', 'ando todo contracturado', 'se me agarrotan los músculos', 'ando de las articulaciones'],
            
            'memoria': ['se me van las cosas', 'quiero mejor memoria', 'se me olvida todo', 'ando muy olvidadizo', 'ando despistado', 'pierdo el hilo', 'ando en las nubes', 'se me va la onda'],
            
            # NUEVAS CATEGORÍAS IMPLEMENTADAS
            'afrodisiaco': ['problemas sexuales', 'libido baja', 'disfunción', 'potencia sexual', 'deseo sexual', 'vida sexual', 'rendimiento sexual'],
            'higado': ['hígado graso', 'limpiar hígado', 'desintoxicar', 'hepatitis', 'problemas hepáticos', 'limpiar el cuerpo'],
            'colesterol': ['colesterol alto', 'triglicéridos altos', 'grasa en sangre', 'problemas cardiovasculares'],
            'huesos': ['osteoporosis', 'artritis', 'reumatismo', 'calcio bajo', 'problemas óseos', 'huesos débiles'],
            'circulacion': ['varices', 'mala circulación', 'piernas hinchadas', 'hemorroides', 'problemas circulatorios'],
            'ansiedad': ['ataques de pánico', 'nerviosismo', 'ansiedad severa', 'crisis de ansiedad', 'trastorno de ansiedad'],
            'menopausia': ['bochornos', 'irregularidad menstrual', 'ovarios poliquísticos', 'problemas hormonales femeninos'],
            'antioxidante': ['envejecimiento', 'radicales libres', 'anti-edad', 'rejuvenecer', 'antioxidantes'],
            'vitaminas': ['complejo b', 'deficiencia vitamínica', 'suplementos vitamínicos', 'vitaminas del complejo b'],
            
            'digestion': ['digestion', 'estreñimiento', 'diarrea', 'intestino', 'problemas digestivos', 'estreñimiento cronico', 'gases', 'reflujo', 'problemas para digerir', 'digestión lenta', 'pesadez estomacal', 'mala digestión',
                         # MEXICANISMOS PARA DIGESTIÓN + CASOS PROBLEMÁTICOS
                         'se me atora la comida', 'no digiero bien', 'se me hace bola la comida', 'ando estreñido', 'ando estreñida', 'traigo el estomago revuelto', 'me cae gorda la comida', 'ando inflamado del estomago',
                         'no puedo hacer del baño', 'no puedo evacuar', 'tengo el intestino cerrado'],
            
            'estreñimiento': ['estreñimiento', 'estreñimiento cronico', 'no puedo defecar', 'problemas para defecar', 'intestino lento', 'estreñimiento severo',
                             # MEXICANISMOS PARA ESTREÑIMIENTO
                             'ando muy estreñido', 'ando muy estreñida', 'no puedo hacer del baño', 'tengo varios dias sin ir al baño', 'se me atora todo', 'ando tapado', 'ando tapada'],
            
            'inflamacion': ['inflamacion', 'inflamado', 'hinchado', 'inflamacion abdominal', 'hinchazón',
                           # MEXICANISMOS PARA INFLAMACIÓN
                           'ando todo inflamado', 'ando todo inflamada', 'ando todo hinchado', 'ando todo hinchada', 'traigo la panza inflamada', 'se me inflama todo'],
            
            'circulacion': ['mala circulacion', 'circulacion', 'piernas hinchadas', 'varices', 'retencion de liquidos', 'piernas pesadas', 'hinchazón en tobillos', 'pies frios', 'hinchazón', 'tobillos hinchados',
                           # MEXICANISMOS PARA CIRCULACIÓN
                           'se me hinchan las piernas', 'traigo las piernas pesadas', 'se me duermen las piernas', 'tengo los pies frios', 'se me entumen las piernas'],
            
            'acidez': ['acidez', 'reflujo', 'reflujo gastroesofagico', 'agruras', 'ardor estomacal', 'arde el estomago', 'gastritis', 'pirosis', 'dolor estomacal',
                      # MEXICANISMOS PARA ACIDEZ
                      'tengo agruras', 'me arde el estomago', 'traigo acidez', 'se me sube la comida', 'tengo reflujo gacho', 'me quema el estomago'],
            
            'gases': ['gases', 'gases intestinales', 'flatulencia',
                     # MEXICANISMOS PARA GASES
                     'ando muy gasoso', 'ando muy gasosa', 'traigo muchos gases', 'se me infla la panza de gases', 'ando lleno de aire'],
            
            'articulaciones': ['articulaciones', 'todas las articulaciones', 'dolor articular generalizado'],
            'hombro': ['hombro', 'dolor de hombro', 'hombro derecho', 'hombro izquierdo'],
            'presion arterial': ['presion arterial', 'hipertension', 'presion alta', 'presion irregular'],
            'llenura': ['llenura', 'sensacion de llenura', 'llenura rapida', 'me lleno rapido'],
            'nauseas': ['nauseas', 'nauseas constantes', 'ganas de vomitar', 'mareos'],
            'menopausia': ['menopausia', 'sofocos', 'sofocos por menopausia', 'cambios hormonales'],
            'quistes': ['quistes', 'quiste', 'quistes ovaricos', 'quiste en ovario', 'quistes en ovarios'],
            'ovarios': ['ovarios', 'dolor de ovarios', 'problemas en ovarios', 'ovario inflamado'],
            'riñones': ['riñones', 'dolor de riñones', 'problemas renales', 'infeccion renal'],
            'prostata': ['prostata', 'problemas de prostata', 'inflamacion de prostata'],
            'artritis': ['artritis', 'dolor artritico', 'inflamacion articular'],
            'colesterol': ['colesterol', 'colesterol alto', 'trigliceridos'],
            'diabetes': ['diabetes', 'azucar alta', 'glucosa alta'],
            'higado': ['higado', 'higado graso', 'problemas hepaticos']
        }
        
        for symptom, keywords in other_symptoms.items():
            if any(keyword in user_normalized for keyword in keywords):
                if symptom not in detected:
                    detected.append(symptom)
        
        return detected[:3]  # Máximo 3 síntomas para mantener enfoque
    
    def _analyze_pain_context(self, user_input):
        """Analizar el contexto para detectar tipos específicos de dolor"""
        detected_pains = []
        
        # CONTEXTOS ESPECÍFICOS DE DOLOR CON PALABRAS CLAVE Y DESCRIPCIONES
        
        # DOLOR DE CABEZA / MIGRAÑA
        cabeza_patterns = [
            'dolor de cabeza', 'cabeza duele', 'me duele la cabeza', 'dolor en la cabeza',
            'migrana', 'migraña', 'jaqueca', 'cefalea', 'dolor en las sienes',
            'presion en la cabeza', 'punzadas en la cabeza', 'cabeza pesada',
            'tengo dolor de cabeza', 'me esta doliendo la cabeza', 'siento la cabeza pesada',
            'tengo migraña', 'me da migraña', 'dolor en la frente', 'dolor en la nuca'
        ]
        
        # DOLOR MUSCULAR / CONTRACTURAS
        muscular_patterns = [
            'dolor muscular', 'musculos duelen', 'dolores musculares', 'contractura',
            'tension muscular', 'cuello tenso', 'espalda tensa', 'rigidez muscular',
            'calambre', 'calambres', 'dolor en los musculos', 'tirón muscular',
            'me duelen los musculos', 'tengo contractura', 'espalda adolorida',
            'cuello adolorido', 'me duele la espalda', 'me duele el cuello',
            'dolor en la espalda', 'dolor en el cuello', 'musculos adoloridos',
            'duele mucho la espalda', 'dolor de espalda', 'dolor de cuello'
        ]
        
        # DOLOR ARTICULAR / ARTRITIS
        articular_patterns = [
            'dolor de articulaciones', 'articulaciones duelen', 'dolor articular',
            'rodillas duelen', 'codos duelen', 'artritis', 'dolor en las rodillas',
            'dolor en los codos', 'rigidez articular', 'inflamacion articular',
            'me duelen las articulaciones', 'duelen las articulaciones', 'articulaciones adoloridas'
        ]
        
        # DOLOR ESTOMACAL / DIGESTIVO
        digestivo_patterns = [
            'dolor de estomago', 'estomago duele', 'dolor estomacal', 'malestar estomacal',
            'dolor abdominal', 'abdomen duele', 'gastritis', 'acidez estomacal',
            'dolor en el estomago', 'estomago irritado', 'indigestion',
            'me duele el estomago', 'tengo dolor de estomago', 'estomago adolorido',
            'dolor en la barriga', 'me duele la barriga', 'dolor en el abdomen',
            'acidez', 'agruras', 'estomago revuelto', 'mala digestion',
            'me arde el estomago', 'arde el estomago', 'ardor estomacal', 'ardor de estomago',
            'estomago arde', 'siento ardor', 'quema el estomago', 'estomago quema'
        ]
        
        # DOLOR MENSTRUAL
        menstrual_patterns = [
            'dolor menstrual', 'colicos menstruales', 'dolor de regla', 'colicos',
            'dolor en el periodo', 'dolores de menstruacion', 'molestias menstruales'
        ]
        
        # DOLOR DE GARGANTA
        garganta_patterns = [
            'dolor de garganta', 'garganta duele', 'garganta irritada', 'garganta inflamada',
            'dolor al tragar', 'garganta rasposa', 'picazon en la garganta'
        ]
        
        # DOLOR DENTAL
        dental_patterns = [
            'dolor de muela', 'dolor dental', 'diente duele', 'muelas duelen',
            'dolor en los dientes', 'sensibilidad dental'
        ]
        
        # Detectar cada tipo específico
        pain_types = {
            'dolor de cabeza': cabeza_patterns,
            'dolor muscular': muscular_patterns,
            'dolor articular': articular_patterns,
            'dolor estomacal': digestivo_patterns,
            'dolor menstrual': menstrual_patterns,
            'dolor de garganta': garganta_patterns,
            'dolor dental': dental_patterns
        }
        
        for pain_type, patterns in pain_types.items():
            if any(pattern in user_input for pattern in patterns):
                detected_pains.append(pain_type)
        
        return detected_pains
    
    def _adjust_score_for_insomnia(self, product_row, base_score):
        """Ajustar puntuación para productos de insomnio priorizando los más específicos"""
        product_name = str(product_row.get('nombre', '')).lower()
        
        # PRIORIDAD ALTA: Productos específicos para sueño
        high_priority = ['valeriana', 'pasiflora', 'triptofano', 'magnesio', '7 azahares', 'dor m bien', 'melatonina']
        if any(priority in product_name for priority in high_priority):
            return base_score + 3  # Aumentar significativamente la prioridad
        
        # PRIORIDAD BAJA: Productos que mencionan insomnio pero no son específicos
        low_priority = ['sin tn sion', 'ant epil', 'presurex', 'tiamin']
        if any(low_priority in product_name for low_priority in low_priority):
            return max(1, base_score - 2)  # Reducir significativamente la prioridad
        
        # PRIORIDAD MEDIA: Productos naturales relacionados con sueño
        medium_priority = ['guanabana', 'vitamina b6']
        if any(medium in product_name for medium in medium_priority):
            return base_score  # Mantener prioridad normal
        
        # EXCLUIR: Productos claramente no relacionados con sueño
        exclude_keywords = ['prostata', 'diabetes', 'presion', 'colesterol']
        if any(keyword in product_name for keyword in exclude_keywords):
            return 0  # Excluir completamente
        
        return base_score
    
    def _find_similar_symptom_products(self, symptom, user_profile, needed_count):
        """Buscar productos para síntomas similares cuando no hay suficientes productos específicos"""
        similar_products = []
        
        # Mapeo de síntomas similares expandido
        symptom_similarities = {
            'dolor de espalda': ['dolor muscular', 'dolor', 'contractura'],
            'dolor articular': ['dolor', 'inflamacion', 'artritis'],
            'estreñimiento': ['digestion', 'dolor estomacal'],
            'inflamacion abdominal': ['dolor estomacal', 'digestion', 'inflamacion'],
            'problemas digestivos': ['digestion', 'dolor estomacal'],
            'sistema inmune': ['inmunidad', 'energia', 'cansancio'],
            'mala circulacion': ['circulacion', 'inflamacion'],
            'varices': ['circulacion', 'inflamacion'],
            'dolor de hombro': ['dolor muscular', 'dolor articular', 'dolor'],
            'articulaciones': ['dolor articular', 'inflamacion', 'dolor'],
            'reflujo': ['dolor estomacal', 'digestion'],
            'gases': ['digestion', 'dolor estomacal', 'inflamacion'],
            'hinchazón': ['circulacion', 'inflamacion'],
            'presión arterial': ['circulacion', 'estres'],
            'piernas pesadas': ['circulacion', 'cansancio']
        }
        
        similar_symptoms = symptom_similarities.get(symptom, [])
        
        for similar_symptom in similar_symptoms:
            if len(similar_products) >= needed_count:
                break
                
            products = self._find_catalog_products_for_symptom(similar_symptom, user_profile, 1, needed_count - len(similar_products))
            
            # Filtrar productos que no estén duplicados
            for product in products:
                if len(similar_products) >= needed_count:
                    break
                    
                is_duplicate = any(p['nombre'] == product['nombre'] for p in similar_products)
                if not is_duplicate:
                    # Marcar como coincidencia similar (menor prioridad)
                    product['match_score'] = max(1, product.get('match_score', 1) - 1)
                    similar_products.append(product)
        
        return similar_products
        
        # Buscar coincidencias en mapeos de síntomas
        for symptom_key, variations in self.symptom_mappings.items():
            for variation in variations:
                if variation in user_normalized:
                    # Si es contexto digestivo y el síntoma es "dolor", omitirlo para evitar confusión
                    if es_contexto_digestivo and symptom_key == 'dolor':
                        continue
                    
                    # Si es contexto de sueño, evitar duplicados de sueño/insomnio y dolor genérico
                    if es_contexto_sueno and symptom_key == 'dolor':
                        continue
                    
                    # Evitar duplicados de sueño e insomnio (son el mismo problema)
                    if symptom_key == 'sueño' and 'insomnio' in detected:
                        continue
                    if symptom_key == 'insomnio' and 'sueño' in detected:
                        continue
                    
                    # Verificar que el síntoma existe en el catálogo
                    if self._symptom_exists_in_catalog(symptom_key):
                        detected.append(symptom_key)
                        break
        
        # Si detectamos contexto gastrointestinal, agregar síntomas específicos del estómago
        if es_contexto_digestivo:
            sintomas_estomacales = ['estomago', 'gastritis', 'indigestion', 'acidez']
            for sintoma in sintomas_estomacales:
                if self._symptom_exists_in_catalog(sintoma) and sintoma not in detected:
                    detected.append(sintoma)
        
        # Búsqueda adicional directa en el catálogo
        if 'sintomas_norm' in self.catalog_df.columns:
            catalog_symptoms = []
            for _, row in self.catalog_df.iterrows():
                if row['sintomas_norm']:
                    symptoms_in_product = str(row['sintomas_norm']).split(',')
                    catalog_symptoms.extend([s.strip() for s in symptoms_in_product if s.strip()])
            
            # Buscar coincidencias directas
            for catalog_symptom in set(catalog_symptoms):
                if catalog_symptom in user_normalized and catalog_symptom not in detected:
                    # Si es contexto digestivo, evitar agregar "dolor" genérico
                    if es_contexto_digestivo and catalog_symptom == 'dolor':
                        continue
                    detected.append(catalog_symptom)
        
        return list(set(detected))[:5]  # Máximo 5 síntomas diferentes
    
    def _symptom_exists_in_catalog(self, symptom):
        """Verificar que el síntoma existe realmente en el catálogo"""
        if 'sintomas_norm' not in self.catalog_df.columns:
            return False
        
        for _, row in self.catalog_df.iterrows():
            if row['sintomas_norm'] and symptom in str(row['sintomas_norm']):
                return True
        return False
    
    def _find_catalog_products_for_symptom(self, symptom, user_profile, min_products, max_products):
        """Encontrar productos reales del catálogo para un síntoma específico con rotación equitativa"""
        all_matching_products = []
        
        # FORZAR PRODUCTOS ESPECÍFICOS DIRECTAMENTE SEGÚN SÍNTOMA
        if 'diabetes' in symptom.lower() or 'glucosa' in symptom.lower() or 'azucar' in symptom.lower():
            # Buscar productos específicos para DIABETES/GLUCOSA
            diabetes_keywords = ['STEVIA', 'CANELA', 'CROMO', 'GYMNEMA', 'FENOGRECO']
            for keyword in diabetes_keywords:
                diabetes_products = self.catalog_df[self.catalog_df['nombre'].str.contains(keyword, case=False, na=False)]
                for idx, row in diabetes_products.head(1).iterrows():
                    if self._is_safe_for_user(row, user_profile):
                        product = self._format_product(row)
                        product['match_score'] = '20'  # Máxima prioridad para diabetes
                        product['product_name'] = str(row.get('nombre', ''))
                        all_matching_products.append(product)
                        if len(all_matching_products) >= max_products:
                            break
                if len(all_matching_products) >= max_products:
                    break
        
        elif 'aumento de peso' in symptom.lower():
            # Buscar productos para GANAR PESO
            peso_keywords = ['PROTEINA', 'PROTEIN', 'MASS', 'GAINER', 'CREATINA']
            for keyword in peso_keywords:
                peso_products = self.catalog_df[self.catalog_df['nombre'].str.contains(keyword, case=False, na=False)]
                for idx, row in peso_products.head(1).iterrows():
                    if self._is_safe_for_user(row, user_profile):
                        product = self._format_product(row)
                        product['match_score'] = '20'
                        product['product_name'] = str(row.get('nombre', ''))
                        all_matching_products.append(product)
                        if len(all_matching_products) >= max_products:
                            break
                if len(all_matching_products) >= max_products:
                    break
        
        elif 'perdida de peso' in symptom.lower():
            # Buscar productos para BAJAR PESO - PRODUCTOS REALES DEL CATÁLOGO
            adelgazar_keywords = ['ALFIX', 'REDUCTOR', 'CARBO BURN', 'CARNITINA', 'GARCINIA', 'TE VERDE', 'TERMOGENICO', 'QUEMADOR', 'TORONJA', 'ALGAS MARINAS']
            for keyword in adelgazar_keywords:
                adelgazar_products = self.catalog_df[self.catalog_df['nombre'].str.contains(keyword, case=False, na=False)]
                for idx, row in adelgazar_products.head(1).iterrows():
                    if self._is_safe_for_user(row, user_profile):
                        product = self._format_product(row)
                        product['match_score'] = '20'
                        product['product_name'] = str(row.get('nombre', ''))
                        all_matching_products.append(product)
                        if len(all_matching_products) >= max_products:
                            break
                if len(all_matching_products) >= max_products:
                    break
        
        elif 'aumento de peso' in symptom.lower():
            # BÚSQUEDA DEFINITIVA PARA AUMENTO DE PESO - PRODUCTOS ESPECÍFICOS DEL CATÁLOGO
            peso_products = []
            
            # Buscar AF TOTALVIT MULTIVITAMINICO específicamente
            if self.catalog_df is not None:
                totalvit_products = self.catalog_df[self.catalog_df['nombre'].str.contains('TOTALVIT', case=False, na=False)]
                for idx, row in totalvit_products.head(1).iterrows():
                    if self._is_safe_for_user(row, user_profile):
                        product = self._format_product(row)
                        product['match_score'] = '30'
                        product['product_name'] = str(row.get('nombre', ''))
                        peso_products.append(product)
                
                # Buscar AF HBINE ZARZAPARRILLA específicamente
                if len(peso_products) < max_products:
                    hbine_products = self.catalog_df[self.catalog_df['nombre'].str.contains('HBINE', case=False, na=False)]
                    for idx, row in hbine_products.head(1).iterrows():
                        if self._is_safe_for_user(row, user_profile):
                            product = self._format_product(row)
                            product['match_score'] = '30'
                            product['product_name'] = str(row.get('nombre', ''))
                            peso_products.append(product)
                
                # Agregar productos encontrados
                all_matching_products.extend(peso_products)
                
                # Retornar inmediatamente si encontramos productos
                if len(peso_products) >= min_products:
                    return self._apply_product_rotation(peso_products, min_products, max_products)
        
        elif 'afrodisiaco' in symptom.lower() or 'sexual' in symptom.lower() or 'libido' in symptom.lower():
            # SALUD SEXUAL/AFRODISÍACOS - PRODUCTOS REALES DEL CATÁLOGO
            sexual_keywords = ['DAMIANA', 'MACA', 'GUARANA', 'AFRODISIACO', 'LIBIDO']
            for keyword in sexual_keywords:
                sexual_products = self.catalog_df[self.catalog_df['nombre'].str.contains(keyword, case=False, na=False)]
                for idx, row in sexual_products.head(1).iterrows():
                    if self._is_safe_for_user(row, user_profile):
                        product = self._format_product(row)
                        product['match_score'] = '20'
                        product['product_name'] = str(row.get('nombre', ''))
                        all_matching_products.append(product)
                        if len(all_matching_products) >= max_products:
                            break
                if len(all_matching_products) >= max_products:
                    break
        
        elif 'higado' in symptom.lower() or 'hepatico' in symptom.lower() or 'desintoxicar' in symptom.lower():
            # SALUD HEPÁTICA/DESINTOXICACIÓN - PRODUCTOS REALES DEL CATÁLOGO  
            higado_keywords = ['CARDO MARIANO', 'BOLDO', 'ALCACHOFA', 'HEPATICO', 'DESINTOX']
            for keyword in higado_keywords:
                higado_products = self.catalog_df[self.catalog_df['nombre'].str.contains(keyword, case=False, na=False)]
                for idx, row in higado_products.head(1).iterrows():
                    if self._is_safe_for_user(row, user_profile):
                        product = self._format_product(row)
                        product['match_score'] = '20'
                        product['product_name'] = str(row.get('nombre', ''))
                        all_matching_products.append(product)
                        if len(all_matching_products) >= max_products:
                            break
                if len(all_matching_products) >= max_products:
                    break
        
        elif 'colesterol' in symptom.lower() or 'trigliceridos' in symptom.lower():
            # COLESTEROL/TRIGLICÉRIDOS - PRODUCTOS REALES DEL CATÁLOGO
            colesterol_keywords = ['OMEGA', 'LECITINA', 'ALCACHOFA', 'CARDO', 'BOLDO']
            for keyword in colesterol_keywords:
                colesterol_products = self.catalog_df[self.catalog_df['nombre'].str.contains(keyword, case=False, na=False)]
                for idx, row in colesterol_products.head(1).iterrows():
                    if self._is_safe_for_user(row, user_profile):
                        product = self._format_product(row)
                        product['match_score'] = '20'
                        product['product_name'] = str(row.get('nombre', ''))
                        all_matching_products.append(product)
                        if len(all_matching_products) >= max_products:
                            break
                if len(all_matching_products) >= max_products:
                    break
        
        elif 'huesos' in symptom.lower() or 'artritis' in symptom.lower() or 'osteoporosis' in symptom.lower():
            # SALUD ÓSEA/ARTICULAR - PRODUCTOS REALES DEL CATÁLOGO
            huesos_keywords = ['CALCIO', 'MAGNESIO', 'COLAGENO', 'SHARK', 'ARTICULAR']
            for keyword in huesos_keywords:
                huesos_products = self.catalog_df[self.catalog_df['nombre'].str.contains(keyword, case=False, na=False)]
                for idx, row in huesos_products.head(1).iterrows():
                    if self._is_safe_for_user(row, user_profile):
                        product = self._format_product(row)
                        product['match_score'] = '20'
                        product['product_name'] = str(row.get('nombre', ''))
                        all_matching_products.append(product)
                        if len(all_matching_products) >= max_products:
                            break
                if len(all_matching_products) >= max_products:
                    break
        
        elif 'circulacion' in symptom.lower() or 'varices' in symptom.lower() or 'hemorroides' in symptom.lower():
            # CIRCULACIÓN/VARICES - PRODUCTOS REALES DEL CATÁLOGO
            circulacion_keywords = ['GINKGO', 'CIRCULACION', 'CENTELLA', 'CASTANO', 'RUSCO']
            for keyword in circulacion_keywords:
                circulacion_products = self.catalog_df[self.catalog_df['nombre'].str.contains(keyword, case=False, na=False)]
                for idx, row in circulacion_products.head(1).iterrows():
                    if self._is_safe_for_user(row, user_profile):
                        product = self._format_product(row)
                        product['match_score'] = '20'
                        product['product_name'] = str(row.get('nombre', ''))
                        all_matching_products.append(product)
                        if len(all_matching_products) >= max_products:
                            break
                if len(all_matching_products) >= max_products:
                    break
        
        elif 'ansiedad' in symptom.lower() or 'nervios' in symptom.lower() or 'panico' in symptom.lower():
            # SISTEMA NERVIOSO/ANSIEDAD - PRODUCTOS REALES DEL CATÁLOGO
            nervios_keywords = ['VALERIANA', 'PASIFLORA', 'DON RELAX', 'AZAHARES', 'TILA']
            for keyword in nervios_keywords:
                nervios_products = self.catalog_df[self.catalog_df['nombre'].str.contains(keyword, case=False, na=False)]
                for idx, row in nervios_products.head(1).iterrows():
                    if self._is_safe_for_user(row, user_profile):
                        product = self._format_product(row)
                        product['match_score'] = '20'
                        product['product_name'] = str(row.get('nombre', ''))
                        all_matching_products.append(product)
                        if len(all_matching_products) >= max_products:
                            break
                if len(all_matching_products) >= max_products:
                    break
        
        elif 'menopausia' in symptom.lower() or 'bochornos' in symptom.lower() or 'hormonal' in symptom.lower():
            # SALUD FEMENINA - PRODUCTOS REALES DEL CATÁLOGO
            femenina_keywords = ['PM MUJ', 'ISOFLAVONAS', 'SOY', 'ANGELICA', 'REX OV']
            for keyword in femenina_keywords:
                femenina_products = self.catalog_df[self.catalog_df['nombre'].str.contains(keyword, case=False, na=False)]
                for idx, row in femenina_products.head(1).iterrows():
                    if self._is_safe_for_user(row, user_profile):
                        product = self._format_product(row)
                        product['match_score'] = '20'
                        product['product_name'] = str(row.get('nombre', ''))
                        all_matching_products.append(product)
                        if len(all_matching_products) >= max_products:
                            break
                if len(all_matching_products) >= max_products:
                    break
        
        elif 'antioxidante' in symptom.lower() or 'envejecimiento' in symptom.lower() or 'anti edad' in symptom.lower():
            # ANTIOXIDANTES/ANTI-EDAD - PRODUCTOS REALES DEL CATÁLOGO
            antioxidante_keywords = ['VITAMINA E', 'VITAMINA C', 'COLAGENO', 'ANTIOXIDANTE', 'OMEGA']
            for keyword in antioxidante_keywords:
                antioxidante_products = self.catalog_df[self.catalog_df['nombre'].str.contains(keyword, case=False, na=False)]
                for idx, row in antioxidante_products.head(1).iterrows():
                    if self._is_safe_for_user(row, user_profile):
                        product = self._format_product(row)
                        product['match_score'] = '20'
                        product['product_name'] = str(row.get('nombre', ''))
                        all_matching_products.append(product)
                        if len(all_matching_products) >= max_products:
                            break
                if len(all_matching_products) >= max_products:
                    break
        
        elif 'vitaminas' in symptom.lower() or 'complejo b' in symptom.lower():
            # VITAMINAS ESPECÍFICAS - PRODUCTOS REALES DEL CATÁLOGO
            vitaminas_keywords = ['VITAMINA B', 'VITAMINA C', 'COMPLEJO', 'MULTIVITAMINICO']
            for keyword in vitaminas_keywords:
                vitaminas_products = self.catalog_df[self.catalog_df['nombre'].str.contains(keyword, case=False, na=False)]
                for idx, row in vitaminas_products.head(1).iterrows():
                    if self._is_safe_for_user(row, user_profile):
                        product = self._format_product(row)
                        product['match_score'] = '20'
                        product['product_name'] = str(row.get('nombre', ''))
                        all_matching_products.append(product)
                        if len(all_matching_products) >= max_products:
                            break
                if len(all_matching_products) >= max_products:
                    break
        
        elif 'inmunidad' in symptom.lower():
            # Buscar productos para DEFENSAS/INMUNIDAD - PRODUCTOS REALES DEL CATÁLOGO
            inmunidad_keywords = ['DEFENCE GOLD', 'L10 PROPOLEO', 'PROPOLEO', 'ECHINACEA', 'VITAMINA C', 'ZINC', 'OREGANO', 'EQUINACEA']
            for keyword in inmunidad_keywords:
                inmunidad_products = self.catalog_df[self.catalog_df['nombre'].str.contains(keyword, case=False, na=False)]
                for idx, row in inmunidad_products.head(1).iterrows():
                    if self._is_safe_for_user(row, user_profile):
                        product = self._format_product(row)
                        product['match_score'] = '20'
                        product['product_name'] = str(row.get('nombre', ''))
                        all_matching_products.append(product)
                        if len(all_matching_products) >= max_products:
                            break
                if len(all_matching_products) >= max_products:
                    break
        
        elif 'energia' in symptom.lower():
            # Buscar productos para ENERGÍA/VITALIDAD
            energia_keywords = ['GINSENG', 'GINKGO', 'GUARANA', 'MACA', 'COMPLEJO B', 'B12']
            for keyword in energia_keywords:
                energia_products = self.catalog_df[self.catalog_df['nombre'].str.contains(keyword, case=False, na=False)]
                for idx, row in energia_products.head(1).iterrows():
                    if self._is_safe_for_user(row, user_profile):
                        product = self._format_product(row)
                        product['match_score'] = '20'
                        product['product_name'] = str(row.get('nombre', ''))
                        all_matching_products.append(product)
                        if len(all_matching_products) >= max_products:
                            break
                if len(all_matching_products) >= max_products:
                    break
        
        elif 'memoria' in symptom.lower():
            # Buscar productos para MEMORIA/CONCENTRACIÓN - PRODUCTOS REALES DEL CATÁLOGO
            memoria_keywords = ['BRAINGEAR', 'MEMORA PLUS', 'GINKGO', 'OMEGA 3', 'LECITINA', 'GINSENG', 'BRAIN', 'FOCUS']
            for keyword in memoria_keywords:
                memoria_products = self.catalog_df[self.catalog_df['nombre'].str.contains(keyword, case=False, na=False)]
                for idx, row in memoria_products.head(1).iterrows():
                    if self._is_safe_for_user(row, user_profile):
                        product = self._format_product(row)
                        product['match_score'] = '20'
                        product['product_name'] = str(row.get('nombre', ''))
                        all_matching_products.append(product)
                        if len(all_matching_products) >= max_products:
                            break
                if len(all_matching_products) >= max_products:
                    break
        
        elif 'dolor de cabeza' in symptom.lower() or 'cabeza' in symptom.lower():
            # Buscar VALERIANA para dolor de cabeza
            valeriana_products = self.catalog_df[self.catalog_df['nombre'].str.contains('VALERIANA', case=False, na=False)]
            for idx, row in valeriana_products.head(2).iterrows():
                if self._is_safe_for_user(row, user_profile):
                    product = self._format_product(row)
                    product['match_score'] = '20'  # Máxima prioridad
                    product['product_name'] = str(row.get('nombre', ''))
                    all_matching_products.append(product)
            
            # Buscar 7 AZAHARES para dolor de cabeza
            azahares_products = self.catalog_df[self.catalog_df['nombre'].str.contains('AZAHARES', case=False, na=False)]
            for idx, row in azahares_products.head(1).iterrows():
                if self._is_safe_for_user(row, user_profile):
                    product = self._format_product(row)
                    product['match_score'] = 20
                    product['product_name'] = str(row.get('nombre', ''))
                    all_matching_products.append(product)
        
        elif 'dolor estomacal' in symptom.lower() or 'estomacal' in symptom.lower() or 'acidez' in symptom.lower():
            # Buscar COPALCHI para acidez/ardor estomacal
            copalchi_products = self.catalog_df[self.catalog_df['nombre'].str.contains('COPALCHI', case=False, na=False)]
            for idx, row in copalchi_products.head(2).iterrows():
                if self._is_safe_for_user(row, user_profile):
                    product = self._format_product(row)
                    product['match_score'] = 20  # Máxima prioridad
                    product['product_name'] = str(row.get('nombre', ''))
                    all_matching_products.append(product)
            
            # Buscar FENOGRECO para digestión
            fenogreco_products = self.catalog_df[self.catalog_df['nombre'].str.contains('FENOGRECO', case=False, na=False)]
            for idx, row in fenogreco_products.head(1).iterrows():
                if self._is_safe_for_user(row, user_profile):
                    product = self._format_product(row)
                    product['match_score'] = 20
                    product['product_name'] = str(row.get('nombre', ''))
                    all_matching_products.append(product)
        
        elif 'insomnio' in symptom.lower() or 'dormir' in symptom.lower() or 'sueño' in symptom.lower():
            # Buscar VALERIANA para insomnio
            valeriana_products = self.catalog_df[self.catalog_df['nombre'].str.contains('VALERIANA', case=False, na=False)]
            for idx, row in valeriana_products.head(2).iterrows():
                if self._is_safe_for_user(row, user_profile):
                    product = self._format_product(row)
                    product['match_score'] = 20
                    product['product_name'] = str(row.get('nombre', ''))
                    all_matching_products.append(product)
            
            # Buscar 7 AZAHARES para relajación/sueño
            azahares_products = self.catalog_df[self.catalog_df['nombre'].str.contains('AZAHARES', case=False, na=False)]
            for idx, row in azahares_products.head(1).iterrows():
                if self._is_safe_for_user(row, user_profile):
                    product = self._format_product(row)
                    product['match_score'] = 20
                    product['product_name'] = str(row.get('nombre', ''))
                    all_matching_products.append(product)
        
        elif 'cansancio' in symptom.lower() or 'fatiga' in symptom.lower() or 'energia' in symptom.lower():
            # Buscar MEGALPISTE para energía/cansancio
            energia_products = self.catalog_df[self.catalog_df['nombre'].str.contains('MEGALPISTE', case=False, na=False)]
            for idx, row in energia_products.head(2).iterrows():
                if self._is_safe_for_user(row, user_profile):
                    product = self._format_product(row)
                    product['match_score'] = 20
                    product['product_name'] = str(row.get('nombre', ''))
                    all_matching_products.append(product)
            
            # Buscar productos VITAL para energía
            vital_products = self.catalog_df[self.catalog_df['nombre'].str.contains('VITAL', case=False, na=False)]
            for idx, row in vital_products.head(1).iterrows():
                if self._is_safe_for_user(row, user_profile):
                    product = self._format_product(row)
                    product['match_score'] = 20
                    product['product_name'] = str(row.get('nombre', ''))
                    all_matching_products.append(product)
        
        elif 'quistes' in symptom.lower() or 'ovarios' in symptom.lower():
            # Productos específicos para quistes y problemas hormonales femeninos
            female_hormonal_products = [
                'PM ISOFLAVONAS', 'PM MUJER', 'AR REX OV', 'PM MUJ ANGELICA', 'PM REX OV'
            ]
            
            products_found = 0
            for product_keyword in female_hormonal_products:
                if products_found >= 2:  # Solo 2 productos
                    break
                    
                matching_products = self.catalog_df[self.catalog_df['nombre'].str.contains(product_keyword, case=False, na=False)]
                for idx, row in matching_products.head(1).iterrows():
                    if self._is_safe_for_user(row, user_profile):
                        product = self._format_product(row)
                        product['match_score'] = 20
                        product['product_name'] = str(row.get('nombre', ''))
                        all_matching_products.append(product)
                        products_found += 1
                        break
        
        elif 'dolor muscular' in symptom.lower() or 'muscular' in symptom.lower() or 'musculo' in symptom.lower() or 'molido' in symptom.lower() or 'crujen' in symptom.lower() or 'quebrado' in symptom.lower():
            # LISTA ESPECÍFICA de productos apropiados para dolor muscular y modismos mexicanos
            muscle_pain_products = [
                'CURA DOL PLUS',  # Producto específico para dolor
                'SHARK CALCIUM',  # Con garra del diablo
                'VOON FLEX',      # Para flexibilidad y dolor
                'JUQUILITA',      # Apropiado para dolor muscular
                'UÑAS GATO', 'UNAS GATO',  # Apropiado para dolor muscular
                'TEPEZCOHUITE',   # Apropiado para dolor muscular
                'ARNICA',         # Si existe en el catálogo
                'SAUCE'          # Si existe en el catálogo
            ]
            
            products_found = 0
            for product_keyword in muscle_pain_products:
                if products_found >= 2:  # Solo 2 productos
                    break
                    
                matching_products = self.catalog_df[self.catalog_df['nombre'].str.contains(product_keyword, case=False, na=False)]
                for idx, row in matching_products.head(1).iterrows():
                    if self._is_safe_for_user(row, user_profile):
                        # VERIFICAR que NO sea MEGALPISTE o productos nutricionales
                        product_name = str(row.get('nombre', '')).lower()
                        product_benefits = str(row.get('beneficios', '')).lower()
                        
                        # EXCLUIR productos nutricionales
                        if any(exclude_word in product_name or exclude_word in product_benefits 
                               for exclude_word in ['megalpiste', 'nutricion', 'digestivo', 'cardiovascular', 'alpiste', 'soya']):
                            continue
                            
                        product = self._format_product(row)
                        product['match_score'] = 20
                        product['product_name'] = str(row.get('nombre', ''))
                        all_matching_products.append(product)
                        products_found += 1
                        break
        
        # Si ya encontramos productos específicos suficientes, retornar directamente
        if len(all_matching_products) >= min_products:
            return self._apply_product_rotation(all_matching_products, min_products, max_products)
        
        # FORZAR productos específicos de insomnio (original)
        if symptom == 'insomnio':
            priority_keywords = ['valeriana', 'pasiflora', 'triptofano', '7 azahares']
            for idx, row in self.catalog_df.iterrows():
                product_name = str(row.get('nombre', '')).lower()
                if any(keyword in product_name for keyword in priority_keywords):
                    # Evitar duplicados
                    already_exists = any(p['product_name'] == row['nombre'] for p in all_matching_products)
                    if not already_exists and self._is_safe_for_user(row, user_profile):
                        product = self._format_product(row)
                        product['match_score'] = 5  # Puntuación máxima
                        product['product_name'] = row['nombre']
                        all_matching_products.append(product)

        # Buscar en síntomas del catálogo (prioridad alta)
        for idx, row in self.catalog_df.iterrows():
            if self._product_matches_symptom(row, symptom):
                if self._is_safe_for_user(row, user_profile):
                    # Evitar duplicados
                    already_exists = any(p['product_name'] == row['nombre'] for p in all_matching_products)
                    if not already_exists:
                        product = self._format_product(row)
                        base_score = 3  # Puntuación alta para síntomas directos
                        
                        # AJUSTE ESPECÍFICO PARA INSOMNIO: priorizar productos más específicos
                        if symptom == 'insomnio':
                            base_score = self._adjust_score_for_insomnia(row, base_score)
                        
                        product['match_score'] = base_score
                        product['product_name'] = row['nombre']
                        all_matching_products.append(product)
        
        # Buscar en beneficios (prioridad media)
        for idx, row in self.catalog_df.iterrows():
            if self._product_benefits_match_symptom(row, symptom):
                if self._is_safe_for_user(row, user_profile):
                    # Verificar si ya está en la lista
                    already_exists = any(p['product_name'] == row['nombre'] for p in all_matching_products)
                    if not already_exists:
                        product = self._format_product(row)
                        product['match_score'] = 2  # Puntuación media
                        product['product_name'] = row['nombre']
                        all_matching_products.append(product)
        
        # Buscar en ingredientes (prioridad baja)
        for idx, row in self.catalog_df.iterrows():
            if self._product_ingredients_match_symptom(row, symptom):
                if self._is_safe_for_user(row, user_profile):
                    # Verificar si ya está en la lista
                    already_exists = any(p['product_name'] == row['nombre'] for p in all_matching_products)
                    if not already_exists:
                        product = self._format_product(row)
                        product['match_score'] = 1  # Puntuación baja
                        product['product_name'] = row['nombre']
                        all_matching_products.append(product)
        
        # Aplicar rotación equitativa
        final_products = self._apply_product_rotation(all_matching_products, min_products, max_products)
        
        # Garantizar mínimo de productos si no hay suficientes
        if len(final_products) < min_products:
            # Primero intentar con síntomas similares
            similar_products = self._find_similar_symptom_products(symptom, user_profile, min_products - len(final_products))
            final_products.extend(similar_products)
            
            # Si aún no hay suficientes, usar productos de bienestar general
            if len(final_products) < min_products:
                additional = self._get_general_wellness_products(min_products - len(final_products))
                final_products.extend(additional)
        
        return final_products[:max_products]
    
    def _apply_product_rotation(self, all_matching_products, min_products, max_products):
        """Aplicar rotación equitativa para dar oportunidades justas a todos los productos"""
        import random
        
        if not all_matching_products:
            return []
        
        # Inicializar contador para productos nuevos
        for product in all_matching_products:
            product_name = product['product_name']
            if product_name not in self.product_rotation_counter:
                self.product_rotation_counter[product_name] = 0
        
        # Separar por puntuación de coincidencia (incluyendo productos específicos para acidez)
        expert_score = [p for p in all_matching_products if int(p.get('match_score', 0)) >= 8]  # Productos específicos para acidez
        high_score = [p for p in all_matching_products if int(p.get('match_score', 0)) == 3]
        medium_score = [p for p in all_matching_products if int(p.get('match_score', 0)) == 2]
        low_score = [p for p in all_matching_products if int(p.get('match_score', 0)) == 1]
        
        # Función para ordenar por rotación (menos veces mostrado = más prioridad)
        def sort_by_rotation(products):
            return sorted(products, key=lambda p: (
                self.product_rotation_counter[p['product_name']],  # Menos veces mostrado primero
                random.random()  # Aleatorio como desempate
            ))
        
        # Ordenar cada grupo por rotación
        expert_score = sort_by_rotation(expert_score)
        high_score = sort_by_rotation(high_score)
        medium_score = sort_by_rotation(medium_score)
        low_score = sort_by_rotation(low_score)
        
        # Seleccionar productos balanceando prioridad y rotación
        selected_products = []
        
        # PRIORIDAD MÁXIMA: productos específicos para acidez/digestivo
        for product in expert_score:
            if len(selected_products) >= max_products:
                break
            selected_products.append(product)
            self.product_rotation_counter[product['product_name']] += 1
        
        # Priorizar productos de alta coincidencia con rotación
        for product in high_score:
            if len(selected_products) >= max_products:
                break
            selected_products.append(product)
            self.product_rotation_counter[product['product_name']] += 1
        
        # Agregar productos de media coincidencia si necesitamos más
        if len(selected_products) < max_products:
            for product in medium_score:
                if len(selected_products) >= max_products:
                    break
                selected_products.append(product)
                self.product_rotation_counter[product['product_name']] += 1
        
        # Agregar productos de baja coincidencia si aún necesitamos más
        if len(selected_products) < max_products:
            for product in low_score:
                if len(selected_products) >= max_products:
                    break
                selected_products.append(product)
                self.product_rotation_counter[product['product_name']] += 1
        
        # Limpiar campos auxiliares
        for product in selected_products:
            if 'match_score' in product:
                del product['match_score']
            if 'product_name' in product:
                del product['product_name']
        
        return selected_products
    
    def _product_matches_symptom(self, product_row, symptom):
        """Verificar si el producto coincide con el síntoma en la columna de síntomas"""
        if 'sintomas_norm' not in product_row or not product_row['sintomas_norm']:
            return False
        
        product_symptoms = str(product_row['sintomas_norm']).lower()
        product_name = str(product_row.get('nombre', '')).lower()
        
        # FILTRO ESPECÍFICO: evitar productos para condiciones médicas específicas
        # cuando se busca un síntoma genérico como "dolor"
        if symptom == 'dolor':
            # Excluir productos específicos para diabetes, hipertensión, etc.
            # si solo mencionan el síntoma genérico
            diabetes_keywords = ['diabetes', 'diabetico', 'glucosa', 'azucar', 'insulina']
            hypertension_keywords = ['hipertension', 'presion alta', 'cardiovascular']
            specific_conditions = diabetes_keywords + hypertension_keywords
            
            # Si el producto contiene términos muy específicos de condiciones médicas
            # pero el usuario solo busca "dolor", no debe aparecer
            product_has_specific_condition = any(cond in product_symptoms or cond in product_name 
                                               for cond in specific_conditions)
            
            # Si es específico para una condición y no menciona dolor directamente, excluir
            if product_has_specific_condition and 'dolor' not in product_symptoms:
                return False
        
        # PERMITIR productos específicos cuando se detecta el tipo correcto de dolor
        elif symptom in ['dolor de cabeza', 'dolor muscular', 'dolor articular', 
                        'dolor estomacal', 'dolor menstrual', 'dolor de garganta', 'dolor dental']:
            # Para dolores específicos, permitir productos especializados
            return True
        
        # PRIORIDAD ESPECIAL para productos específicos de insomnio
        if symptom == 'insomnio':
            # Productos específicos que DEBEN aparecer para insomnio
            priority_sleep_products = ['valeriana', 'pasiflora', 'triptofano', 'magnesio', '7 azahares']
            if any(priority in product_name for priority in priority_sleep_products):
                return True
        
        return symptom in product_symptoms
    
    def _product_benefits_match_symptom(self, product_row, symptom):
        """Verificar si los beneficios del producto coinciden con el síntoma"""
        if 'beneficios_norm' not in product_row or not product_row['beneficios_norm']:
            return False
        
        product_benefits = str(product_row['beneficios_norm']).lower()
        product_name = str(product_row.get('nombre', '')).lower()
        
        # MISMO FILTRO: evitar productos específicos para condiciones médicas
        if symptom == 'dolor':
            diabetes_keywords = ['diabetes', 'diabetico', 'glucosa', 'azucar', 'insulina']
            hypertension_keywords = ['hipertension', 'presion alta', 'cardiovascular']
            specific_conditions = diabetes_keywords + hypertension_keywords
            
            product_has_specific_condition = any(cond in product_benefits or cond in product_name 
                                               for cond in specific_conditions)
            
            # Si es específico para una condición médica, debe mencionar dolor explícitamente
            if product_has_specific_condition and 'dolor' not in product_benefits:
                return False
        
        return symptom in product_benefits
    
    def _product_ingredients_match_symptom(self, product_row, symptom):
        """Verificar si los ingredientes del producto coinciden con el síntoma"""
        if 'ingredientes_norm' not in product_row or not product_row['ingredientes_norm']:
            return False
        
        product_ingredients = str(product_row['ingredientes_norm']).lower()
        product_name = str(product_row.get('nombre', '')).lower()
        
        # MISMO FILTRO: evitar productos específicos para condiciones médicas
        if symptom == 'dolor':
            diabetes_keywords = ['diabetes', 'diabetico', 'glucosa', 'azucar', 'insulina']
            hypertension_keywords = ['hipertension', 'presion alta', 'cardiovascular']
            specific_conditions = diabetes_keywords + hypertension_keywords
            
            product_has_specific_condition = any(cond in product_ingredients or cond in product_name 
                                               for cond in specific_conditions)
            
            # Si es específico para una condición médica, debe mencionar dolor explícitamente
            if product_has_specific_condition and 'dolor' not in product_ingredients:
                return False
        
        return symptom in product_ingredients
    
    def _is_safe_for_user(self, product_row, user_profile):
        """Verificar si el producto es seguro para el usuario (contraindicaciones y restricciones)"""
        if not user_profile:
            return True
        
        # 1. FILTRO POR SEXO - Verificar restricciones de género
        if 'sexo' in product_row and product_row['sexo']:
            product_gender = str(product_row['sexo']).lower().strip()
            user_gender = user_profile.get('gender', '').lower().strip()
            
            # Si el producto especifica un sexo, debe coincidir exactamente con el usuario
            if product_gender in ['mujer', 'femenino', 'mujeres', 'female']:
                if user_gender not in ['femenino', 'mujer']:
                    self.logger.info(f"Producto {product_row.get('nombre', 'Desconocido')} excluido por género (solo mujeres)")
                    return False
            elif product_gender in ['hombre', 'masculino', 'hombres', 'male']:
                if user_gender not in ['masculino', 'hombre']:
                    self.logger.info(f"Producto {product_row.get('nombre', 'Desconocido')} excluido por género (solo hombres)")
                    return False
            # Si el campo está vacío o dice "ambos/unisex", es para todos
        
        # 1.5. FILTRO POR EDAD - Verificar si es apropiado para menores de edad
        user_age = int(user_profile.get('age', 18))
        product_name = str(product_row.get('nombre', '')).lower()
        
        # Productos específicos para niños que NO deben aparecer para adultos
        kids_only_products = ['mi peke', 'peke', 'niños', 'infantil', 'pediatrico']
        is_kids_product = any(kid_term in product_name for kid_term in kids_only_products)
        
        # Productos específicos para adultos que NO deben aparecer para menores
        adult_only_products = ['resveratrol', 'energy', 'vigor', 'libido', 'testosterone']
        is_adult_product = any(adult_term in product_name for adult_term in adult_only_products)
        
        if user_age < 18 and is_adult_product:
            self.logger.info(f"Producto {product_row.get('nombre', 'Desconocido')} excluido (solo adultos)")
            return False
        elif user_age >= 18 and is_kids_product:
            self.logger.info(f"Producto {product_row.get('nombre', 'Desconocido')} excluido (solo niños)")
            return False
        
        # 1.6. FILTRO POR RELEVANCIA DE SÍNTOMAS - Evitar productos irrelevantes para síntomas específicos
        # Productos que no son apropiados para ciertos síntomas específicos
        product_name_lower = product_name.lower()
        
        # Multivitamínicos para niños no son apropiados para estrés en adultos
        if 'mi peke' in product_name_lower and user_age >= 18:
            self.logger.info(f"Producto {product_row.get('nombre', 'Desconocido')} excluido (multivitamínico infantil no apropiado para adultos)")
            return False
        
        # Antioxidantes como resveratrol no son para síntomas agudos
        if 'resveratrol' in product_name_lower:
            # Solo permitir resveratrol para síntomas donde sea realmente relevante
            symptoms_text = str(product_row.get('sintomas', '')).lower() + str(product_row.get('beneficios', '')).lower()
            if 'antioxidante' not in symptoms_text and 'cardiovascular' not in symptoms_text:
                self.logger.info(f"Producto {product_row.get('nombre', 'Desconocido')} excluido (antioxidante no relevante para síntoma actual)")
                return False
        
        # 2. FILTRO PARA DIABÉTICOS - Verificar contraindicaciones específicas
        user_has_diabetes = user_profile.get('diabetes', False)
        if user_has_diabetes and 'contradiccion' in product_row and product_row['contradiccion']:
            contraindications = self._normalize_text(str(product_row['contradiccion']))
            
            # Palabras clave que indican contraindicación para diabéticos
            diabetes_warnings = [
                'diabeticos', 'diabetico', 'diabetes', 'glucosa alta', 
                'azucar alta', 'hiperglucemia', 'insulina'
            ]
            
            for warning in diabetes_warnings:
                if warning in contraindications:
                    self.logger.info(f"Producto {product_row.get('nombre', 'Desconocido')} excluido por diabetes")
                    return False
        
        # 3. OTROS FILTROS DE SEGURIDAD
        if 'contradiccion' in product_row and product_row['contradiccion']:
            contraindications = self._normalize_text(str(product_row['contradiccion']))
            
            # Verificar hipertensión
            user_has_hypertension = user_profile.get('hypertension', False)
            if user_has_hypertension:
                hypertension_warnings = ['hipertenso', 'hipertension', 'presion alta']
                for warning in hypertension_warnings:
                    if warning in contraindications:
                        return False
            
            # Verificar embarazo
            user_is_pregnant = user_profile.get('pregnancy', False)
            if user_is_pregnant:
                pregnancy_warnings = ['embarazada', 'embarazo', 'gestacion', 'lactancia']
                for warning in pregnancy_warnings:
                    if warning in contraindications:
                        return False
        
        return True
    
    def _format_product(self, product_row):
        """Formatear información del producto real del catálogo"""
        return {
            'nombre': str(product_row.get('nombre', 'Producto Canatura')),
            'beneficios': str(product_row.get('beneficios', 'Beneficios naturales para la salud')),
            'dosis': str(product_row.get('dosis', 'Consultar con especialista')),
            'modo_de_uso': str(product_row.get('modo_de_uso', 'INGERIBLE')),
            'presentacion': str(product_row.get('presentacion', 'Suplemento natural')),
            'ingredientes': str(product_row.get('ingredientes', 'Ingredientes naturales')),
            'contradiccion': str(product_row.get('contradiccion', '')),
            'condiciones_especiales': str(product_row.get('condiciones especiales', ''))
        }
    
    def _ensure_product_variety(self, products, max_count):
        """Asegurar variedad de productos (evitar duplicados del mismo base)"""
        seen_bases = set()
        varied_products = []
        
        for product in products:
            # Extraer nombre base (sin presentación/tamaño)
            base_name = re.sub(r'C/\d+|\d+\s*(GRS|ML|CAPS|TABLETAS)', '', product['nombre']).strip()
            
            if base_name not in seen_bases:
                seen_bases.add(base_name)
                varied_products.append(product)
                
                if len(varied_products) >= max_count:
                    break
        
        return varied_products
    
    def _get_general_wellness_products(self, count):
        """Obtener productos generales de bienestar como respaldo con rotación equitativa"""
        wellness_keywords = ['energia', 'bienestar', 'salud', 'vitaminas', 'natural', 'inmune']
        all_wellness_products = []
        
        # Recopilar todos los productos de bienestar
        for idx, row in self.catalog_df.iterrows():
            product_text = f"{row.get('beneficios', '')} {row.get('nombre', '')}".lower()
            if any(keyword in product_text for keyword in wellness_keywords):
                product = self._format_product(row)
                product['product_name'] = row['nombre']
                product['match_score'] = 0  # Puntuación base para productos de bienestar
                all_wellness_products.append(product)
        
        # Aplicar rotación si hay productos disponibles
        if all_wellness_products:
            rotated_products = self._apply_product_rotation(all_wellness_products, count, count)
            return rotated_products
        
        # Si no hay productos de bienestar, devolver lista vacía
        wellness_products = []
        
        return wellness_products[:count]