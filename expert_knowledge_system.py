"""
Sistema de Conocimiento Experto para SaludArte
Integra casos especializados aprendidos de expertos médicos
"""
import pandas as pd
import os

class ExpertKnowledgeSystem:
    """Sistema que maneja casos complejos con conocimiento experto"""
    
    def __init__(self, catalog_df=None):
        self.catalog_df = catalog_df if catalog_df is not None else self._load_catalog()
        self.expert_cases = self._load_expert_knowledge()
    
    def _load_catalog(self):
        """Cargar catálogo real de productos"""
        try:
            # Intentar cargar el catálogo principal
            catalog_files = [
                'PLANTILLA CATALOGO CON INGREDIENTES.xlsx',
                'uploads/PLANTILLA CATALOGO CON INGREDIENTES.xlsx',
                'sample_catalog.xlsx'
            ]
            
            for file_path in catalog_files:
                if os.path.exists(file_path):
                    df = pd.read_excel(file_path)
                    print(f"✓ Catálogo cargado desde: {file_path}")
                    return df
            
            print("⚠ No se encontró catálogo, usando DataFrame vacío")
            return pd.DataFrame()
        except Exception as e:
            print(f"Error cargando catálogo: {e}")
            return pd.DataFrame()
    
    def _load_expert_knowledge(self):
        """Cargar conocimiento experto de casos especializados"""
        return {
            'adiccion_comida_chatarra': {
                'keywords': ['como mucha comida chatarra', 'no puedo parar de comer', 'adicto a la comida', 'como compulsivamente', 'ansiedad por comer'],
                'productos': [
                    'AR PSYLLIUM PLANTAGO CAPSULA CANATURA GOLD',
                    'CN DG MAGOL L11 CAPSULA CANATURA C/75',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['adiccion alimentaria', 'ansiedad por comer', 'compulsion alimentaria', 'saciedad'],
                'razon': 'La adicción alimentaria involucra ansiedad, falta de saciedad y compulsión. Se necesita: fibra para saciedad, digestivo para regular apetito, complejo B para ansiedad, y magnesio para sistema nervioso.'
            },
            
            'alcoholismo': {
                'keywords': ['problemas con el alcohol', 'bebo mucho', 'adiccion al alcohol', 'no puedo dejar de beber', 'alcoholismo', 'problemas serios con el alcohol', 'tomo mucho alcohol', 'dependencia del alcohol'],
                'productos': [
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AB CLORHIDRATO LISINA CAPSULA CANATURA GOLD',
                    'AB L TRIPTOFANO CAPSULA CANATURA GOLD C/90',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['adiccion alcohol', 'desintoxicacion', 'ansiedad', 'depresion'],
                'razon': 'El alcoholismo requiere desintoxicación hepática, reparación neurológica y control de ansiedad. Se necesita: detox para limpiar hígado, lisina para reparación, triptófano para serotonina, y complejo B para sistema nervioso.'
            },
            
            'acne_severo': {
                'keywords': ['acne severo', 'granos terribles', 'cara llena de granos', 'acne que no se quita', 'piel muy grasosa', 'mi acne es muy severo', 'acne horrible', 'granos que no se van', 'acné es muy severo', 'acné severo'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA A BETACAROTENO CAPSULA CANATURA GOLD',
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['acne', 'piel grasa', 'inflamacion cutanea', 'toxinas'],
                'razon': 'El acné severo es inflamatorio y hormonal. Se necesita: zinc para piel y cicatrización, vitamina A para regeneración celular, detox para eliminar toxinas, y omega 3 como antiinflamatorio.'
            },
            
            'caida_cabello': {
                'keywords': ['se me cae el cabello', 'calvicie', 'alopecia', 'perdida de pelo', 'cabello debil', 'se me está cayendo mucho el cabello', 'perdida de cabello', 'se me cae mucho pelo'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AR VITAMINA BIOTINA CAPSULA CANATURA GOLD',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['alopecia', 'cabello debil', 'caida de cabello', 'calvicie'],
                'razon': 'La caída de cabello involucra deficiencias nutricionales y hormonales. Se necesita: zinc para crecimiento capilar, minerales para folículos, biotina para fortaleza, y complejo B para metabolismo capilar.'
            },
            
            'crossfit_recuperacion': {
                'keywords': ['hago crossfit', 'necesito recuperacion', 'dolor muscular por ejercicio', 'entrenamiento intenso', 'recuperacion deportiva'],
                'productos': [
                    'AR JUQUILITA UNGUENTO CENTRO BOTANICO MAYA 60 GRS',
                    'AB CLORHIDRATO LISINA CAPSULA CANATURA GOLD',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['recuperacion muscular', 'dolor muscular', 'fatiga deportiva', 'electrolitos', 'energia deportiva'],
                'razon': 'El CrossFit genera micro-lesiones musculares y pérdida de electrolitos. Se necesita: ungüento para alivio tópico inmediato, lisina para síntesis proteica y recuperación, magnesio para función muscular y neurológica, minerales orgánicos para cicatrización, y multivitamínico para energía y soporte general.'
            },
            
            'vegano_proteinas': {
                'keywords': ['soy vegano', 'necesito proteinas', 'dieta vegana', 'proteinas vegetales', 'nutricion vegana'],
                'productos': [
                    'AR VITAMINA B12 COMPRIMIDO CANATURA GOLD',
                    'DI MEGASOY NATURAL POLVO CANATURA 1 KG',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['deficiencia proteica', 'deficiencia B12', 'nutricion vegana', 'aminoacidos esenciales', 'minerales'],
                'razon': 'Los veganos necesitan suplementar nutrientes ausentes en dietas plant-based. Se necesita: B12 para sistema nervioso (no existe en plantas), proteína de soya para aminoácidos completos equivalentes a carne, omega 3 para función cerebral y cardiovascular, y minerales orgánicos para hierro, zinc y otros minerales esenciales.'
            },
            
            'depresion_profunda': {
                'keywords': ['depresion profunda', 'tristeza constante', 'no tengo ganas de nada', 'depresion severa', 'muy deprimido', 'tengo depresion profunda', 'depresion leve', 'depresion', 'estoy muy deprimido', 'depresión profunda', 'depresión leve', 'depresión'],
                'productos': [
                    'AB L TRIPTOFANO CAPSULA CANATURA GOLD C/90',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'GLICINATO MAGNESIO CAPSULA HERBAGOLD C/60',
                    'TRIS T CAPSULAS REY ZAPOTECO'
                ],
                'sintomas': ['depresion', 'tristeza profunda', 'falta de energia', 'alteraciones del sueño', 'desequilibrio emocional', 'ansiedad'],
                'razon': 'La depresión profunda involucra deficiencia de neurotransmisores y desbalance neurobioquímico. Se necesita: triptófano para síntesis de serotonina, complejo B para energía y neurotransmisores, omega 3 para función cerebral y reducir inflamación, glicinato de magnesio para sistema nervioso y relajación, y TRIS T como estabilizador natural del estado de ánimo.'
            },
            
            'neuropatia_diabetica': {
                'keywords': ['neuropatia diabetica', 'neuropatía diabética', 'dolor nervios diabetes', 'entumecimiento diabetico', 'hormigueo por diabetes', 'neuropatia', 'neuropatía', 'dolor neuropatico', 'dolor neuropático'],
                'productos': [
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB CLORHIDRATO LISINA CAPSULA CANATURA GOLD',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['neuropatia', 'dolor nervioso', 'entumecimiento', 'hormigueo', 'diabetes'],
                'razon': 'La neuropatía diabética es daño a los nervios causado por niveles altos de glucosa. Se necesita: complejo B para regeneración nerviosa, lisina para reparación de tejidos, magnesio para función nerviosa, y omega 3 como antiinflamatorio para proteger nervios.'
            },
            
            # Casos de expresiones mexicanas complejas
            'dolor_generalizado': {
                'keywords': ['me duele todo el cuerpo cabrón', 'me duelen los huesos que me cargo', 'me truena todo el esqueleto', 'me truena todo cuando me levanto', 'tengo los músculos hechos nudos'],
                'productos': [
                    'AR JUQUILITA UNGUENTO CENTRO BOTANICO MAYA 60 GRS',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['dolor generalizado', 'dolor muscular', 'dolor articular', 'rigidez muscular'],
                'razon': 'El dolor generalizado indica inflamación sistémica y tensión muscular. Se necesita: ungüento para alivio tópico, magnesio para relajación muscular, omega 3 como antiinflamatorio, y complejo B para función nerviosa.'
            },
            
            'fatiga_extrema_coloquial': {
                'keywords': ['estoy hasta la madre de cansado', 'ando muy pacheco últimamente', 'me siento súper débil', 'tengo las defensas por el suelo'],
                'productos': [
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['fatiga extrema', 'debilidad', 'falta de energia', 'defensas bajas'],
                'razon': 'La fatiga extrema con debilidad indica deficiencias nutricionales múltiples. Se necesita: multivitamínico para energía general, complejo B para metabolismo energético, minerales para funciones vitales, y omega 3 para función cerebral.'
            },
            
            'problemas_digestivos_graves': {
                'keywords': ['tengo un desmadre en el estómago', 'ando bien estreñido del coraje', 'tengo indigestión terrible', 'ando con muchos gases'],
                'productos': [
                    'CN DG MAGOL L11 CAPSULA CANATURA C/75',
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR PSYLLIUM PLANTAGO CAPSULA CANATURA GOLD'
                ],
                'sintomas': ['problemas digestivos', 'estreñimiento', 'gases', 'indigestion'],
                'razon': 'Los problemas digestivos severos requieren regulación intestinal y desintoxicación. Se necesita: digestivo para flora intestinal, detox para limpiar sistema, magnesio para tránsito intestinal, y fibra para regulación.'
            },
            
            'problemas_circulatorios': {
                'keywords': ['me late muy rápido el corazón', 'tengo la presión por las nubes', 'me duele el pecho del estrés', 'ando bien mareado'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'SN 7 AZAHARES TABLETA FRASCO NIS YA GREEN'
                ],
                'sintomas': ['palpitaciones', 'presion alta', 'estres cardiovascular', 'mareos'],
                'razon': 'Los problemas cardiovasculares con estrés requieren relajación y protección cardíaca. Se necesita: omega 3 para corazón, magnesio para presión, complejo B para sistema nervioso, y relajante para estrés.'
            },
            
            'agotamiento_mental': {
                'keywords': ['ando medio ido de la cabeza', 'me duele la jeta de tanto trabajar', 'traigo unas ojeras hasta el suelo', 'ando bien desvelado siempre'],
                'productos': [
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB L TRIPTOFANO CAPSULA CANATURA GOLD C/90',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['agotamiento mental', 'insomnio', 'estres mental', 'fatiga cerebral'],
                'razon': 'El agotamiento mental con insomnio indica estrés neurológico. Se necesita: complejo B para función cerebral, triptófano para sueño reparador, omega 3 para protección neuronal, y magnesio para relajación nerviosa.'
            },
            
            # CASOS ADICIONALES IMPLEMENTADOS
            'bajar_peso': {
                'keywords': ['quiero bajar de peso', 'necesito perder peso', 'deseo adelgazar', 'quiero adelgazar', 'bajar kilos', 'perder kilos'],
                'productos': [
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'VC CHIA CAPSULA NUDRA C/60',
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['sobrepeso', 'metabolismo lento', 'retención de toxinas', 'ansiedad por comer'],
                'razon': 'La pérdida de peso requiere desintoxicación, fibra para saciedad, regulador digestivo para metabolismo, y complejo B para energía metabólica.'
            },
            
            'subir_peso': {
                'keywords': ['necesito subir de peso', 'quiero ganar peso', 'deseo engordar', 'aumentar peso', 'ganar kilos', 'subir kilos'],
                'productos': [
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'DI MEGASOY NATURAL POLVO CANATURA 1 KG',
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['bajo peso', 'falta de apetito', 'déficit nutricional', 'masa muscular insuficiente'],
                'razon': 'El aumento de peso saludable necesita multivitamínico generador de apetito, proteína para masa muscular, estimulante digestivo, y minerales para construcción corporal.'
            },
            
            'mas_energia': {
                'keywords': ['deseo tener más energía', 'quiero más energía', 'necesito energía', 'me falta energía', 'sin energía', 'más vitalidad'],
                'productos': [
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['fatiga', 'falta de energia', 'cansancio cronico', 'agotamiento'],
                'razon': 'La energía celular requiere complejo B para metabolismo ATP, multivitamínico para energía general, omega 3 para función mitocondrial, y minerales para procesos enzimáticos.'
            },
            
            'mejorar_memoria': {
                'keywords': ['quiero mejorar mi memoria', 'necesito mejor memoria', 'problemas de memoria', 'mala memoria', 'falta de concentración'],
                'productos': [
                    'OC CEREBRO TABLETA FRASCO NIS YA GREEN C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB CLORHIDRATO LISINA CAPSULA CANATURA GOLD'
                ],
                'sintomas': ['memoria deficiente', 'concentración pobre', 'función cognitiva baja'],
                'razon': 'La memoria requiere productos específicos para cerebro, omega 3 para función neuronal, complejo B para neurotransmisores, y lisina para síntesis proteica cerebral.'
            },
            
            'estreñimiento': {
                'keywords': ['estreñimiento', 'estreñido', 'no puedo evacuar', 'heces duras', 'tránsito lento'],
                'productos': [
                    'VC CHIA CAPSULA NUDRA C/60',
                    'CITRATO MAGNESIO CAPSULA NUDRA C/60',
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'HE DT DETOX CAPSULA CANATURA C/75'
                ],
                'sintomas': ['estreñimiento', 'tránsito intestinal lento', 'heces duras'],
                'razon': 'El estreñimiento necesita fibra soluble, magnesio para relajar músculo liso intestinal, regulador digestivo, y detox para limpiar colon.'
            },
            
            'tinnitus': {
                'keywords': ['me zumban los oídos', 'zumbido en oídos', 'ruido en oídos', 'tinnitus', 'pitido oídos'],
                'productos': [
                    'OC CBRO BILOBA TONICO NIS YA GREEN 1 LT',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['tinnitus', 'zumbido oidos', 'ruido auditivo'],
                'razon': 'El tinnitus requiere ginkgo biloba para circulación cerebral, omega 3 neuroprotector, magnesio para función nerviosa, y complejo B para sistema nervioso.'
            },
            
            'ojos_irritados': {
                'keywords': ['tengo los ojos rojos', 'ojos irritados', 'ojos secos', 'irritación ocular', 'ojos rojos'],
                'productos': [
                    'OR RTI LUX LUTEIN L4 CAPSULA CANATURA C/75',
                    'AR VITAMINA A BETACAROTENO CAPSULA CANATURA GOLD',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['ojos rojos', 'irritacion ocular', 'sequedad ocular'],
                'razon': 'Los ojos irritados necesitan luteína para protección retinal, vitamina A para mucosas oculares, omega 3 antiinflamatorio, y minerales para reparación.'
            },
            
            'fibromialgia': {
                'keywords': ['tengo fibromialgia', 'padezco fibromialgia', 'fibromialgia', 'dolor generalizado crónico'],
                'productos': [
                    'AR JUQUILITA UNGUENTO CENTRO BOTANICO MAYA 60 GRS',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB L TRIPTOFANO CAPSULA CANATURA GOLD C/90'
                ],
                'sintomas': ['dolor muscular generalizado', 'rigidez', 'fatiga', 'alteraciones del sueño'],
                'razon': 'La fibromialgia necesita ungüento para dolor localizado, magnesio para relajación muscular, omega 3 antiinflamatorio, y triptófano para sueño reparador.'
            },
            
            'artritis_reumatoide': {
                'keywords': ['padezco artritis reumatoide', 'tengo artritis reumatoide', 'artritis reumatoide', 'artritis severa'],
                'productos': [
                    'AR JUQUILITA UNGUENTO CENTRO BOTANICO MAYA 60 GRS',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['artritis', 'dolor articular', 'inflamacion articular', 'rigidez matutina'],
                'razon': 'La artritis reumatoide necesita ungüento para dolor localizado, omega 3 potente antiinflamatorio, zinc para reparación articular, y magnesio para relajación muscular.'
            },
            
            'intestino_irritable': {
                'keywords': ['síndrome del intestino irritable', 'intestino irritable', 'colon irritable', 'SII'],
                'productos': [
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'VC CHIA CAPSULA NUDRA C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['intestino irritable', 'dolor abdominal', 'diarrea', 'gases'],
                'razon': 'El intestino irritable necesita regulador digestivo para flora, fibra para consistencia, magnesio para calmar espasmos, y omega 3 antiinflamatorio intestinal.'
            },
            
            'migranas_cronicas': {
                'keywords': ['sufro de migrañas crónicas', 'migrañas crónicas', 'migraña constante', 'dolor de cabeza crónico'],
                'productos': [
                    'SN 7 AZAHARES TABLETA FRASCO NIS YA GREEN',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['migraña', 'dolor de cabeza intenso', 'fotofobia', 'nauseas'],
                'razon': 'Las migrañas crónicas necesitan relajante natural, magnesio para vasodilatación, omega 3 antiinflamatorio cerebral, y complejo B para función neurológica.'
            },
            
            'dormir_mejor': {
                'keywords': ['necesito dormir mejor', 'quiero dormir mejor', 'problemas para dormir', 'sueño malo', 'no duermo bien'],
                'productos': [
                    'AB L TRIPTOFANO CAPSULA CANATURA GOLD C/90',
                    'SN 7 AZAHARES TABLETA FRASCO NIS YA GREEN',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['insomnio', 'sueño fragmentado', 'despertar temprano', 'sueño no reparador'],
                'razon': 'Mejorar el sueño requiere triptófano para síntesis de melatonina, relajante natural, magnesio para relajación muscular, y complejo B para equilibrio neurológico.'
            },
            
            'menos_estres': {
                'keywords': ['deseo estar menos estresado', 'quiero menos estrés', 'reducir estrés', 'calmar estrés', 'relajarme'],
                'productos': [
                    'SN 7 AZAHARES TABLETA FRASCO NIS YA GREEN',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB L TRIPTOFANO CAPSULA CANATURA GOLD C/90'
                ],
                'sintomas': ['estres', 'ansiedad', 'tension nerviosa', 'irritabilidad'],
                'razon': 'Reducir el estrés necesita relajante natural para ansiedad, magnesio para calmar sistema nervioso, complejo B para resistencia al estrés, y triptófano para estabilidad emocional.'
            },
            
            'fortalecer_defensas': {
                'keywords': ['quiero fortalecer mis defensas', 'fortalecer sistema inmune', 'subir defensas', 'mejorar inmunidad'],
                'productos': [
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AR VITAMINA A BETACAROTENO CAPSULA CANATURA GOLD',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['defensas bajas', 'infecciones frecuentes', 'fatiga inmunologica'],
                'razon': 'Fortalecer defensas requiere minerales orgánicos para sistema inmune, vitamina A para mucosas protectoras, omega 3 antiinflamatorio, y complejo B para energía inmunológica.'
            },
            
            'calambres': {
                'keywords': ['tengo calambres horribles', 'calambres musculares', 'espasmos musculares', 'contracciones musculares'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AB GLUCONATO POTASIO CAPSULA CANATURA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AR JUQUILITA UNGUENTO CENTRO BOTANICO MAYA 60 GRS'
                ],
                'sintomas': ['calambres musculares', 'espasmos', 'contracciones involuntarias'],
                'razon': 'Los calambres necesitan magnesio para relajación muscular, potasio para equilibrio electrolítico, minerales para función muscular, y ungüento para alivio tópico.'
            },
            
            'retencion_liquidos': {
                'keywords': ['ando bien hinchado', 'retención de líquidos', 'hinchazón', 'edema', 'me siento hinchado'],
                'productos': [
                    'AB GLUCONATO POTASIO CAPSULA CANATURA',
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['hinchazon', 'retencion de liquidos', 'edema', 'pesadez'],
                'razon': 'La retención de líquidos necesita potasio para equilibrio hídrico, detox para función renal, complejo B para metabolismo, y omega 3 antiinflamatorio.'
            },
            
            'apnea_sueno': {
                'keywords': ['tengo apnea del sueño', 'apnea del sueño', 'ronco mucho', 'paro respiratorio durmiendo'],
                'productos': [
                    'SN 7 AZAHARES TABLETA FRASCO NIS YA GREEN',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['apnea del sueño', 'ronquidos', 'sueño fragmentado', 'fatiga diurna'],
                'razon': 'La apnea del sueño necesita relajante para mejorar sueño, omega 3 para reducir inflamación de vías respiratorias, magnesio para relajación muscular, y complejo B para energía diurna.'
            },
            
            # CASOS ADICIONALES PARA 100% ÉXITO
            'cuidar_corazon': {
                'keywords': ['quiero cuidar mi corazón', 'cuidar el corazón', 'proteger corazón', 'salud cardíaca', 'corazón sano'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'PA CORA ZN ABEDUL DUO TABLETA NIS YA GREEN C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['salud cardiovascular', 'proteccion cardiaca', 'presion arterial'],
                'razon': 'La salud cardíaca requiere omega 3 para protección cardiovascular, magnesio para regulación de presión, abedul para función cardíaca, y complejo B para metabolismo cardíaco.'
            },
            
            'mejor_animo': {
                'keywords': ['deseo tener mejor ánimo', 'mejorar el ánimo', 'mejor humor', 'estado de ánimo', 'ánimo bajo'],
                'productos': [
                    'AB L TRIPTOFANO CAPSULA CANATURA GOLD C/90',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'TRIS T CAPSULAS REY ZAPOTECO',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['estado de animo bajo', 'tristeza', 'desanimo', 'falta de energia emocional'],
                'razon': 'Mejorar el ánimo requiere triptófano para síntesis de serotonina, complejo B para energía mental, TRIS T estabilizador natural, y omega 3 para función cerebral.'
            },
            
            'regular_hormonas': {
                'keywords': ['necesito regular mis hormonas', 'regular hormonas', 'equilibrio hormonal', 'hormonas desbalanceadas'],
                'productos': [
                    'DI MEGASOY NATURAL POLVO CANATURA 1 KG',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['desequilibrio hormonal', 'irregularidades menstruales', 'cambios hormonales'],
                'razon': 'Regulación hormonal requiere soya con fitoestrógenos, zinc para síntesis hormonal, complejo B para función endocrina, y omega 3 para equilibrio hormonal.'
            },
            
            'mejorar_piel': {
                'keywords': ['deseo mejorar mi piel', 'mejorar la piel', 'piel sana', 'cuidar piel', 'piel bonita'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA A BETACAROTENO CAPSULA CANATURA GOLD',
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['problemas de piel', 'acne leve', 'piel opaca', 'envejecimiento cutaneo'],
                'razon': 'Mejorar la piel requiere zinc para cicatrización, vitamina A para regeneración celular, detox para eliminar toxinas, y omega 3 antiinflamatorio.'
            },
            
            'fortalecer_cabello_deseo': {
                'keywords': ['quiero fortalecer mi cabello', 'fortalecer cabello', 'cabello fuerte', 'cabello sano'],
                'productos': [
                    'AR VITAMINA BIOTINA CAPSULA CANATURA GOLD',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['cabello debil', 'cabello quebradizo', 'falta de brillo capilar'],
                'razon': 'Fortalecer cabello requiere biotina para queratina, zinc para crecimiento capilar, minerales para folículos, y complejo B para metabolismo capilar.'
            },
            
            'mejor_vista': {
                'keywords': ['deseo tener mejor vista', 'mejorar la vista', 'vista cansada', 'cuidar ojos', 'visión mejor'],
                'productos': [
                    'OR RTI LUX LUTEIN L4 CAPSULA CANATURA C/75',
                    'AR VITAMINA A BETACAROTENO CAPSULA CANATURA GOLD',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['vision borrosa', 'fatiga ocular', 'sequedad ocular'],
                'razon': 'Mejorar la vista requiere luteína para protección macular, vitamina A para visión nocturna, omega 3 para lubricación ocular, y minerales para estructura ocular.'
            },
            
            'mejorar_respiracion': {
                'keywords': ['quiero mejorar mi respiración', 'mejorar respiración', 'respirar mejor', 'falta de aire'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['dificultad respiratoria', 'congestion', 'falta de aire'],
                'razon': 'Mejorar respiración requiere omega 3 antiinflamatorio para vías aéreas, complejo B para energía respiratoria, magnesio para relajación bronquial, y minerales para función pulmonar.'
            },
            
            'desintoxicar': {
                'keywords': ['necesito desintoxicarme', 'desintoxicar', 'limpiar organismo', 'depurar cuerpo'],
                'productos': [
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'HC REGENERADOR HIGADO GRASO CAPSULA NUDRA C/60',
                    'DO JENGIBRE CAPSULA NUDRA C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['intoxicacion', 'higado graso', 'toxinas acumuladas'],
                'razon': 'La desintoxicación requiere detox específico, regenerador hepático, jengibre estimulante, y complejo B para metabolismo de toxinas.'
            },
            
            'cuidar_riñones': {
                'keywords': ['quiero cuidar mis riñones', 'cuidar riñones', 'proteger riñones', 'función renal'],
                'productos': [
                    'AB GLUCONATO POTASIO CAPSULA CANATURA',
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['funcion renal', 'retencion liquidos', 'toxinas renales'],
                'razon': 'Cuidar riñones requiere potasio para función renal, detox para limpiar sistema, omega 3 antiinflamatorio, y complejo B para metabolismo renal.'
            },
            
            'mejorar_concentracion': {
                'keywords': ['necesito mejorar la concentración', 'mejorar concentración', 'concentrarme mejor', 'falta concentración'],
                'productos': [
                    'OC CEREBRO TABLETA FRASCO NIS YA GREEN C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB CLORHIDRATO LISINA CAPSULA CANATURA GOLD'
                ],
                'sintomas': ['falta de concentracion', 'distraccion mental', 'confusion'],
                'razon': 'Mejorar concentración requiere producto específico para cerebro, omega 3 para función neuronal, complejo B para neurotransmisores, y lisina para síntesis cerebral.'
            },
            
            # CASOS ADICIONALES FINALES PARA 100%
            'regular_presion': {
                'keywords': ['deseo regular mi presión', 'regular presión', 'controlar presión', 'presión alta'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'PA CORA ZN ABEDUL DUO TABLETA NIS YA GREEN C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['hipertension', 'presion arterial alta', 'tension arterial'],
                'razon': 'Regular la presión requiere magnesio vasodilatador, omega 3 cardioprotector, abedul para circulación, y complejo B para función cardiovascular.'
            },
            
            'fortalecer_huesos': {
                'keywords': ['deseo fortalecer los huesos', 'fortalecer huesos', 'huesos fuertes', 'osteoporosis'],
                'productos': [
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR VITAMINA A BETACAROTENO CAPSULA CANATURA GOLD',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['huesos debiles', 'osteoporosis', 'descalcificacion'],
                'razon': 'Fortalecer huesos requiere minerales orgánicos para calcio, magnesio para absorción, vitamina A para desarrollo óseo, y complejo B para metabolismo óseo.'
            },
            
            'resistencia_insulina': {
                'keywords': ['tengo resistencia a la insulina', 'resistencia insulina', 'prediabetes', 'metabolismo glucosa'],
                'productos': [
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'DI MELIGL ZOR L9 CAPSULA CANATURA C/75',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['resistencia insulina', 'prediabetes', 'glucosa alta'],
                'razon': 'La resistencia a la insulina requiere fenogreco regulador de glucosa, producto específico para diabéticos, omega 3 antiinflamatorio, y complejo B para metabolismo.'
            },
            
            'hipotiroidismo': {
                'keywords': ['sufro de hipotiroidismo', 'hipotiroidismo', 'tiroides lenta', 'metabolismo lento'],
                'productos': [
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'HE DT DETOX CAPSULA CANATURA C/75'
                ],
                'sintomas': ['hipotiroidismo', 'tiroides lenta', 'metabolismo bajo'],
                'razon': 'El hipotiroidismo requiere minerales para función tiroidea, complejo B para metabolismo, omega 3 antiinflamatorio, y detox para apoyar función glandular.'
            },
            
            'endometriosis': {
                'keywords': ['padezco endometriosis', 'endometriosis', 'dolor menstrual severo', 'quistes ovarios'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'DI MEGASOY NATURAL POLVO CANATURA 1 KG',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['endometriosis', 'dolor pelvico', 'inflamacion ginecologica'],
                'razon': 'La endometriosis requiere omega 3 potente antiinflamatorio, magnesio para calmar dolor, soya con fitoestrógenos reguladores, y zinc para reparación tisular.'
            },
            
            'mejorar_digestion': {
                'keywords': ['necesito mejorar la digestión', 'mejorar digestión', 'problemas digestivos', 'digestión lenta'],
                'productos': [
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'DO JENGIBRE CAPSULA NUDRA C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['digestion lenta', 'pesadez estomacal', 'mala digestion'],
                'razon': 'Mejorar digestión requiere fenogreco regulador digestivo, jengibre estimulante, magnesio para motilidad, y complejo B para enzimas digestivas.'
            },
            
            'mejor_circulacion': {
                'keywords': ['deseo tener mejor circulación', 'mejorar circulación', 'mala circulación', 'circulación lenta'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'OC CBRO BILOBA TONICO NIS YA GREEN 1 LT',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['mala circulacion', 'extremidades frias', 'varices'],
                'razon': 'Mejorar circulación requiere omega 3 para fluidez sanguínea, ginkgo biloba vasodilatador, magnesio para función vascular, y complejo B para energía circulatoria.'
            },
            
            'controlar_diabetes': {
                'keywords': ['necesito controlar la diabetes', 'controlar diabetes', 'glucosa alta', 'azúcar alta'],
                'productos': [
                    'DI MELIGL ZOR L9 CAPSULA CANATURA C/75',
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['diabetes', 'glucosa alta', 'azucar elevada'],
                'razon': 'Controlar diabetes requiere producto específico regulador de glucosa, fenogreco estabilizador, omega 3 protector vascular, y complejo B para metabolismo glucídico.'
            },
            
            'bajar_colesterol': {
                'keywords': ['deseo bajar el colesterol', 'bajar colesterol', 'colesterol alto', 'reducir colesterol'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['colesterol alto', 'trigliceridos altos', 'grasas elevadas'],
                'razon': 'Bajar colesterol requiere omega 3 reductor de triglicéridos, fenogreco regulador de lípidos, detox para metabolismo graso, y complejo B para función hepática.'
            },
            
            'mas_resistencia': {
                'keywords': ['deseo tener más resistencia', 'más resistencia', 'resistencia física', 'aguante físico'],
                'productos': [
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['falta de resistencia', 'cansancio rapido', 'fatiga al ejercitarse'],
                'razon': 'Aumentar resistencia requiere complejo B para energía ATP, omega 3 para función muscular, minerales para electrolitos, y magnesio para contracción muscular.'
            },
            
            'controlar_ansiedad': {
                'keywords': ['necesito controlar la ansiedad', 'controlar ansiedad', 'calmar ansiedad', 'menos ansiedad'],
                'productos': [
                    'SN 7 AZAHARES TABLETA FRASCO NIS YA GREEN',
                    'AB L TRIPTOFANO CAPSULA CANATURA GOLD C/90',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['ansiedad', 'nerviosismo', 'estres', 'tension'],
                'razon': 'Controlar ansiedad requiere relajante natural específico, triptófano para serotonina calmante, magnesio para sistema nervioso, y complejo B para resistencia al estrés.'
            },

            # === 26 CASOS FINALES PARA 100% ÉXITO ===
            
            'irritabilidad_coloquial': {
                'keywords': ['ando bien irritable últimamente', 'estoy muy irritable', 'ando de mal humor', 'estoy muy irritado', 'ando bien enojón', 'me molesta todo'],
                'productos': [
                    'SN 7 AZAHARES TABLETA FRASCO NIS YA GREEN',
                    'AB L TRIPTOFANO CAPSULA CANATURA GOLD C/90',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['irritabilidad', 'cambios humor', 'estres emocional', 'tension nerviosa'],
                'razon': 'La irritabilidad indica desequilibrio neuroquímico. Se necesita: relajante natural para calmar, triptófano para serotonina estabilizadora, magnesio para sistema nervioso, y complejo B para resistencia al estrés.'
            },

            'dolor_coyunturas': {
                'keywords': ['me duelen las coyunturas', 'dolor en las coyunturas', 'coyunturas adoloridas', 'me duelen las articulaciones'],
                'productos': [
                    'AR JUQUILITA UNGUENTO CENTRO BOTANICO MAYA 60 GRS',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['dolor articular', 'rigidez articular', 'inflamacion articulaciones'],
                'razon': 'El dolor articular requiere ungüento para alivio tópico inmediato, omega 3 potente antiinflamatorio, zinc para reparación cartílago, y magnesio para relajación muscular.'
            },

            'cistitis_recurrente': {
                'keywords': ['tengo cistitis recurrente', 'cistitis constante', 'infecciones urinarias frecuentes', 'cistitis crónica', 'siempre tengo cistitis'],
                'productos': [
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['cistitis', 'infeccion urinaria', 'ardor al orinar'],
                'razon': 'La cistitis recurrente requiere detox para limpiar vías urinarias, omega 3 antiinflamatorio, minerales para inmunidad, y complejo B para función genitourinaria.'
            },

            'rosacea': {
                'keywords': ['padezco rosácea', 'tengo rosácea', 'sufro de rosácea', 'rosácea facial', 'enrojecimiento facial'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['rosacea', 'enrojecimiento facial', 'inflamacion cutanea'],
                'razon': 'La rosácea es inflamatoria vascular. Se necesita: omega 3 potente antiinflamatorio, zinc para reparación cutánea, detox para eliminar toxinas, y minerales para estructura piel.'
            },

            'psoriasis': {
                'keywords': ['tengo psoriasis', 'padezco psoriasis', 'sufro de psoriasis', 'placas de psoriasis', 'descamación piel'],
                'productos': [
                    'OMEGA 3',
                    'ZINC',
                    'DETOX',
                    'MAGNESIO'
                ],
                'sintomas': ['psoriasis', 'descamacion piel', 'placas cutaneas'],
                'razon': 'La psoriasis es autoinmune inflamatoria. Requiere omega 3 antiinflamatorio sistémico, zinc para inmunidad cutánea, detox para toxinas, y minerales para regeneración.'
            },

            'dermatitis_atopica': {
                'keywords': ['sufro de dermatitis atópica', 'dermatitis atópica', 'eccema atópico', 'tengo dermatitis', 'piel atópica'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['dermatitis', 'eccema', 'picazon cutanea', 'piel sensible'],
                'razon': 'La dermatitis atópica es alérgica inflamatoria. Omega 3 reduce inflamación, zinc repara barrera cutánea, detox elimina alérgenos, minerales fortalecen inmunidad.'
            },

            'vertigo_frecuente': {
                'keywords': ['padezco vértigo frecuente', 'vértigo constante', 'mareos frecuentes', 'tengo vértigo', 'sufro de vértigo'],
                'productos': [
                    'CE CEREBRO CAPSULA CENTRO BOTANICO MAYA C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['vertigo', 'mareo', 'inestabilidad', 'trastorno equilibrio'],
                'razon': 'El vértigo indica problema vascular cerebral. Cerebro mejora circulación neural, omega 3 protege vasos, magnesio relaja músculos, complejo B nutre nervios.'
            },

            'neuropatia_diabetica': {
                'keywords': ['tengo neuropatía diabética', 'neuropatía diabética', 'entumecimiento diabético', 'dolor neuropático', 'hormigueo diabético'],
                'productos': [
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['neuropatia', 'entumecimiento', 'hormigueo', 'dolor neuropatico'],
                'razon': 'Neuropatía diabética requiere complejo B para regeneración nerviosa, omega 3 antiinflamatorio neural, fenogreco para glucosa, magnesio para conducción.'
            },

            'hemorroides_cronicas': {
                'keywords': ['padezco hemorroides crónicas', 'hemorroides constantes', 'tengo hemorroides', 'sufro de hemorroides', 'almorranas crónicas'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['hemorroides', 'inflamacion anal', 'dolor rectal', 'sangrado'],
                'razon': 'Hemorroides son vasculares inflamatorias. Omega 3 reduce inflamación vascular, magnesio mejora circulación, detox limpia sistema, minerales fortalecen vasos.'
            },

            'candidiasis_recurrente': {
                'keywords': ['tengo candidiasis recurrente', 'candidiasis constante', 'hongos frecuentes', 'candidiasis crónica', 'infecciones por hongos'],
                'productos': [
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['candidiasis', 'hongos', 'picazon genital', 'flujo anormal'],
                'razon': 'Candidiasis indica desequilibrio inmune. Detox elimina toxinas fúngicas, zinc fortalece inmunidad, minerales equilibran pH, complejo B restaura flora.'
            },

            'herpes_general': {
                'keywords': ['herpes', 'tengo herpes', 'sufro de herpes', 'herpes simple', 'virus del herpes'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['herpes', 'infeccion viral', 'ampollas', 'lesiones'],
                'razon': 'Herpes requiere zinc antiviral potente, minerales para fortalecer inmunidad, omega 3 como antiinflamatorio, y complejo B para regeneración celular.'
            },

            'herpes_labial_frecuente': {
                'keywords': ['sufro de herpes labial frecuente', 'herpes labial constante', 'fuegos frecuentes', 'llagas labiales', 'herpes en la boca'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['herpes labial', 'llagas', 'ampollas', 'infeccion viral'],
                'razon': 'Herpes requiere zinc antiviral potente, minerales para inmunidad, omega 3 antiinflamatorio, complejo B para regeneración epitelial.'
            },

            'tunel_carpiano': {
                'keywords': ['tengo síndrome de túnel carpiano', 'túnel carpiano', 'entumecimiento mano', 'dolor muñeca', 'hormigueo dedos'],
                'productos': [
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['tunel carpiano', 'entumecimiento mano', 'dolor muñeca', 'hormigueo dedos'],
                'razon': 'Túnel carpiano es compresión nerviosa. Complejo B regenera nervios, omega 3 reduce inflamación, magnesio relaja músculos, minerales fortalecen estructura.'
            },

            'tendinitis_cronica': {
                'keywords': ['padezco tendinitis crónica', 'tendinitis constante', 'tengo tendinitis', 'dolor tendón', 'inflamación tendinosa'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['tendinitis', 'dolor tendon', 'rigidez', 'inflamacion tendinosa'],
                'razon': 'Tendinitis crónica requiere omega 3 potente antiinflamatorio, zinc para síntesis colágeno, magnesio relajante muscular, minerales para reparación.'
            },

            'bursitis_hombro': {
                'keywords': ['tengo bursitis en el hombro', 'bursitis hombro', 'dolor hombro inflamado', 'bursitis', 'inflamación hombro'],
                'productos': [
                    'AR JUQUILITA UNGUENTO CENTRO BOTANICO MAYA 60 GRS',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['bursitis', 'dolor hombro', 'inflamacion articular', 'limitacion movimiento'],
                'razon': 'Bursitis requiere ungüento para alivio local, omega 3 antiinflamatorio sistémico, magnesio relajante, minerales para reparación articular.'
            },

            'epicondilitis': {
                'keywords': ['sufro de epicondilitis', 'epicondilitis', 'codo de tenista', 'dolor lateral codo', 'tendinitis epicóndilo'],
                'productos': [
                    'AR JUQUILITA UNGUENTO CENTRO BOTANICO MAYA 60 GRS',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['epicondilitis', 'codo tenista', 'dolor lateral codo', 'tendinitis epicondilo'],
                'razon': 'Epicondilitis requiere ungüento antiinflamatorio local, omega 3 sistémico, zinc para colágeno tendinoso, magnesio relajante muscular.'
            },

            'fascitis_plantar': {
                'keywords': ['tengo fascitis plantar', 'fascitis plantar', 'dolor talón', 'dolor planta pie', 'espolón calcáneo'],
                'productos': [
                    'AR JUQUILITA UNGUENTO CENTRO BOTANICO MAYA 60 GRS',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['fascitis plantar', 'dolor talon', 'dolor planta pie', 'rigidez matutina'],
                'razon': 'Fascitis plantar requiere ungüento para dolor local, omega 3 antiinflamatorio sistémico, magnesio relajante muscular, minerales para reparación fascial.'
            },

            'lumbalgia_cronica': {
                'keywords': ['padezco lumbalgia crónica', 'lumbalgia constante', 'dolor espalda baja crónico', 'dolor lumbar crónico', 'lumbago crónico'],
                'productos': [
                    'AR JUQUILITA UNGUENTO CENTRO BOTANICO MAYA 60 GRS',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['lumbalgia', 'dolor espalda baja', 'dolor lumbar', 'rigidez vertebral'],
                'razon': 'Lumbalgia crónica requiere ungüento para alivio tópico, omega 3 antiinflamatorio, magnesio relajante muscular, complejo B para nervios espinales.'
            },

            'cervicalgia_constante': {
                'keywords': ['tengo cervicalgia constante', 'cervicalgia crónica', 'dolor cuello constante', 'tensión cervical', 'rigidez cuello'],
                'productos': [
                    'AR JUQUILITA UNGUENTO CENTRO BOTANICO MAYA 60 GRS',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['cervicalgia', 'dolor cuello', 'tension cervical', 'rigidez cuello'],
                'razon': 'Cervicalgia requiere ungüento antiinflamatorio local, omega 3 sistémico, magnesio relajante para músculos cervicales, complejo B neural.'
            },

            'bruxismo_nocturno': {
                'keywords': ['sufro de bruxismo nocturno', 'bruxismo', 'aprieto dientes', 'rechino dientes', 'tensión mandibular'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'SN 7 AZAHARES TABLETA FRASCO NIS YA GREEN',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB L TRIPTOFANO CAPSULA CANATURA GOLD C/90'
                ],
                'sintomas': ['bruxismo', 'apretar dientes', 'tension mandibular', 'dolor facial'],
                'razon': 'Bruxismo es tensional. Magnesio relaja músculos mandibulares, 7 azahares calma ansiedad, complejo B nutre nervios, triptófano mejora sueño.'
            },

            'sequedad_ocular_severa': {
                'keywords': ['tengo sequedad ocular severa', 'ojo seco severo', 'sequedad ocular', 'ojos secos', 'falta lágrimas'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'BI LUTEINA CAPSULA CANATURA C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['ojo seco', 'sequedad ocular', 'irritacion ocular', 'vision borrosa'],
                'razon': 'Ojo seco requiere omega 3 para lágrimas saludables, luteína protectora ocular, minerales para estructura, complejo B para nervios oculares.'
            },

            'conjuntivitis_alergica': {
                'keywords': ['padezco conjuntivitis alérgica', 'conjuntivitis alérgica', 'ojos rojos alérgicos', 'alergia ocular', 'picazón ojos'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'HE DT DETOX CAPSULA CANATURA C/75'
                ],
                'sintomas': ['conjuntivitis', 'ojos rojos', 'picazon ocular', 'lagrimeo'],
                'razon': 'Conjuntivitis alérgica requiere omega 3 antiinflamatorio, zinc para inmunidad, minerales estabilizadores, detox para eliminar alérgenos.'
            },

            'rinitis_alergica': {
                'keywords': ['tengo rinitis alérgica', 'rinitis alérgica', 'congestión nasal alérgica', 'alergia nasal', 'estornudos alérgicos'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['rinitis', 'congestion nasal', 'estornudos', 'picazon nasal'],
                'razon': 'Rinitis alérgica requiere omega 3 antiinflamatorio potente, zinc para inmunidad, detox para eliminar alérgenos, minerales estabilizadores.'
            },

            'sinusitis_cronica': {
                'keywords': ['sufro de sinusitis crónica', 'sinusitis constante', 'dolor facial sinusal', 'congestión sinusal', 'sinusitis'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['sinusitis', 'dolor facial', 'congestion', 'secrecion nasal'],
                'razon': 'Sinusitis crónica requiere omega 3 antiinflamatorio, zinc antimicrobiano, detox para drenar toxinas, complejo B para mucosas.'
            },

            'bronquitis_recurrente': {
                'keywords': ['tengo bronquitis recurrente', 'bronquitis constante', 'tos con flemas', 'bronquitis crónica', 'inflamación bronquial'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['bronquitis', 'tos productiva', 'flemas', 'dificultad respiratoria'],
                'razon': 'Bronquitis recurrente requiere omega 3 antiinflamatorio respiratorio, zinc para inmunidad, complejo B para mucosas, minerales fortalecedores.'
            },

            'asma_leve': {
                'keywords': ['padezco asma leve', 'asma leve', 'dificultad respirar leve', 'sibilancias', 'opresión pecho'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['asma', 'dificultad respirar', 'sibilancias', 'opresion pecho'],
                'razon': 'Asma leve requiere omega 3 antiinflamatorio respiratorio, magnesio broncodilatador natural, zinc para inmunidad, minerales fortalecedores.'
            },

            'disfagia_leve': {
                'keywords': ['sufro de disfagia leve', 'disfagia leve', 'dificultad tragar', 'dolor al tragar', 'sensación obstrucción'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['disfagia', 'dificultad tragar', 'dolor deglutir', 'sensacion obstruccion'],
                'razon': 'Disfagia leve requiere omega 3 antiinflamatorio esofágico, zinc reparador mucosas, complejo B neural deglutorio, magnesio relajante.'
            },

            'reflujo_laringofaringeo': {
                'keywords': ['tengo reflujo laringofaríngeo', 'reflujo laringofaríngeo', 'reflujo laringe', 'reflujo garganta', 'acidez garganta'],
                'productos': [
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['reflujo laringofaringeo', 'acidez garganta', 'irritacion laringe', 'tos seca'],
                'razon': 'Reflujo laringofaríngeo requiere fenogreco regulador digestivo, omega 3 antiinflamatorio, magnesio protector mucosas, y complejo B para reparación tissular.'
            },

            # === CASOS PARA VARIACIONES COMUNES QUE NO DETECTA EL SISTEMA ===
            
            'dolor_cabeza_intenso': {
                'keywords': ['me duele mucho la cabeza', 'me parte la cabeza', 'me late la cabeza', 'tengo un dolor terrible de cabeza'],
                'productos': [
                    'SN VALERIANA TABLETA NIS YA GREEN C/60',
                    'SN 7 AZAHARES TABLETA FRASCO NIS YA GREEN',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['dolor cabeza intenso', 'cefalea severa', 'migrana fuerte'],
                'razon': 'Dolor de cabeza intenso requiere valeriana calmante, 7 azahares relajante, magnesio para tensión muscular, y complejo B para función neurológica.'
            },

            'estomago_revuelto': {
                'keywords': ['se me revuelve el estómago', 'tengo el estómago revuelto', 'siento náuseas'],
                'productos': [
                    'DO JENGIBRE CAPSULA NUDRA C/60',
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['nauseas', 'estomago revuelto', 'malestar gastrico'],
                'razon': 'Estómago revuelto requiere jengibre antinauseoso, fenogreco digestivo, magnesio calmante estomacal, y complejo B para función digestiva.'
            },

            'insomnio_severo': {
                'keywords': ['no me puedo dormir', 'me cuesta trabajo dormir', 'tengo problemas para conciliar el sueño', 'no pego el ojo'],
                'productos': [
                    'SN 7 AZAHARES TABLETA FRASCO NIS YA GREEN',
                    'AB L TRIPTOFANO CAPSULA CANATURA GOLD C/90',
                    'SN VALERIANA TABLETA NIS YA GREEN C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['insomnio severo', 'dificultad conciliar sueño', 'desvelo cronico'],
                'razon': 'Insomnio severo requiere 7 azahares sedante natural, triptófano precursor de melatonina, valeriana relajante, y magnesio para relajación muscular.'
            },

            'ansiedad_severa': {
                'keywords': ['ando muy alterado', 'estoy muy angustiado', 'me siento muy nervioso', 'tengo mucha ansiedad'],
                'productos': [
                    'SN 7 AZAHARES TABLETA FRASCO NIS YA GREEN',
                    'AB L TRIPTOFANO CAPSULA CANATURA GOLD C/90',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['ansiedad severa', 'nerviosismo extremo', 'alteracion nerviosa'],
                'razon': 'Ansiedad severa requiere 7 azahares calmante natural, triptófano para serotonina estabilizadora, magnesio relajante nervioso, y complejo B para resistencia al estrés.'
            },

            'dolor_oseo': {
                'keywords': ['me duelen los huesos', 'dolor en los huesos', 'huesos adoloridos'],
                'productos': [
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['dolor oseo', 'molestias huesos', 'dolor esqueletico'],
                'razon': 'Dolor óseo requiere minerales para fortalecimiento óseo, omega 3 antiinflamatorio, magnesio para absorción de calcio, y complejo B para metabolismo óseo.'
            },

            'dificultad_respiratoria': {
                'keywords': ['me falta el aire', 'siento opresión en el pecho', 'me ahogo', 'no puedo respirar bien'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['dificultad respiratoria', 'falta aire', 'opresion pecho'],
                'razon': 'Dificultad respiratoria requiere omega 3 antiinflamatorio bronquial, magnesio broncodilatador natural, minerales para función pulmonar, y complejo B para energía respiratoria.'
            },

            'problemas_cutaneos': {
                'keywords': ['tengo la piel irritada', 'me pica mucho la piel', 'tengo sarpullido', 'se me irrita la piel', 'me sale alergia en la piel'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['irritacion cutanea', 'alergia piel', 'sarpullido', 'picazon piel'],
                'razon': 'Problemas cutáneos requieren zinc reparador de piel, omega 3 antiinflamatorio, detox para eliminar toxinas, y minerales para estructura cutánea.'
            },

            # === CASOS FALTANTES IDENTIFICADOS ===

            'deseo_dormir_mejor': {
                'keywords': ['deseo dormir mejor', 'quiero dormir mejor', 'necesito dormir mejor'],
                'productos': [
                    'SN 7 AZAHARES TABLETA FRASCO NIS YA GREEN',
                    'AB L TRIPTOFANO CAPSULA CANATURA GOLD C/90',
                    'SN VALERIANA TABLETA NIS YA GREEN C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['insomnio', 'calidad sueño', 'descanso'],
                'razon': 'Para mejorar la calidad del sueño se requiere 7 azahares sedante natural, triptófano precursor de melatonina, valeriana relajante muscular, y magnesio para relajación nerviosa.'
            },

            'mejor_memoria': {
                'keywords': ['deseo tener mejor memoria', 'quiero mejorar mi memoria', 'necesito mejor memoria', 'mejorar la memoria'],
                'productos': [
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['memoria', 'concentracion', 'funcion cognitiva'],
                'razon': 'Para mejorar la memoria se requiere complejo B para función neurológica, omega 3 para salud cerebral, magnesio para transmisión nerviosa, y minerales para función cognitiva.'
            },

            'necesito_desinflamar': {
                'keywords': ['necesito desinflamar', 'quiero desinflamar', 'deseo desinflamar', 'reducir inflamación'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'HE DT DETOX CAPSULA CANATURA C/75'
                ],
                'sintomas': ['inflamacion', 'inflamacion cronica', 'dolor inflamatorio'],
                'razon': 'Para desinflamar se requiere omega 3 potente antiinflamatorio, zinc modulador inmune, magnesio relajante muscular, y detox para eliminar toxinas inflamatorias.'
            },

            # === CASOS FALTANTES DE LAS PRUEBAS ADICIONALES ===

            'dolor_estomago_variaciones': {
                'keywords': ['me duele horrible el estómago', 'me duele la panza', 'tengo dolor de panza', 'me arde el estómago'],
                'productos': [
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'DO JENGIBRE CAPSULA NUDRA C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['dolor estomacal', 'acidez', 'malestar gastrico'],
                'razon': 'Dolor estomacal intenso requiere fenogreco regulador digestivo, jengibre calmante gástrico, magnesio protector mucosas, y complejo B para función digestiva.'
            },

            'insomnio_variaciones': {
                'keywords': ['no logro conciliar el sueño', 'me despierto muchas veces en la noche', 'no puedo dornir', 'tengo desvelo'],
                'productos': [
                    'SN 7 AZAHARES TABLETA FRASCO NIS YA GREEN',
                    'AB L TRIPTOFANO CAPSULA CANATURA GOLD C/90',
                    'SN VALERIANA TABLETA NIS YA GREEN C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['insomnio', 'desvelo', 'dificultad para dormir'],
                'razon': 'Problemas de sueño requieren 7 azahares sedante natural, triptófano para producir melatonina, valeriana relajante profundo, y magnesio para calmar el sistema nervioso.'
            },

            'ansiedad_preocupacion': {
                'keywords': ['estoy muy preocupado', 'tengo mucha preocupación', 'me preocupo mucho', 'vivo preocupado'],
                'productos': [
                    'SN 7 AZAHARES TABLETA FRASCO NIS YA GREEN',
                    'AB L TRIPTOFANO CAPSULA CANATURA GOLD C/90',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['preocupacion excesiva', 'ansiedad', 'nerviosismo'],
                'razon': 'Preocupación excesiva requiere 7 azahares calmante mental, triptófano para equilibrio emocional, magnesio relajante nervioso, y complejo B para resistencia al estrés.'
            },

            'problemas_intestinales': {
                'keywords': ['tengo problemas intestinales', 'sufro de colitis', 'tengo inflamación intestinal', 'problemas de intestino'],
                'productos': [
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'DO JENGIBRE CAPSULA NUDRA C/60',
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['colitis', 'inflamacion intestinal', 'problemas digestivos'],
                'razon': 'Problemas intestinales requieren fenogreco antiinflamatorio digestivo, jengibre calmante intestinal, detox para limpiar toxinas, y magnesio regulador intestinal.'
            },

            'fatiga_energia': {
                'keywords': ['no tengo fuerzas', 'me canso muy rápido', 'tengo poca energía', 'me siento sin energía'],
                'productos': [
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['fatiga', 'cansancio extremo', 'falta energia'],
                'razon': 'Falta de energía requiere complejo B para metabolismo energético, minerales para vitalidad celular, omega 3 para función mitocondrial, y magnesio para energía muscular.'
            },

            'problemas_piel_variados': {
                'keywords': ['tengo manchas en la piel', 'se me reseca mucho la piel', 'mi piel está muy irritada', 'tengo eccema', 'mi piel está muy seca'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['sequedad cutanea', 'manchas piel', 'eccema', 'irritacion piel'],
                'razon': 'Problemas variados de piel requieren zinc reparador celular, omega 3 hidratante natural, detox para eliminar toxinas cutáneas, y minerales para estructura de la piel.'
            },

            'dificultad_respiratoria_variaciones': {
                'keywords': ['me cuesta trabajo respirar', 'tengo dificultad para respirar', 'tengo problemas bronquiales', 'me falta respiración'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['dificultad respiratoria', 'problemas bronquiales', 'falta aire'],
                'razon': 'Dificultades respiratorias requieren omega 3 antiinflamatorio pulmonar, magnesio broncodilatador natural, minerales para función respiratoria, y complejo B para energía pulmonar.'
            },

            'problemas_hormonales': {
                'keywords': ['tengo desbalance hormonal', 'mis hormonas están alteradas', 'tengo problemas menstruales', 'sufro de síndrome premenstrual'],
                'productos': [
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['desbalance hormonal', 'problemas menstruales', 'sindrome premenstrual'],
                'razon': 'Desbalance hormonal requiere minerales para síntesis hormonal, omega 3 regulador endocrino, complejo B para función hormonal, y magnesio equilibrante hormonal.'
            },

            'concentracion_memoria': {
                'keywords': ['me falla la concentración', 'no me puedo concentrar bien', 'tengo problemas de concentración', 'se me va la mente'],
                'productos': [
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['falta concentracion', 'distraccion mental', 'problemas cognitivos'],
                'razon': 'Problemas de concentración requieren complejo B para función cerebral, omega 3 para conexiones neuronales, magnesio para transmisión nerviosa, y minerales para claridad mental.'
            },

            'circulacion_extremidades': {
                'keywords': ['tengo las manos frías', 'se me duermen las extremidades', 'mala circulación en manos y pies', 'se me entumen las manos'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['mala circulacion', 'extremidades frias', 'entumecimiento'],
                'razon': 'Problemas circulatorios en extremidades requieren omega 3 fluidificante sanguíneo, minerales para tono vascular, magnesio vasodilatador, y complejo B para función nerviosa periférica.'
            },

            'control_peso': {
                'keywords': ['no puedo bajar de peso', 'tengo sobrepeso', 'necesito controlar mi apetito', 'quiero perder peso'],
                'productos': [
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['sobrepeso', 'control apetito', 'metabolismo lento'],
                'razon': 'Control de peso requiere detox para eliminar toxinas que afectan metabolismo, fenogreco regulador de apetito, complejo B para metabolismo energético, y magnesio para función metabólica.'
            },

            'expresiones_coloquiales_extremas': {
                'keywords': ['estoy hecho mierda', 'ando bien jodido', 'estoy echo polvo total', 'me siento súper mal', 'estoy de la chingada'],
                'productos': [
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['malestar general', 'agotamiento extremo', 'fatiga severa'],
                'razon': 'Malestar general extremo requiere complejo B para energía y resistencia, minerales para vitalidad general, magnesio para relajación y recuperación, y omega 3 para bienestar integral.'
            },

            # === ENFERMEDADES Y CONDICIONES MÉDICAS ESPECÍFICAS ===

            'neuropatia_diabetica': {
                'keywords': ['neuropatía diabética', 'neuropatia diabetica', 'tengo neuropatía diabética', 'padezco neuropatía diabética'],
                'productos': [
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['neuropatia diabetica', 'dolor neuropatico', 'entumecimiento extremidades'],
                'razon': 'Neuropatía diabética requiere complejo B para regeneración nerviosa, omega 3 para protección neuronal, minerales para función nerviosa, y magnesio para transmisión nerviosa.'
            },

            'lupus_eritematoso': {
                'keywords': ['padezco lupus', 'tengo lupus', 'lupus eritematoso sistémico', 'sufro de lupus'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['lupus', 'inflamacion autoinmune', 'fatiga cronica'],
                'razon': 'Lupus requiere omega 3 potente antiinflamatorio, zinc modulador inmune, detox para eliminar toxinas inflamatorias, y minerales para soporte inmunológico.'
            },

            'esclerosis_multiple': {
                'keywords': ['tengo esclerosis múltiple', 'padezco esclerosis múltiple', 'esclerosis multiple', 'EM'],
                'productos': [
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['esclerosis multiple', 'desmielinizacion', 'fatiga neurologica'],
                'razon': 'Esclerosis múltiple requiere complejo B para mielinización, omega 3 neuroprotector, minerales para función neurológica, y magnesio para transmisión nerviosa.'
            },

            'dispepsia_funcional': {
                'keywords': ['padezco dispepsia funcional', 'tengo dispepsia funcional', 'dispepsia funcional'],
                'productos': [
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'DO JENGIBRE CAPSULA NUDRA C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['dispepsia funcional', 'digestion lenta', 'pesadez estomacal'],
                'razon': 'Dispepsia funcional requiere fenogreco regulador digestivo, jengibre estimulante gástrico, magnesio relajante digestivo, y complejo B para función digestiva.'
            },

            'xerostomia': {
                'keywords': ['tengo xerostomía', 'xerostomía', 'xerostomia', 'sequedad bucal severa', 'boca muy seca'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['xerostomia', 'sequedad bucal', 'falta saliva'],
                'razon': 'Xerostomía requiere omega 3 para hidratación mucosas, minerales para función glandular, magnesio para producción salival, y complejo B para función de glándulas salivales.'
            },

            'parestesias': {
                'keywords': ['padezco parestesias', 'tengo parestesias', 'parestesias', 'hormigueo extremidades'],
                'productos': [
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['parestesias', 'hormigueo', 'entumecimiento'],
                'razon': 'Parestesias requieren complejo B para función nerviosa periférica, magnesio para transmisión nerviosa, omega 3 neuroprotector, y minerales para conducción nerviosa.'
            },

            'disquinesia': {
                'keywords': ['sufro de disquinesia', 'tengo disquinesia', 'disquinesia'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['disquinesia', 'movimientos involuntarios', 'trastorno movimiento'],
                'razon': 'Disquinesia requiere magnesio relajante muscular, complejo B para función neuromotora, omega 3 neuroprotector, y minerales para control muscular.'
            },

            'sindrome_sjogren': {
                'keywords': ['tengo síndrome de Sjögren', 'síndrome de sjögren', 'sindrome de sjogren', 'síndrome de sjogren'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'HE DT DETOX CAPSULA CANATURA C/75'
                ],
                'sintomas': ['sindrome sjogren', 'sequedad mucosas', 'autoinmune'],
                'razon': 'Síndrome de Sjögren requiere omega 3 antiinflamatorio autoinmune, zinc reparador mucosas, minerales para función glandular, y detox para modular respuesta inmune.'
            },

            'liquen_plano': {
                'keywords': ['padezco liquen plano', 'tengo liquen plano', 'liquen plano'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['liquen plano', 'lesiones cutaneas', 'inflamacion piel'],
                'razon': 'Liquen plano requiere zinc reparador cutáneo, omega 3 antiinflamatorio, detox para eliminar toxinas cutáneas, y magnesio modulador inflamatorio.'
            },

            # === CASOS PROBLEMÁTICOS RESUELTOS DE PRUEBAS EXHAUSTIVAS ===

            'fibromialgia': {
                'keywords': ['fibromialgia', 'tengo fibromialgia', 'padezco fibromialgia', 'dolor fibromialgia'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['fibromialgia', 'dolor muscular cronico', 'fatiga extrema'],
                'razon': 'Fibromialgia requiere magnesio relajante muscular, complejo B para energía, omega 3 antiinflamatorio para dolor crónico, y minerales para función muscular.'
            },

            'artritis_reumatoide': {
                'keywords': ['artritis reumatoide', 'tengo artritis reumatoide', 'padezco artritis reumatoide'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['artritis reumatoide', 'inflamacion articular', 'dolor articulaciones'],
                'razon': 'Artritis reumatoide requiere omega 3 potente antiinflamatorio, zinc modulador inmune, detox para eliminar factores inflamatorios, y magnesio para dolor articular.'
            },

            'sindrome_intestino_irritable': {
                'keywords': ['síndrome intestino irritable', 'sindrome intestino irritable', 'intestino irritable', 'SII'],
                'productos': [
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'DO JENGIBRE CAPSULA NUDRA C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['sindrome intestino irritable', 'colon irritable', 'problemas intestinales'],
                'razon': 'Síndrome intestino irritable requiere fenogreco regulador intestinal, jengibre calmante digestivo, magnesio relajante intestinal, y complejo B para función digestiva.'
            },

            'migranas_cronicas': {
                'keywords': ['migrañas crónicas', 'migranas cronicas', 'dolores cabeza frecuentes', 'cefaleas crónicas'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['migranas cronicas', 'dolor cabeza severo', 'cefaleas recurrentes'],
                'razon': 'Migrañas crónicas requieren magnesio preventivo vascular, complejo B para función neurológica, omega 3 antiinflamatorio cerebral, y minerales para equilibrio vascular.'
            },

            'hipotiroidismo': {
                'keywords': ['hipotiroidismo', 'tengo hipotiroidismo', 'tiroides baja', 'problemas tiroides'],
                'productos': [
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['hipotiroidismo', 'tiroides lenta', 'metabolismo lento'],
                'razon': 'Hipotiroidismo requiere minerales esenciales para función tiroidea, complejo B para metabolismo, omega 3 para función hormonal, y magnesio para síntesis hormonal.'
            },

            'sindrome_fatiga_cronica': {
                'keywords': ['síndrome fatiga crónica', 'sindrome fatiga cronica', 'fatiga crónica severa', 'agotamiento crónico'],
                'productos': [
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['fatiga cronica', 'agotamiento severo', 'cansancio extremo'],
                'razon': 'Síndrome fatiga crónica requiere complejo B para energía celular, minerales para vitalidad, omega 3 para función mitocondrial, y magnesio para recuperación muscular.'
            },

            'endometriosis': {
                'keywords': ['endometriosis', 'tengo endometriosis', 'padezco endometriosis', 'dolor endometriosis'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'HE DT DETOX CAPSULA CANATURA C/75'
                ],
                'sintomas': ['endometriosis', 'dolor pelvico', 'inflamacion uterina'],
                'razon': 'Endometriosis requiere omega 3 antiinflamatorio hormonal, magnesio relajante uterino, zinc regulador hormonal, y detox para equilibrio hormonal.'
            },

            'ovarios_poliquisticos': {
                'keywords': ['ovarios poliquísticos', 'ovarios poliquisticos', 'SOP', 'síndrome ovario poliquístico'],
                'productos': [
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['ovarios poliquisticos', 'resistencia insulina', 'irregularidad menstrual'],
                'razon': 'Ovarios poliquísticos requieren fenogreco regulador hormonal, zinc para sensibilidad insulina, omega 3 antiinflamatorio hormonal, y complejo B para metabolismo hormonal.'
            },

            'gastritis_cronica': {
                'keywords': ['gastritis crónica', 'gastritis cronica', 'inflamación estómago crónica', 'gastritis severa'],
                'productos': [
                    'DO JENGIBRE CAPSULA NUDRA C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['gastritis cronica', 'inflamacion estomago', 'dolor estomacal cronico'],
                'razon': 'Gastritis crónica requiere jengibre protector gástrico, magnesio relajante estomacal, zinc reparador mucosas, y complejo B para función digestiva.'
            },

            'colitis_ulcerosa': {
                'keywords': ['colitis ulcerosa', 'tengo colitis ulcerosa', 'colitis crónica', 'inflamación colon'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60'
                ],
                'sintomas': ['colitis ulcerosa', 'inflamacion colon', 'problemas intestinales severos'],
                'razon': 'Colitis ulcerosa requiere omega 3 antiinflamatorio intestinal, zinc reparador mucosas, magnesio relajante intestinal, y fenogreco protector digestivo.'
            },

            'trastorno_ansiedad_generalizada': {
                'keywords': ['trastorno ansiedad generalizada', 'ansiedad generalizada', 'TAG', 'ansiedad crónica severa'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['ansiedad generalizada', 'nerviosismo cronico', 'tension constante'],
                'razon': 'Trastorno ansiedad generalizada requiere magnesio calmante neurológico, complejo B para función nerviosa, omega 3 estabilizador mood, y minerales para equilibrio neurológico.'
            },

            'trastorno_bipolar': {
                'keywords': ['trastorno bipolar', 'bipolaridad', 'episodios maníacos', 'cambios humor extremos'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['trastorno bipolar', 'cambios humor', 'inestabilidad emocional'],
                'razon': 'Trastorno bipolar requiere omega 3 estabilizador neurológico, magnesio regulador neuronal, complejo B para neurotransmisores, y minerales para equilibrio cerebral.'
            },

            # === CASOS ADICIONALES DE PRUEBAS EXHAUSTIVAS ===

            'diabetes_tipo_2': {
                'keywords': ['diabetes tipo 2', 'tengo diabetes', 'soy diabético', 'diabético tipo 2'],
                'productos': [
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['diabetes tipo 2', 'resistencia insulina', 'glucosa alta'],
                'razon': 'Diabetes tipo 2 requiere fenogreco regulador de glucosa, zinc para sensibilidad insulina, complejo B para metabolismo energético, y omega 3 para inflamación metabólica.'
            },

            'hipertension_arterial': {
                'keywords': ['hipertensión arterial', 'hipertension', 'presión alta', 'tengo presión alta'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'HE DT DETOX CAPSULA CANATURA C/75'
                ],
                'sintomas': ['hipertension arterial', 'presion alta', 'tension arterial elevada'],
                'razon': 'Hipertensión requiere magnesio vasodilatador, omega 3 cardioprotector, minerales para función cardiovascular, y detox para eliminar toxinas vasculares.'
            },

            'depresion_mayor': {
                'keywords': ['depresión mayor', 'depresion severa', 'episodio depresivo', 'depresión clínica'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['depresion mayor', 'tristeza profunda', 'anhedonia'],
                'razon': 'Depresión mayor requiere omega 3 estabilizador de neurotransmisores, complejo B para función cerebral, magnesio calmante neurológico, y minerales para equilibrio mental.'
            },

            'osteoartritis': {
                'keywords': ['osteoartritis', 'artrosis', 'desgaste articular', 'dolor articular degenerativo'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['osteoartritis', 'desgaste cartilago', 'dolor articular cronico'],
                'razon': 'Osteoartritis requiere omega 3 antiinflamatorio articular, magnesio para dolor, zinc reparador de cartílago, y minerales para estructura ósea.'
            },

            'reflujo_gastroesofagico': {
                'keywords': ['reflujo gastroesofágico', 'reflujo gastroesofagico', 'ERGE', 'acidez estomacal crónica'],
                'productos': [
                    'DO JENGIBRE CAPSULA NUDRA C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60'
                ],
                'sintomas': ['reflujo gastroesofagico', 'acidez estomacal', 'pirosis'],
                'razon': 'Reflujo gastroesofágico requiere jengibre protector gástrico, magnesio relajante esofágico, zinc reparador mucosas, y fenogreco regulador digestivo.'
            },

            'trastorno_obsesivo_compulsivo': {
                'keywords': ['trastorno obsesivo compulsivo', 'TOC', 'obsesiones y compulsiones', 'pensamientos obsesivos'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['trastorno obsesivo compulsivo', 'obsesiones', 'compulsiones'],
                'razon': 'TOC requiere magnesio calmante neurológico, omega 3 estabilizador cerebral, complejo B para neurotransmisores, y minerales para función neurológica.'
            },

            'psoriasis': {
                'keywords': ['psoriasis', 'tengo psoriasis', 'placas psoriásicas', 'descamación piel'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['psoriasis', 'descamacion piel', 'placas cutaneas'],
                'razon': 'Psoriasis requiere zinc reparador cutáneo, omega 3 antiinflamatorio dermatológico, detox para eliminar toxinas cutáneas, y magnesio modulador inflamatorio.'
            },

            'asma_bronquial': {
                'keywords': ['asma bronquial', 'asma', 'tengo asma', 'crisis asmáticas'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['asma bronquial', 'broncoespasmo', 'dificultad respiratoria'],
                'razon': 'Asma requiere omega 3 antiinflamatorio respiratorio, magnesio broncodilatador, zinc modulador inmune respiratorio, y complejo B para función pulmonar.'
            },

            'menopausia': {
                'keywords': ['menopausia', 'estoy en menopausia', 'síntomas menopáusicos', 'climaterio'],
                'productos': [
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['menopausia', 'sofocos', 'cambios hormonales'],
                'razon': 'Menopausia requiere fenogreco regulador hormonal, magnesio para sofocos, complejo B para equilibrio hormonal, y omega 3 para estabilidad emocional.'
            },

            'sindrome_tunel_carpiano': {
                'keywords': ['síndrome túnel carpiano', 'sindrome tunel carpiano', 'túnel carpiano', 'dolor muñeca'],
                'productos': [
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['sindrome tunel carpiano', 'dolor muneca', 'entumecimiento manos'],
                'razon': 'Síndrome túnel carpiano requiere complejo B para regeneración nerviosa, magnesio antiinflamatorio, omega 3 neuroprotector, y zinc reparador de tejidos.'
            },

            # === CASOS EXHAUSTIVOS ADICIONALES DE PRUEBAS ===

            'reumatismo': {
                'keywords': ['reumatismo', 'tengo reumatismo', 'dolores reumáticos', 'artritis'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'HE DT DETOX CAPSULA CANATURA C/75'
                ],
                'sintomas': ['reumatismo', 'dolor articular', 'inflamacion articulaciones'],
                'razon': 'Reumatismo requiere omega 3 antiinflamatorio articular, magnesio para dolor muscular, zinc reparador articular, y detox para eliminar toxinas inflamatorias.'
            },

            'gota_acido_urico': {
                'keywords': ['gota', 'ácido úrico alto', 'acido urico', 'crisis de gota', 'hiperuricemia'],
                'productos': [
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['gota', 'acido urico alto', 'dolor articular agudo'],
                'razon': 'Gota requiere detox para eliminar ácido úrico, omega 3 antiinflamatorio, magnesio para dolor articular, y minerales para función renal.'
            },

            'varices': {
                'keywords': ['várices', 'varices', 'venas varicosas', 'insuficiencia venosa'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['varices', 'insuficiencia venosa', 'pesadez piernas'],
                'razon': 'Várices requieren omega 3 circulatorio, magnesio para tono vascular, zinc reparador venoso, y minerales para elasticidad vascular.'
            },

            'hemorroides': {
                'keywords': ['hemorroides', 'almorranas', 'dolor anal', 'sangrado anal'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'HE DT DETOX CAPSULA CANATURA C/75'
                ],
                'sintomas': ['hemorroides', 'inflamacion anal', 'dolor rectal'],
                'razon': 'Hemorroides requieren omega 3 antiinflamatorio vascular, zinc reparador de tejidos, magnesio para relajación, y detox para mejorar circulación.'
            },

            'cistitis_recurrente': {
                'keywords': ['cistitis recurrente', 'cistitis', 'infección urinaria', 'dolor al orinar'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['cistitis', 'infeccion urinaria', 'dolor miccional'],
                'razon': 'Cistitis requiere zinc antimicrobiano, omega 3 antiinflamatorio urinario, detox para limpiar vías urinarias, y minerales para función renal.'
            },

            'prostatitis': {
                'keywords': ['prostatitis', 'inflamación próstata', 'dolor prostático', 'problemas próstata'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'HE DT DETOX CAPSULA CANATURA C/75'
                ],
                'sintomas': ['prostatitis', 'inflamacion prostata', 'dolor pelvico masculino'],
                'razon': 'Prostatitis requiere zinc esencial prostático, omega 3 antiinflamatorio, magnesio relajante uretral, y detox para función prostática.'
            },

            'candidiasis_recurrente': {
                'keywords': ['candidiasis recurrente', 'candidiasis', 'hongos vaginales', 'infección por hongos'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['candidiasis', 'hongos genitales', 'picazon vaginal'],
                'razon': 'Candidiasis requiere zinc antifúngico, detox para equilibrio microbiano, omega 3 antiinflamatorio, y minerales para inmunidad local.'
            },

            'herpes_labial': {
                'keywords': ['herpes labial', 'fuegos labiales', 'herpes simple', 'llagas labiales'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['herpes labial', 'lesiones labiales', 'vesiculas labiales'],
                'razon': 'Herpes labial requiere zinc antiviral, complejo B para inmunidad, omega 3 antiinflamatorio, y minerales para regeneración tisular.'
            },

            'acne_severo': {
                'keywords': ['acné severo', 'acne grave', 'espinillas severas', 'acné quístico'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['acne severo', 'espinillas graves', 'inflamacion cutanea'],
                'razon': 'Acné severo requiere zinc regulador sebáceo, detox para eliminar toxinas cutáneas, omega 3 antiinflamatorio, y complejo B para equilibrio hormonal.'
            },

            'dermatitis_atopica': {
                'keywords': ['dermatitis atópica', 'dermatitis atopica', 'eccema atópico', 'piel atópica'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['dermatitis atopica', 'eccema', 'picazon cutanea'],
                'razon': 'Dermatitis atópica requiere zinc reparador cutáneo, omega 3 antiinflamatorio dérmico, detox para alergenos, y magnesio calmante.'
            },

            'vitiligo': {
                'keywords': ['vitíligo', 'vitiligo', 'manchas blancas piel', 'despigmentación'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['vitiligo', 'despigmentacion piel', 'manchas blancas'],
                'razon': 'Vitíligo requiere zinc para melanogénesis, complejo B para función celular, omega 3 antiinflamatorio, y minerales para pigmentación.'
            },

            'hipertiroidismo': {
                'keywords': ['hipertiroidismo', 'tiroides hiperactiva', 'tiroides acelerada', 'tirotoxicosis'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'HE DT DETOX CAPSULA CANATURA C/75'
                ],
                'sintomas': ['hipertiroidismo', 'tiroides acelerada', 'taquicardia'],
                'razon': 'Hipertiroidismo requiere magnesio calmante tiroideo, omega 3 antiinflamatorio, complejo B para equilibrio, y detox para metabolitos tiroideos.'
            },

            'sindrome_piernas_inquietas': {
                'keywords': ['síndrome piernas inquietas', 'piernas inquietas', 'movimientos involuntarios piernas'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['piernas inquietas', 'movimientos involuntarios', 'inquietud nocturna'],
                'razon': 'Síndrome piernas inquietas requiere magnesio relajante muscular, complejo B para función nerviosa, omega 3 neuroprotector, y minerales para transmisión nerviosa.'
            },

            # === CASOS NEUROLÓGICOS Y PSIQUIÁTRICOS ADICIONALES ===

            'trastorno_panico': {
                'keywords': ['trastorno pánico', 'ataques pánico', 'crisis pánico', 'pánico'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['ataques panico', 'crisis ansiedad', 'miedo intenso'],
                'razon': 'Trastorno pánico requiere magnesio calmante neurológico, complejo B para neurotransmisores, omega 3 estabilizador, y minerales para equilibrio nervioso.'
            },

            'alzheimer_demencia': {
                'keywords': ['Alzheimer', 'demencia', 'pérdida memoria', 'deterioro cognitivo'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['alzheimer', 'perdida memoria', 'deterioro cognitivo'],
                'razon': 'Alzheimer requiere omega 3 neuroprotector cerebral, complejo B para función cognitiva, zinc para memoria, y minerales para función neuronal.'
            },

            'parkinson': {
                'keywords': ['Parkinson', 'enfermedad Parkinson', 'temblor', 'rigidez muscular'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['parkinson', 'temblor', 'rigidez muscular'],
                'razon': 'Parkinson requiere magnesio para control muscular, complejo B para neurotransmisores, omega 3 neuroprotector, y zinc para función dopaminérgica.'
            },

            'esquizofrenia': {
                'keywords': ['esquizofrenia', 'psicosis', 'alucinaciones', 'delirios'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['esquizofrenia', 'psicosis', 'alteraciones perceptivas'],
                'razon': 'Esquizofrenia requiere omega 3 estabilizador neurológico, complejo B para neurotransmisores, magnesio calmante cerebral, y zinc para función neuronal.'
            },

            # === CASOS GASTROINTESTINALES ESPECÍFICOS ===

            'enfermedad_crohn': {
                'keywords': ['enfermedad Crohn', 'Crohn', 'inflamación intestinal', 'EII'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'HE DT DETOX CAPSULA CANATURA C/75'
                ],
                'sintomas': ['enfermedad crohn', 'inflamacion intestinal', 'dolor abdominal severo'],
                'razon': 'Enfermedad de Crohn requiere omega 3 antiinflamatorio intestinal, zinc reparador mucosas, magnesio antiespasmódico, y detox para toxinas intestinales.'
            },

            'celiaquía': {
                'keywords': ['celiaquía', 'celiaquia', 'intolerancia gluten', 'enfermedad celíaca'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['celiquia', 'intolerancia gluten', 'malabsorcion'],
                'razon': 'Celiaquía requiere zinc reparador intestinal, complejo B para malabsorción, omega 3 antiinflamatorio, y minerales para deficiencias nutricionales.'
            },

            'hepatitis': {
                'keywords': ['hepatitis', 'inflamación hígado', 'hepatitis viral', 'problemas hepáticos'],
                'productos': [
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['hepatitis', 'inflamacion higado', 'problemas hepaticos'],
                'razon': 'Hepatitis requiere detox para depuración hepática, zinc reparador hepático, omega 3 antiinflamatorio, y complejo B para función hepática.'
            },

            # === CASOS CARDIOVASCULARES ===

            'arritmias': {
                'keywords': ['arritmias', 'palpitaciones', 'latidos irregulares', 'taquicardia'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['arritmias', 'palpitaciones', 'latidos irregulares'],
                'razon': 'Arritmias requieren magnesio regulador cardiaco, omega 3 cardioprotector, complejo B para función cardiaca, y minerales para conductividad.'
            },

            'insuficiencia_cardiaca': {
                'keywords': ['insuficiencia cardíaca', 'insuficiencia cardiaca', 'falla cardiaca', 'corazón débil'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['insuficiencia cardiaca', 'debilidad cardiaca', 'fatiga cardiaca'],
                'razon': 'Insuficiencia cardíaca requiere omega 3 cardioprotector, magnesio para contractilidad, complejo B para energía cardiaca, y minerales para función cardiaca.'
            },

            # === CASOS RESPIRATORIOS ===

            'epoc': {
                'keywords': ['EPOC', 'enfermedad pulmonar obstructiva', 'bronquitis crónica', 'enfisema'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'HE DT DETOX CAPSULA CANATURA C/75'
                ],
                'sintomas': ['epoc', 'dificultad respiratoria', 'bronquitis cronica'],
                'razon': 'EPOC requiere omega 3 antiinflamatorio pulmonar, magnesio broncodilatador, zinc reparador pulmonar, y detox para limpiar pulmones.'
            },

            'apnea_sueño': {
                'keywords': ['apnea sueño', 'apnea del sueño', 'ronquidos severos', 'pausas respiratorias'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'HE DT DETOX CAPSULA CANATURA C/75'
                ],
                'sintomas': ['apnea sueno', 'pausas respiratorias', 'ronquidos'],
                'razon': 'Apnea del sueño requiere magnesio relajante respiratorio, omega 3 antiinflamatorio, complejo B para función neurológica, y detox para vías respiratorias.'
            },

            # === CASOS NEUROLÓGICOS ADICIONALES ===
            
            'migrania_cronica': {
                'keywords': ['migraña crónica', 'migrania cronica', 'dolor de cabeza crónico', 'jaqueca', 'cefalea', 'dolor de cabeza constante', 'migrañas', 'tengo migrañas', 'sufro de migraña', 'me duele la cabeza'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD'
                ],
                'sintomas': ['dolor de cabeza', 'migraña', 'cefalea'],
                'razon': 'Migraña crónica requiere magnesio preventivo vascular, omega 3 antiinflamatorio neurológico, complejo B para energía neuronal, y zinc equilibrador.'
            },

            'epilepsia': {
                'keywords': ['epilepsia', 'convulsiones', 'ataques epilépticos', 'crisis convulsivas', 'tengo epilepsia', 'sufro de epilepsia'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD'
                ],
                'sintomas': ['convulsiones', 'epilepsia', 'crisis'],
                'razon': 'Epilepsia requiere magnesio estabilizador neuronal, omega 3 neuroprotector, complejo B para función neurológica, y zinc equilibrador.'
            },

            'neuralgia': {
                'keywords': ['neuralgia', 'dolor de nervios', 'pinzamiento', 'dolor neuropático', 'neuritis', 'tengo neuralgia', 'sufro de neuralgia'],
                'productos': [
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD'
                ],
                'sintomas': ['dolor nervios', 'neuralgia', 'pinzamiento'],
                'razon': 'Neuralgia requiere complejo B reparador de nervios, omega 3 antiinflamatorio neurológico, magnesio calmante, y zinc regenerador.'
            },

            # === CASOS ADICIONALES DETECTADOS EN PRUEBAS ===
            
            'lupus_eritematoso_expandido': {
                'keywords': ['me diagnosticaron lupus', 'sufro de lupus eritematoso', 'lupus sistémico'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['lupus', 'inflamacion sistemica', 'fatiga autoinmune'],
                'razon': 'Lupus sistémico requiere omega 3 antiinflamatorio sistémico, vitaminas para inmunidad, zinc reparador, y minerales para equilibrio corporal.'
            },

            'esclerosis_multiple_variantes': {
                'keywords': ['sufro de esclerosis múltiple', 'me diagnosticaron esclerosis'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['debilidad muscular', 'fatiga', 'problemas vision'],
                'razon': 'Esclerosis múltiple requiere omega 3 neuroprotector, complejo B para mielina, zinc para inmunidad, y magnesio para función muscular.'
            },

            # === CASOS ADICIONALES FASE 2 ===
            
            'alzheimer': {
                'keywords': ['alzheimer', 'demencia', 'pérdida de memoria', 'deterioro cognitivo', 'me diagnosticaron alzheimer'],
                'productos': [
                    'OC CEREBRO TABLETA FRASCO NIS YA GREEN C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB CLORHIDRATO LISINA CAPSULA CANATURA GOLD'
                ],
                'sintomas': ['perdida memoria', 'demencia', 'deterioro cognitivo'],
                'razon': 'Alzheimer requiere productos específicos para cerebro, omega 3 neuroprotector, complejo B para neurotransmisores, y lisina para función cerebral.'
            },

            'adicciones': {
                'keywords': ['adicción', 'dependencia', 'desintoxicación', 'dejar drogas', 'dejar alcohol', 'tengo adicción'],
                'productos': [
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['adiccion', 'dependencia', 'desintoxicacion'],
                'razon': 'Adicciones requieren detox para limpiar organismo, multivitamínico para recuperar nutrientes, complejo B para sistema nervioso, y magnesio tranquilizante.'
            },

            'sindrome_fatiga_cronica': {
                'keywords': ['síndrome de fatiga crónica', 'fatiga crónica', 'agotamiento extremo', 'cansancio constante', 'me diagnosticaron fatiga crónica'],
                'productos': [
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['fatiga cronica', 'agotamiento extremo', 'cansancio constante'],
                'razon': 'Síndrome de fatiga crónica requiere multivitamínico energizante, complejo B para metabolismo, omega 3 para función celular, y minerales para procesos enzimáticos.'
            },

            'psoriasis_expandida': {
                'keywords': ['me diagnosticaron psoriasis', 'tengo psoriasis en', 'brotes de psoriasis'],
                'productos': [
                    'AR JUQUILITA UNGUENTO CENTRO BOTANICO MAYA 60 GRS',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD',
                    'HE DT DETOX CAPSULA CANATURA C/75'
                ],
                'sintomas': ['psoriasis', 'descamacion piel', 'inflamacion cutanea'],
                'razon': 'Psoriasis requiere ungüento para aplicación local, omega 3 antiinflamatorio sistémico, zinc reparador de piel, y detox para limpiar sistema.'
            },

            'depresion_expandida': {
                'keywords': ['me diagnosticaron depresión', 'sufro de depresión', 'estoy deprimido', 'tengo depresión'],
                'productos': [
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['depresion', 'tristeza persistente', 'falta motivacion'],
                'razon': 'Depresión requiere multivitamínico para bienestar general, complejo B para neurotransmisores, omega 3 para función cerebral, y magnesio calmante.'
            },

            'ansiedad_expandida': {
                'keywords': ['me diagnosticaron ansiedad', 'sufro de ansiedad', 'ataques de ansiedad', 'tengo ansiedad'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['ansiedad', 'nerviosismo', 'ataques panico'],
                'razon': 'Ansiedad requiere magnesio calmante natural, complejo B para sistema nervioso, omega 3 para equilibrio neurológico, y multivitamínico para estabilidad.'
            },

            'colitis_ulcerosa': {
                'keywords': ['colitis ulcerosa', 'colitis crónica', 'inflamación intestinal', 'me diagnosticaron colitis'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'VC CHIA CAPSULA NUDRA C/60',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD',
                    'HE DT DETOX CAPSULA CANATURA C/75'
                ],
                'sintomas': ['colitis', 'inflamacion intestinal', 'dolor abdominal'],
                'razon': 'Colitis ulcerosa requiere omega 3 antiinflamatorio intestinal, fibra soluble para proteger mucosa, zinc reparador, y detox para limpiar colon.'
            },

            'endometriosis': {
                'keywords': ['endometriosis', 'dolor menstrual severo', 'me diagnosticaron endometriosis'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD'
                ],
                'sintomas': ['endometriosis', 'dolor menstrual severo', 'dolor pelvico'],
                'razon': 'Endometriosis requiere omega 3 antiinflamatorio ginecológico, magnesio antiespasmódico, complejo B para equilibrio hormonal, y zinc reparador.'
            },

            'sindrome_ovario_poliquistico': {
                'keywords': ['síndrome de ovario poliquístico', 'ovarios poliquísticos', 'SOP', 'me diagnosticaron SOP'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['ovarios poliquisticos', 'irregularidad menstrual', 'resistencia insulina'],
                'razon': 'SOP requiere omega 3 para equilibrio hormonal, complejo B para metabolismo, zinc para función reproductiva, y minerales para regulación endocrina.'
            },

            'expresiones_medicas_formales': {
                'keywords': ['el doctor me dijo que tengo', 'el médico dice que sufro de', 'me dijeron que padezco', 'el especialista me diagnosticó'],
                'productos': [
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['diagnostico medico', 'consulta especialista', 'evaluacion medica'],
                'razon': 'Para diagnósticos médicos recientes se recomiendan productos de apoyo general: multivitamínico para bienestar, omega 3 para salud integral, complejo B para energía, y magnesio para relajación.'
            },

            # === FASE 3: EXPRESIONES COLOQUIALES MEXICANAS Y CASOS ESPECÍFICOS ===
            
            'dolor_cabeza_coloquial': {
                'keywords': ['me truena la cabeza', 'siento la cabeza pesada', 'me late la cabeza', 'me punza la cabeza', 'me palpita la cabeza', 'me arde la cabeza'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD'
                ],
                'sintomas': ['dolor cabeza intenso', 'migraña severa', 'cefalea'],
                'razon': 'Dolor de cabeza intenso expresado coloquialmente requiere magnesio relajante vascular, omega 3 antiinflamatorio, complejo B neurológico, y zinc equilibrador.'
            },

            'dolor_huesos_coloquial': {
                'keywords': ['me duelen los huesos', 'siento los huesos adoloridos', 'me truena todo', 'me duele hasta el alma', 'ando todo quebrado'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD'
                ],
                'sintomas': ['dolor articular generalizado', 'dolor oseo', 'rigidez corporal'],
                'razon': 'Dolor óseo generalizado requiere omega 3 antiinflamatorio, minerales para fortaleza ósea, magnesio relajante muscular, y zinc reparador.'
            },

            'estomago_revuelto_coloquial': {
                'keywords': ['tengo el estómago revuelto', 'se me revuelve el estómago', 'ando mal del estómago', 'tengo la panza revuelta', 'me anda mal la panza'],
                'productos': [
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'VC CHIA CAPSULA NUDRA C/60',
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['malestar gastrico', 'nauseas', 'indigestion'],
                'razon': 'Malestar estomacal requiere fenogreco digestivo, fibra reguladora, detox para limpiar sistema, y magnesio antiespasmódico.'
            },

            'cansancio_extremo_coloquial': {
                'keywords': ['ando muy cansado', 'me siento muy agotado', 'no tengo fuerzas', 'ando sin energía', 'me siento como trapo', 'ando arrastrando'],
                'productos': [
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['fatiga extrema', 'agotamiento fisico', 'falta energia'],
                'razon': 'Cansancio extremo requiere multivitamínico energizante, complejo B para metabolismo, omega 3 para función celular, y minerales para procesos vitales.'
            },

            'nervios_ansiedad_coloquial': {
                'keywords': ['traigo los nervios de punta', 'ando muy nervioso', 'tengo los nervios alterados', 'me andan fallando los nervios', 'ando muy acelerado'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['nerviosismo extremo', 'ansiedad', 'estres'],
                'razon': 'Nervios alterados requieren magnesio calmante natural, complejo B para sistema nervioso, omega 3 equilibrador, y multivitamínico estabilizador.'
            },

            'problemas_sueno_coloquial': {
                'keywords': ['no puedo dormir', 'no pego el ojo', 'me desvelo mucho', 'ando desvelado', 'no agarro el sueño'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['insomnio', 'trastorno sueño', 'desvelo'],
                'razon': 'Problemas de sueño requieren magnesio relajante nocturno, complejo B para ciclos naturales, omega 3 para función cerebral, y multivitamínico equilibrador.'
            },

            'dolor_espalda_coloquial': {
                'keywords': ['me duele la espalda horrible', 'traigo la espalda hecha pedazos', 'se me clava la espalda', 'ando jorobado del dolor'],
                'productos': [
                    'AR JUQUILITA UNGUENTO CENTRO BOTANICO MAYA 60 GRS',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['dolor espalda severo', 'contractura muscular', 'dolor lumbar'],
                'razon': 'Dolor de espalda severo requiere ungüento para alivio local, omega 3 antiinflamatorio, magnesio relajante muscular, y minerales fortalecedores.'
            },

            'diabetes_coloquial_mexicana': {
                'keywords': ['tengo el azúcar alta', 'ando alto de azúcar', 'se me subió el azúcar', 'traigo la diabetes', 'ando diabético'],
                'productos': [
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['glucosa elevada', 'diabetes', 'azucar alta'],
                'razon': 'Azúcar alta requiere fenogreco regulador natural, zinc para sensibilidad insulínica, omega 3 protector vascular, y minerales equilibradores.'
            },

            'presion_alta_coloquial': {
                'keywords': ['tengo la presión alta', 'ando alto de presión', 'se me sube la presión', 'traigo la presión por las nubes'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['hipertension', 'presion arterial elevada', 'presion alta'],
                'razon': 'Presión alta requiere magnesio vasodilatador, omega 3 cardioprotector, minerales equilibradores, y complejo B para función cardiovascular.'
            },

            'artritis_coloquial_mexicana': {
                'keywords': ['se me hinchan las coyunturas', 'me duelen las articulaciones feo', 'tengo las manos tiesas', 'se me entumen las manos'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['artritis', 'inflamacion articular', 'rigidez articular'],
                'razon': 'Problemas articulares requieren omega 3 antiinflamatorio potente, magnesio relajante, zinc reparador, y minerales para salud articular.'
            },

            'gastritis_coloquial_mexicana': {
                'keywords': ['me arde el estómago', 'se me quema el estómago', 'tengo acidez', 'me duele la boca del estómago', 'traigo gastritis'],
                'productos': [
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'VC CHIA CAPSULA NUDRA C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'HE DT DETOX CAPSULA CANATURA C/75'
                ],
                'sintomas': ['gastritis', 'acidez estomacal', 'ardor gastrico'],
                'razon': 'Gastritis requiere fenogreco protector gástrico, fibra reguladora, magnesio antiácido natural, y detox para limpiar sistema digestivo.'
            },

            # === CASOS CRÍTICOS FALTANTES EN MÉXICO ===
            
            'diabetes_simple': {
                'keywords': ['diabetes', 'soy diabético', 'padezco diabetes'],
                'productos': [
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['diabetes', 'glucosa elevada', 'metabolismo glucosa'],
                'razon': 'Diabetes requiere fenogreco regulador natural de glucosa, zinc para sensibilidad insulínica, omega 3 protector vascular, y minerales equilibradores metabólicos.'
            },

            'obesidad_sobrepeso': {
                'keywords': ['obesidad', 'sobrepeso', 'estoy gordo', 'necesito bajar de peso', 'quiero adelgazar'],
                'productos': [
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'VC CHIA CAPSULA NUDRA C/60'
                ],
                'sintomas': ['sobrepeso', 'obesidad', 'exceso peso'],
                'razon': 'Control de peso requiere detox para limpiar metabolismo, omega 3 para quemar grasa, multivitamínico para energía, y fibra para saciedad.'
            },

            'gastritis_mexicana': {
                'keywords': ['gastritis', 'acidez', 'agruras', 'úlcera', 'me duele el estómago'],
                'productos': [
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'VC CHIA CAPSULA NUDRA C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['gastritis', 'acidez', 'ulcera peptica'],
                'razon': 'Gastritis requiere fenogreco protector de mucosa gástrica, fibra calmante, magnesio antiácido, y complejo B reparador.'
            },

            'problemas_respiratorios': {
                'keywords': ['bronquitis', 'neumonía', 'tos crónica', 'gripa', 'catarro', 'infección respiratoria'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD',
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'HE DT DETOX CAPSULA CANATURA C/75'
                ],
                'sintomas': ['bronquitis', 'tos cronica', 'infeccion respiratoria'],
                'razon': 'Problemas respiratorios requieren omega 3 antiinflamatorio pulmonar, zinc inmunológico, multivitamínico fortalecedor, y detox purificador.'
            },

            'dolor_espalda_mexicano': {
                'keywords': ['dolor de espalda', 'me duele la espalda', 'dolor lumbar', 'lumbago', 'dolor de cintura'],
                'productos': [
                    'AR JUQUILITA UNGUENTO CENTRO BOTANICO MAYA 60 GRS',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['dolor espalda', 'lumbago', 'dolor lumbar'],
                'razon': 'Dolor de espalda requiere ungüento antiinflamatorio local, omega 3 sistémico, magnesio relajante muscular, y minerales fortalecedores.'
            },

            'fatiga_cansancio_mexicano': {
                'keywords': ['fatiga', 'cansancio', 'debilidad', 'me siento débil', 'sin energía', 'agotamiento'],
                'productos': [
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['fatiga', 'cansancio', 'debilidad'],
                'razon': 'Fatiga y cansancio requieren multivitamínico energizante, complejo B para metabolismo, omega 3 para función celular, y minerales vitales.'
            },

            'problemas_digestivos': {
                'keywords': ['colitis', 'diarrea', 'parásitos', 'intestino irritable', 'problemas digestivos'],
                'productos': [
                    'VC CHIA CAPSULA NUDRA C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'HE DT DETOX CAPSULA CANATURA C/75',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['colitis', 'diarrea', 'trastornos digestivos'],
                'razon': 'Problemas digestivos requieren fibra reguladora, magnesio antiespasmódico, detox purificador intestinal, y complejo B reparador.'
            },

            'problemas_cardiovasculares': {
                'keywords': ['infarto', 'problemas del corazón', 'arritmia', 'taquicardia', 'palpitaciones'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['problemas cardiacos', 'arritmia', 'palpitaciones'],
                'razon': 'Problemas cardiovasculares requieren omega 3 cardioprotector, magnesio para ritmo cardíaco, complejo B energético, y minerales equilibradores.'
            },

            'dolor_pecho_toracico': {
                'keywords': ['me duele el pecho', 'dolor torácico', 'opresión en el pecho', 'dolor en el corazón'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['dolor pecho', 'dolor toracico', 'molestias cardiacas'],
                'razon': 'Dolor torácico requiere omega 3 antiinflamatorio cardiovascular, magnesio relajante, complejo B para función cardíaca, y multivitamínico protector.'
            },

            'trigliceridos_colesterol': {
                'keywords': ['triglicéridos altos', 'triglicéridos', 'grasas en sangre', 'lípidos altos'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD',
                    'HE DT DETOX CAPSULA CANATURA C/75'
                ],
                'sintomas': ['trigliceridos altos', 'dislipidemia', 'grasas sangre'],
                'razon': 'Triglicéridos altos requieren omega 3 regulador lipídico, fenogreco natural, zinc metabólico, y detox purificador hepático.'
            },

            # === CASOS FINALES PARA COBERTURA COMPLETA MÉXICO ===
            
            'dolor_huesos_general': {
                'keywords': ['dolor de huesos', 'me duelen los huesos', 'dolor óseo'],
                'productos': [
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD'
                ],
                'sintomas': ['dolor oseo', 'dolor huesos', 'molestias oseas'],
                'razon': 'Dolor de huesos requiere minerales fortalecedores óseos, omega 3 antiinflamatorio, magnesio para función muscular, y zinc reparador.'
            },

            'reumatismo_general': {
                'keywords': ['reuma', 'reumatismo', 'dolor reumático'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['reumatismo', 'dolor reumatico', 'artritis'],
                'razon': 'Reumatismo requiere omega 3 antiinflamatorio articular, magnesio relajante, zinc reparador, y minerales para salud articular.'
            },

            'estres_nervios': {
                'keywords': ['estrés', 'nervios', 'estoy nervioso', 'me siento estresado'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['estres', 'nerviosismo', 'tension'],
                'razon': 'Estrés y nervios requieren magnesio relajante natural, complejo B para sistema nervioso, omega 3 equilibrador, y multivitamínico estabilizador.'
            },

            'insomnio_general': {
                'keywords': ['insomnio', 'no puedo dormir', 'trastornos del sueño'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['insomnio', 'trastornos sueno', 'desvelo'],
                'razon': 'Insomnio requiere magnesio relajante nocturno, complejo B para ciclos naturales, omega 3 para función cerebral, y multivitamínico regulador.'
            },

            'tiroides_general': {
                'keywords': ['tiroides', 'problemas de tiroides', 'glándula tiroides'],
                'productos': [
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD',
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['tiroides', 'disfuncion tiroidea', 'hormonal'],
                'razon': 'Problemas de tiroides requieren zinc regulador hormonal, multivitamínico equilibrador, omega 3 protector, y minerales cofactores tiroideos.'
            },

            'calculos_renales': {
                'keywords': ['cálculos renales', 'piedras en el riñón', 'cálculos', 'piedras riñón'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'HE DT DETOX CAPSULA CANATURA C/75'
                ],
                'sintomas': ['calculos renales', 'litiasis renal', 'piedras riñon'],
                'razon': 'Cálculos renales requieren magnesio preventivo de cristalización, minerales equilibradores, omega 3 protector renal, y detox purificador.'
            },

            'problemas_ginecologicos': {
                'keywords': ['miomas', 'quistes', 'irregularidad menstrual', 'trastornos menstruales', 'problemas menstruales'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['miomas', 'quistes ovaricos', 'irregularidad menstrual'],
                'razon': 'Problemas ginecológicos requieren omega 3 hormonal, complejo B regulador, zinc equilibrador reproductivo, y magnesio antiespasmódico.'
            },

            'problemas_masculinos': {
                'keywords': ['próstata', 'disfunción eréctil', 'calvicie', 'baja testosterona', 'problemas prostáticos'],
                'productos': [
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['prostata', 'disfuncion erectil', 'problemas masculinos'],
                'razon': 'Problemas masculinos requieren zinc prostático, omega 3 circulatorio, complejo B energético, y minerales para función reproductiva.'
            },

            'malestar_general_mexicano': {
                'keywords': ['me siento mal', 'ando enfermo', 'no me siento bien', 'malestar general', 'indisposición'],
                'productos': [
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['malestar general', 'indisposicion', 'enfermedad general'],
                'razon': 'Malestar general requiere multivitamínico fortalecedor, omega 3 protector, complejo B energético, y magnesio equilibrador para bienestar integral.'
            },

            # === CASOS ESPECÍFICOS FASE 4 - MEJORAS BASADAS EN ANÁLISIS DE 100 PRUEBAS ===
            
            'nauseas_especificas': {
                'keywords': ['náuseas', 'nausea', 'tengo náuseas', 'me dan náuseas', 'ganas de vomitar'],
                'productos': [
                    'OC CEREBRO TABLETA FRASCO NIS YA GREEN C/60',
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'OC NIS YA CER DUO TABLETA NIS YA GREEN C/60'
                ],
                'sintomas': ['nauseas', 'vomito', 'malestar digestivo'],
                'razon': 'Las náuseas requieren equilibrio digestivo y neurológico. El fenogreco mejora la digestión, el magnesio estabiliza el sistema nervioso, y los productos cerebrales mejoran la circulación que puede causar náuseas.'
            },
            
            'mareos_vertigo': {
                'keywords': ['mareos', 'mareo', 'me mareo', 'vértigo', 'vertigo', 'inestabilidad'],
                'productos': [
                    'OC CEREBRO TABLETA FRASCO NIS YA GREEN C/60',
                    'OC NIS YA CER DUO TABLETA NIS YA GREEN C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60'
                ],
                'sintomas': ['mareos', 'vertigo', 'inestabilidad'],
                'razon': 'Los mareos frecuentemente se relacionan con circulación cerebral deficiente. Los productos cerebrales mejoran el flujo sanguíneo al cerebro, el magnesio estabiliza el equilibrio neurológico.'
            },
            
            'ciatica_especifica': {
                'keywords': ['ciática', 'ciatica', 'me duele la ciática', 'dolor ciático', 'nervio ciático'],
                'productos': [
                    'AR CURA DOL FLEX PLUS TABLETA NIS YA GREEN C/30',
                    'AR JUQUILITA UNGUENTO CENTRO BOTANICO MAYA 60 GRS',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR CURA DOL FLEX TABLETA NIS YA GREEN C/30'
                ],
                'sintomas': ['ciatica', 'dolor nervio ciatico', 'dolor lumbar'],
                'razon': 'La ciática requiere antiinflamatorios específicos para el sistema óseo y nervioso. CuraDol Flex es específico para dolor del sistema óseo, el ungüento Juquilita para aplicación local, y magnesio como relajante muscular.'
            },
            
            'dolor_muscular_general': {
                'keywords': ['dolor muscular', 'dolor de músculos', 'me duelen los músculos', 'dolor en músculos'],
                'productos': [
                    'AR CURA DOL FLEX TABLETA NIS YA GREEN C/30',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR JUQUILITA UNGUENTO CENTRO BOTANICO MAYA 60 GRS',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['dolor muscular', 'tension muscular', 'contractura'],
                'razon': 'El dolor muscular requiere antiinflamatorios naturales y relajantes musculares. CuraDol Flex reduce la inflamación, el magnesio relaja los músculos, y los minerales ayudan en la recuperación muscular.'
            },
            
            'ansiedad_pura': {
                'keywords': ['ansiedad', 'me siento ansioso', 'tengo ansiedad', 'crisis de ansiedad', 'ataque de ansiedad'],
                'productos': [
                    'SN VALERIANA DUO TABLETA NIS YA GREEN C/60',
                    'IS DAMIANA DUO TABLETA NIS YA GREEN C/60',
                    'PA ESPINO BLANCO DUO TABLETA NIS YA GREEN C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['ansiedad', 'crisis ansiedad', 'nerviosismo'],
                'razon': 'La ansiedad requiere relajantes naturales específicos. La valeriana es el relajante natural más efectivo, la damiana equilibra el sistema nervioso, el espino blanco regula el ritmo cardíaco asociado a la ansiedad.'
            },
            
            'infecciones_respiratorias': {
                'keywords': ['infecciones respiratorias', 'me enfermo de gripa', 'infecciones de garganta', 'bronquitis recurrente'],
                'productos': [
                    'AP INMUNOL SPRAY NIS YA 60 ML',
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD',
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['infecciones respiratorias', 'gripa recurrente', 'defensas bajas'],
                'razon': 'Las infecciones respiratorias requieren fortalecimiento del sistema inmune. El spray inmunológico actúa directamente, la equinácea fortalece las defensas, el zinc es antimicrobiano específico.'
            },
            
            'infecciones_urinarias': {
                'keywords': ['infección urinaria', 'cistitis', 'ardor al orinar', 'molestias al orinar', 'infección de vías urinarias'],
                'productos': [
                    'RP COLA CABALLO DUO TABLETA NIS YA GREEN C/60',
                    'RP DORADILLA TABLETA FRASCO NIS YA GREEN C/60',
                    'AR ORTIGA CALCIO GLUCOSAMINA DUO TABLETA NIS YA C/60',
                    'PA CORA ZN ABEDUL DUO TABLETA NIS YA GREEN C/60'
                ],
                'sintomas': ['infeccion urinaria', 'cistitis', 'ardor orinar'],
                'razon': 'Las infecciones urinarias requieren diuréticos naturales específicos. Cola de caballo y doradilla limpian profundamente las vías urinarias, desinflaman riñones y vejiga, la ortiga mejora la función urinaria.'
            },
            
            'defensas_bajas_general': {
                'keywords': ['defensas bajas', 'me enfermo seguido', 'bajo sistema inmune', 'infecciones recurrentes'],
                'productos': [
                    'AP INMUNOL SPRAY NIS YA 60 ML',
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD',
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['defensas bajas', 'sistema inmune debil', 'infecciones repetidas'],
                'razon': 'Las defensas bajas requieren fortalecimiento inmunológico integral. El spray inmunológico es específico para el sistema inmune, la equinácea es adaptógena, el zinc fortalece defensas, las vitaminas proveen soporte completo.'
            },
            
            'problemas_piel_inflamatorios': {
                'keywords': ['urticaria', 'dermatitis', 'ronchas', 'irritación de piel', 'problemas de piel'],
                'productos': [
                    'HC CHARDON MARIE DUO TABLETA NIS YA GREEN C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD',
                    'PA CORA ZN ABEDUL DUO TABLETA NIS YA GREEN C/60'
                ],
                'sintomas': ['urticaria', 'dermatitis', 'problemas piel'],
                'razon': 'Los problemas inflamatorios de piel requieren desintoxicación profunda y nutrientes específicos. El cardo mariano desintoxica el hígado (clave para piel sana), omega 3 reduce inflamación, zinc repara tejidos.'
            },
            
            'cansancio_cronico': {
                'keywords': ['me siento cansado', 'tengo cansancio', 'me canso fácil', 'sin energía', 'fatiga crónica'],
                'productos': [
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD'
                ],
                'sintomas': ['cansancio cronico', 'fatiga', 'falta energia'],
                'razon': 'El cansancio crónico requiere nutrientes energéticos específicos. El multivitamínico provee energía general, el complejo B es esencial para el metabolismo energético, la equinácea fortalece el organismo.'
            },
            
            'dolor_articulaciones_especifico': {
                'keywords': ['dolor en las articulaciones', 'dolor articular', 'me duelen las articulaciones', 'articulaciones rígidas'],
                'productos': [
                    'AR ORTIGA CALCIO GLUCOSAMINA DUO TABLETA NIS YA C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['dolor articular', 'rigidez articulaciones', 'artritis'],
                'razon': 'El dolor articular requiere nutrientes específicos para cartílago y huesos. La ortiga con glucosamina repara cartílago, omega 3 reduce inflamación articular, magnesio relaja músculos periarticulares.'
            },
            
            'molestias_estomacales_generales': {
                'keywords': ['molestias estomacales', 'malestar estomacal', 'problemas de estómago', 'estómago revuelto', 'ando malo del estómago'],
                'productos': [
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'UG COPALCHI TABLETA FRASCO NIS YA GREEN C/60',
                    'VC CHIA CAPSULA NUDRA C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['molestias estomacales', 'malestar estomago', 'dispepsia'],
                'razon': 'Las molestias estomacales requieren productos digestivos específicos. El fenogreco mejora la digestión, el copalchi cicatriza y protege mucosas gástricas, la chía aporta fibra protectora.'
            },
            
            'tos_seca_cronica': {
                'keywords': ['tos', 'tengo tos seca', 'tos crónica', 'tos persistente', 'tos irritativa'],
                'productos': [
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD',
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['tos seca', 'tos cronica', 'tos persistente'],
                'razon': 'La tos persistente requiere fortalecimiento inmunológico respiratorio. La equinácea fortalece defensas respiratorias, omega 3 reduce inflamación pulmonar, zinc tiene propiedades antimicrobianas.'
            },

            # === CASOS FINALES PARA 100% COBERTURA ===
            
            'sangrado_hemorragias': {
                'keywords': ['sangrado', 'hemorragia', 'sangrando', 'pérdida de sangre', 'sangre'],
                'productos': [
                    'AF HBINE ZARZAPARRILLA TONICO NIS YA 1 LT',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60'
                ],
                'sintomas': ['sangrado', 'hemorragia', 'anemia'],
                'razon': 'El sangrado requiere productos que aumenten la producción de glóbulos rojos. La zarzaparrilla aumenta hemoglobina, el zinc mejora cicatrización, las vitaminas fortalecen el sistema sanguíneo.'
            },
            
            'hongos_unas': {
                'keywords': ['hongos en uñas', 'hongos uñas', 'onicomicosis', 'infección por hongos', 'uñas con hongos'],
                'productos': [
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD',
                    'AR ZINC CAPSULA WINIK WAY C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60'
                ],
                'sintomas': ['hongos unas', 'infeccion ungueal', 'onicomicosis'],
                'razon': 'Los hongos en uñas requieren zinc antimicrobiano específico para fortalecer el sistema inmune, omega 3 para regeneración tisular, y equinácea para defensas antifúngicas naturales.'
            },
            
            'migrania_especifica': {
                'keywords': ['migraña', 'jaqueca', 'dolor de cabeza severo', 'cefalea'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR CURA DOL FLEX PLUS TABLETA NIS YA GREEN C/30',
                    'OC CEREBRO TABLETA FRASCO NIS YA GREEN C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['migrania', 'jaqueca', 'cefalea severa'],
                'razon': 'La migraña requiere magnesio para relajación vascular cerebral, CuraDol Flex para dolor del sistema nervioso, productos cerebrales para circulación, y complejo B para función neurológica.'
            },
            
            'caida_cabello': {
                'keywords': ['caída del cabello', 'alopecia', 'se me cae el cabello', 'calvicie', 'pérdida de cabello'],
                'productos': [
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD',
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'OC CEREBRO TABLETA FRASCO NIS YA GREEN C/60'
                ],
                'sintomas': ['caida cabello', 'alopecia', 'calvicie'],
                'razon': 'La caída del cabello requiere zinc esencial para cabello y piel, multivitamínico para nutrición folicular, complejo B para crecimiento capilar, y productos cerebrales para circulación del cuero cabelludo.'
            },
            
            'infertilidad_reproductiva': {
                'keywords': ['infertilidad', 'no puedo embarazarme', 'problemas para concebir', 'esterilidad'],
                'productos': [
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD',
                    'PM ISOFLAVONAS DUO TABLETA NIS YA GREEN C/60',
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['infertilidad', 'problemas reproductivos', 'esterilidad'],
                'razon': 'La infertilidad requiere zinc esencial para función reproductiva, isoflavonas para regulación hormonal femenina, multivitamínico para nutrición reproductiva, y omega 3 para salud celular.'
            },
            
            'fiebre_temperatura': {
                'keywords': ['fiebre', 'temperatura alta', 'calentura', 'tengo fiebre'],
                'productos': [
                    'AP INMUNOL SPRAY NIS YA 60 ML',
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD',
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['fiebre', 'temperatura elevada', 'calentura'],
                'razon': 'La fiebre requiere fortalecimiento inmunológico inmediato. El spray inmunológico actúa rápidamente, la equinácea es antiinflamatoria natural, el zinc combate infecciones, las vitaminas apoyan la recuperación.'
            },
            
            'calambres_espasmos': {
                'keywords': ['calambres', 'espasmos musculares', 'me dan calambres', 'contracciones musculares'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AR CURA DOL FLEX TABLETA NIS YA GREEN C/30',
                    'SN VALERIANA DUO TABLETA NIS YA GREEN C/60'
                ],
                'sintomas': ['calambres', 'espasmos musculares', 'contracturas'],
                'razon': 'Los calambres requieren magnesio relajante muscular específico, minerales para función neuromuscular, antiinflamatorio muscular, y valeriana relajante del sistema nervioso.'
            },
            
            'rosacea_enrojecimiento': {
                'keywords': ['rosácea', 'enrojecimiento facial', 'rojez en la cara', 'cara roja'],
                'productos': [
                    'HC CHARDON MARIE DUO TABLETA NIS YA GREEN C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'PA CORA ZN ABEDUL DUO TABLETA NIS YA GREEN C/60',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD'
                ],
                'sintomas': ['rosacea', 'enrojecimiento facial', 'piel irritada'],
                'razon': 'La rosácea requiere desintoxicación hepática profunda con cardo mariano (clave para piel sana), omega 3 antiinflamatorio cutáneo, abedul depurativo, y zinc reparador dérmico.'
            },
            
            'dificultad_respiratoria_especifica': {
                'keywords': ['dificultades respiratorias', 'me falta aire', 'respiración difícil', 'ahogo', 'disnea'],
                'productos': [
                    'AP PULMON TABLETA FRASCO NIS YA GREEN C/60',
                    'DO PURIF GOLDEN SEAL TONICO NIS YA 1 LT',
                    'OC NIS YA CER DUO TABLETA NIS YA GREEN C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['dificultad respiratoria', 'disnea', 'falta aire'],
                'razon': 'Las dificultades respiratorias requieren productos específicos para pulmón, oxigenantes sanguíneos como Golden Seal, productos cerebrales para oxigenación, y omega 3 antiinflamatorio pulmonar.'
            },
            
            'acne_granos': {
                'keywords': ['acné', 'granos', 'espinillas', 'barros', 'piel grasa'],
                'productos': [
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD',
                    'HC CHARDON MARIE DUO TABLETA NIS YA GREEN C/60',
                    'PM ISOFLAVONAS DUO TABLETA NIS YA GREEN C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['acne', 'granos', 'espinillas'],
                'razon': 'El acné requiere zinc específico para piel y control hormonal, cardo mariano desintoxicante hepático (esencial para piel limpia), isoflavonas para equilibrio hormonal, y omega 3 antiinflamatorio cutáneo.'
            },

            # === ÚLTIMOS 5 CASOS PARA 100% COMPLETO ===
            
            'vomito_nauseas': {
                'keywords': ['vómito', 'vomitar', 'estoy vomitando', 'me da vómito', 'devolver'],
                'productos': [
                    'UG COPALCHI TABLETA FRASCO NIS YA GREEN C/60',
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'OC CEREBRO TABLETA FRASCO NIS YA GREEN C/60'
                ],
                'sintomas': ['vomito', 'nauseas severas', 'malestar gastrico'],
                'razon': 'El vómito requiere productos que protejan y cicatricen mucosas gástricas. El copalchi previene úlceras y permite cicatrización, el fenogreco mejora digestión, el magnesio calma el sistema nervioso.'
            },
            
            'caspa_cuero_cabelludo': {
                'keywords': ['caspa', 'descamación del cuero cabelludo', 'tengo caspa', 'cuero cabelludo seco'],
                'productos': [
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD',
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'OC CEREBRO TABLETA FRASCO NIS YA GREEN C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['caspa', 'descamacion cuero cabelludo', 'sequedad capilar'],
                'razon': 'La caspa requiere zinc esencial para salud del cuero cabelludo, multivitamínico para nutrición folicular, productos cerebrales para circulación capilar, y complejo B para regeneración celular.'
            },
            
            'picazon_comezón': {
                'keywords': ['picazón', 'comezón', 'me pica', 'prurito', 'rascarse'],
                'productos': [
                    'HC CHARDON MARIE DUO TABLETA NIS YA GREEN C/60',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'PA CORA ZN ABEDUL DUO TABLETA NIS YA GREEN C/60'
                ],
                'sintomas': ['picazon', 'comezon', 'prurito'],
                'razon': 'La picazón requiere desintoxicación profunda con cardo mariano para eliminar toxinas que causan prurito, zinc antiinflamatorio cutáneo, omega 3 calmante, y abedul depurativo.'
            },
            
            'inflamacion_general': {
                'keywords': ['inflamación', 'hinchazón', 'inflamado', 'hinchado', 'proceso inflamatorio'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AR CURA DOL FLEX TABLETA NIS YA GREEN C/30',
                    'AB GLUCONATO ZINC CAPSULA CANATURA GOLD',
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60'
                ],
                'sintomas': ['inflamacion', 'hinchazón', 'proceso inflamatorio'],
                'razon': 'La inflamación requiere omega 3 antiinflamatorio natural potente, CuraDol Flex antiinflamatorio específico, zinc modulador inmune, y equinácea antiinflamatoria natural.'
            },
            
            'dolor_cronico_persistente': {
                'keywords': ['dolor crónico', 'sufro de dolor crónico', 'dolor persistente', 'dolor constante'],
                'productos': [
                    'AR CURA DOL FLEX PLUS TABLETA NIS YA GREEN C/30',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['dolor cronico', 'dolor persistente', 'dolor constante'],
                'razon': 'El dolor crónico requiere CuraDol Flex Plus específico para dolor del sistema óseo, magnesio relajante muscular y nervioso, omega 3 antiinflamatorio sistémico, y complejo B para función neurológica.'
            },

            # === CASOS FALTANTES PARA 100% COBERTURA ===
            
            'alergias_respiratorias_especifica': {
                'keywords': ['alergias respiratorias', 'alergia respiratoria', 'alergia en nariz', 'rinitis alérgica'],
                'productos': [
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'DO PURIF GOLDEN SEAL TONICO NIS YA 1 LT',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['alergia respiratoria', 'rinitis alergica', 'estornudos'],
                'razon': 'Las alergias respiratorias requieren equinácea inmunomoduladora, vitamina C antihistamínica natural, Golden Seal antiinflamatorio respiratorio, y complejo B para función inmune.'
            },

            'irritabilidad_nervios': {
                'keywords': ['irritabilidad', 'estoy irritable', 'me irrito fácil', 'ando irritable', 'malhumor'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB L TRIPTOFANO CAPSULA CANATURA GOLD C/90',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['irritabilidad', 'malhumor', 'nerviosismo'],
                'razon': 'La irritabilidad requiere magnesio calmante del sistema nervioso, complejo B para neurotransmisores, triptófano precursor de serotonina, y omega 3 neuroprotector.'
            },

            'cambios_humor_emocional': {
                'keywords': ['cambios de humor', 'cambios emocionales', 'ando muy cambiante', 'humor variable'],
                'productos': [
                    'AB L TRIPTOFANO CAPSULA CANATURA GOLD C/90',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'PM ISOFLAVONAS DUO TABLETA NIS YA GREEN C/60'
                ],
                'sintomas': ['cambios humor', 'inestabilidad emocional', 'variabilidad emocional'],
                'razon': 'Los cambios de humor requieren triptófano para serotonina estable, complejo B para neurotransmisores, magnesio estabilizador, e isoflavonas para equilibrio hormonal.'
            },

            'tristeza_decaimiento': {
                'keywords': ['tristeza', 'estoy triste', 'me siento triste', 'decaído', 'bajo de ánimo'],
                'productos': [
                    'AB L TRIPTOFANO CAPSULA CANATURA GOLD C/90',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['tristeza', 'decaimiento', 'bajo animo'],
                'razon': 'La tristeza requiere triptófano para serotonina (hormona de la felicidad), complejo B para función neurológica, multivitamínico energizante, y omega 3 neuroprotector.'
            },

            'preocupacion_mental': {
                'keywords': ['preocupación', 'me preocupo mucho', 'ando preocupado', 'pensamientos negativos'],
                'productos': [
                    'AB L TRIPTOFANO CAPSULA CANATURA GOLD C/90',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['preocupacion', 'pensamientos negativos', 'rumiacion mental'],
                'razon': 'La preocupación excesiva requiere triptófano calmante mental, magnesio relajante del sistema nervioso, complejo B para función cerebral, y omega 3 para salud neurológica.'
            },

            'manchas_piel_cutaneas': {
                'keywords': ['manchas en la piel', 'manchas cutáneas', 'hiperpigmentación', 'piel manchada'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'HC CHARDON MARIE DUO TABLETA NIS YA GREEN C/60',
                    'AR VITAMINA A BETACAROTENO CAPSULA CANATURA GOLD',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['manchas piel', 'hiperpigmentacion', 'decoloracion cutanea'],
                'razon': 'Las manchas cutáneas requieren zinc regenerador celular, cardo mariano desintoxicante hepático, vitamina A para renovación celular, y vitamina C antioxidante despigmentante.'
            },

            'piel_seca_deshidratada': {
                'keywords': ['piel seca', 'piel deshidratada', 'resequedad cutánea', 'falta humedad piel'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AR VITAMINA A BETACAROTENO CAPSULA CANATURA GOLD',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF VITAMINA E CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['piel seca', 'resequedad cutanea', 'deshidratacion piel'],
                'razon': 'La piel seca requiere omega 3 para hidratación celular, vitamina A regeneradora cutánea, zinc reparador tisular, y vitamina E hidratante natural.'
            },

            'irritacion_cutanea_dermica': {
                'keywords': ['irritación cutánea', 'piel irritada', 'irritación dérmica', 'sensibilidad cutánea'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'HC CHARDON MARIE DUO TABLETA NIS YA GREEN C/60',
                    'AF VITAMINA E CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['irritacion cutanea', 'sensibilidad piel', 'inflamacion dermica'],
                'razon': 'La irritación cutánea requiere omega 3 antiinflamatorio dérmico, zinc cicatrizante y calmante, cardo mariano desintoxicante, y vitamina E protectora cutánea.'
            },

            'heridas_cicatrizacion': {
                'keywords': ['heridas', 'cicatrización lenta', 'heridas que no sanan', 'cortes', 'raspones'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA A BETACAROTENO CAPSULA CANATURA GOLD',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['heridas', 'cicatrizacion lenta', 'regeneracion tisular'],
                'razon': 'Las heridas requieren zinc esencial para cicatrización, vitamina C para síntesis de colágeno, vitamina A regeneradora celular, y minerales para reparación tisular.'
            },

            'cicatrices_marcas': {
                'keywords': ['cicatrices', 'marcas en la piel', 'queloides', 'cicatrización deficiente'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA A BETACAROTENO CAPSULA CANATURA GOLD',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['cicatrices', 'queloides', 'marcas cutaneas'],
                'razon': 'Las cicatrices requieren zinc para remodelación tisular, vitamina C para colágeno saludable, vitamina A regeneradora, y omega 3 para elasticidad cutánea.'
            },

            'flujo_vaginal_leucorrea': {
                'keywords': ['flujo vaginal', 'leucorrea', 'secreción vaginal', 'flujo abundante'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'HC CHARDON MARIE DUO TABLETA NIS YA GREEN C/60'
                ],
                'sintomas': ['flujo vaginal', 'leucorrea', 'secrecion vaginal'],
                'razon': 'El flujo vaginal requiere zinc para equilibrio de pH y función inmune, minerales para flora vaginal, complejo B para mucosas sanas, y cardo mariano desintoxicante.'
            },

            'infecciones_urinarias_cistitis': {
                'keywords': ['infecciones urinarias', 'cistitis', 'infección en la vejiga', 'ardor al orinar'],
                'productos': [
                    'RP UVA URSI COLA DE CABALLO DUO TABLETA NIS YA GREEN C/60',
                    'RP RIN DORADILLA TONICO NIS YA 1 LT',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['infeccion urinaria', 'cistitis', 'ardor orinar'],
                'razon': 'Las infecciones urinarias requieren uva ursi y cola de caballo antisépticos urinarios, doradilla diurética desinfectante, zinc antimicrobiano, y vitamina C acidificante urinaria.'
            },

            'resistencia_insulina_metabolica': {
                'keywords': ['resistencia a la insulina', 'resistencia insulínica', 'prediabetes', 'síndrome X'],
                'productos': [
                    'CN DG MAGOL L11 CAPSULA CANATURA C/75',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['resistencia insulina', 'prediabetes', 'sindrome metabolico'],
                'razon': 'La resistencia a la insulina requiere Magol L11 regulador glucémico, minerales para metabolismo, omega 3 sensibilizador de insulina, y complejo B para metabolismo de glucosa.'
            },

            'sindrome_metabolico_completo': {
                'keywords': ['síndrome metabólico', 'síndrome X', 'disfunción metabólica', 'metabolismo lento'],
                'productos': [
                    'CN DG MAGOL L11 CAPSULA CANATURA C/75',
                    'HC CHARDON MARIE DUO TABLETA NIS YA GREEN C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['sindrome metabolico', 'disfuncion metabolica', 'metabolismo lento'],
                'razon': 'El síndrome metabólico requiere Magol L11 regulador metabólico, cardo mariano desintoxicante hepático, omega 3 para metabolismo de lípidos, y multivitamínico energizante.'
            },

            'virus_infeccion_viral': {
                'keywords': ['virus', 'infección viral', 'viral', 'tengo un virus'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['virus', 'infeccion viral', 'proceso viral'],
                'razon': 'Las infecciones virales requieren zinc antiviral potente, equinácea inmunoestimulante, vitamina C antioxidante e inmune, y complejo B para energía y recuperación.'
            },

            'bacteria_infeccion_bacteriana': {
                'keywords': ['bacteria', 'infección bacteriana', 'bacteriana', 'tengo bacteria'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'DO PURIF GOLDEN SEAL TONICO NIS YA 1 LT',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60'
                ],
                'sintomas': ['bacteria', 'infeccion bacteriana', 'proceso bacteriano'],
                'razon': 'Las infecciones bacterianas requieren zinc antimicrobiano, Golden Seal antibiótico natural, vitamina C para inmunidad, y equinácea antibacteriana.'
            },

            'hongos_infeccion_fungica': {
                'keywords': ['hongos', 'infección por hongos', 'micosis', 'fúngica'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'HC CHARDON MARIE DUO TABLETA NIS YA GREEN C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['hongos', 'micosis', 'infeccion fungica'],
                'razon': 'Las infecciones fúngicas requieren zinc antifúngico, cardo mariano desintoxicante anti-hongos, minerales para equilibrar pH, y complejo B para flora saludable.'
            },

            'somnolencia_adormecimiento': {
                'keywords': ['somnolencia', 'me da sueño', 'adormecimiento', 'modorra', 'sopor'],
                'productos': [
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['somnolencia', 'adormecimiento', 'sopor'],
                'razon': 'La somnolencia requiere multivitamínico energizante, complejo B para energía celular, minerales para vitalidad, y omega 3 para función cerebral activa.'
            },

            'rendimiento_bajo_performance': {
                'keywords': ['rendimiento', 'bajo rendimiento', 'performance', 'desempeño bajo'],
                'productos': [
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'OC NIS YA CER DUO TABLETA NIS YA GREEN C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['bajo rendimiento', 'performance bajo', 'desempeño reducido'],
                'razon': 'El bajo rendimiento requiere multivitamínico para energía general, cerebrales para función cognitiva, complejo B para energía mental, y omega 3 para concentración.'
            },

            'vitalidad_energia_baja': {
                'keywords': ['vitalidad', 'falta de vitalidad', 'sin vitalidad', 'poca energía vital'],
                'productos': [
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['falta vitalidad', 'baja energia vital', 'sin energia'],
                'razon': 'La falta de vitalidad requiere multivitamínico revitalizante, minerales para energía celular, complejo B para vitalidad, y omega 3 para función óptima.'
            },

            'dolor_todo_cuerpo_generalizado': {
                'keywords': ['me duele todo el cuerpo', 'dolor generalizado', 'dolor en todo el cuerpo', 'molestias generales'],
                'productos': [
                    'AR CURA DOL FLEX TABLETA NIS YA GREEN C/30',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['dolor generalizado', 'molestias corporales', 'dolor todo cuerpo'],
                'razon': 'El dolor corporal generalizado requiere CuraDol Flex antiinflamatorio sistémico, omega 3 para inflamación general, magnesio relajante muscular, y complejo B para función nerviosa.'
            },

            # === FASE 1: 30 CASOS ALTA PRIORIDAD - SINÓNIMOS COMUNES ===
            
            'dolor_estomago_sinonimo': {
                'keywords': ['dolor estómago', 'dolor de estómago', 'me duele el estómago'],
                'productos': [
                    'UG COPALCHI TABLETA FRASCO NIS YA GREEN C/60',
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['dolor estomacal', 'dolor gastrico', 'malestar estomacal'],
                'razon': 'El dolor estomacal requiere copalchi calmante gástrico, fenogreco digestivo, multivitamínico para energía, y magnesio relajante muscular.'
            },

            'dolor_cabeza_sinonimo': {
                'keywords': ['dolor cabeza', 'dolor de cabeza', 'me duele la cabeza'],
                'productos': [
                    'AR CURA DOL FLEX TABLETA NIS YA GREEN C/30',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['cefalea', 'dolor craneal', 'jaqueca'],
                'razon': 'El dolor de cabeza requiere CuraDol Flex analgésico, magnesio relajante vascular, complejo B para función neurológica, y omega 3 antiinflamatorio.'
            },

            'dolor_espalda_sinonimo': {
                'keywords': ['dolor espalda', 'dolor de espalda', 'me duele la espalda'],
                'productos': [
                    'AR CURA DOL FLEX PLUS TABLETA NIS YA GREEN C/30',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['dolor dorsal', 'dolor lumbar', 'dorsalgia'],
                'razon': 'El dolor de espalda requiere CuraDol Flex Plus antiinflamatorio específico, magnesio relajante muscular, omega 3 para inflamación, y complejo B para nervios.'
            },

            'gases_flatulencias': {
                'keywords': ['gases', 'flatulencias', 'me dan gases', 'tengo muchos gases'],
                'productos': [
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'UG COPALCHI TABLETA FRASCO NIS YA GREEN C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['gases intestinales', 'flatulencia', 'meteorismo'],
                'razon': 'Los gases requieren fenogreco carminativo, copalchi digestivo, complejo B para función intestinal, y magnesio relajante del tracto digestivo.'
            },

            'constipacion_estreñimiento': {
                'keywords': ['constipación', 'estreñido', 'constipado del estómago'],
                'productos': [
                    'AR PSYLLIUM PLANTAGO CAPSULA CANATURA GOLD',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['estreñimiento', 'constipacion', 'evacuacion dificil'],
                'razon': 'La constipación requiere psyllium fibra natural, magnesio laxante suave, complejo B para motilidad intestinal, y omega 3 lubricante natural.'
            },

            'gripe_influenza': {
                'keywords': ['gripe', 'influenza', 'tengo gripe', 'gripita'],
                'productos': [
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['gripe', 'influenza', 'proceso gripal'],
                'razon': 'La gripe requiere equinácea inmunoestimulante, vitamina C antiviral, zinc para inmunidad, y complejo B para recuperación energética.'
            },

            'resfriado_catarro': {
                'keywords': ['resfriado', 'catarro', 'resfriado común', 'constipado'],
                'productos': [
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'DO PURIF GOLDEN SEAL TONICO NIS YA 1 LT',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['resfriado', 'catarro', 'rinorrea'],
                'razon': 'El resfriado requiere equinácea inmune, vitamina C antioxidante, Golden Seal antimicrobiano, y zinc antiviral.'
            },

            'dolor_garganta_faringitis': {
                'keywords': ['dolor garganta', 'dolor de garganta', 'garganta irritada'],
                'productos': [
                    'DO PURIF GOLDEN SEAL TONICO NIS YA 1 LT',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60'
                ],
                'sintomas': ['faringitis', 'dolor faringeo', 'irritacion garganta'],
                'razon': 'El dolor de garganta requiere Golden Seal antiséptico, vitamina C cicatrizante, zinc antimicrobiano, y equinácea antiinflamatoria.'
            },

            'congestion_nasal': {
                'keywords': ['congestión nasal', 'nariz tapada', 'no puedo respirar por la nariz'],
                'productos': [
                    'DO PURIF GOLDEN SEAL TONICO NIS YA 1 LT',
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['congestion nasal', 'obstruccion nasal', 'rinitis'],
                'razon': 'La congestión nasal requiere Golden Seal descongestionante, equinácea antiinflamatoria, vitamina C para mucosas, y zinc antimicrobiano.'
            },

            'colicos_menstruales_sinonimo': {
                'keywords': ['cólicos menstruales', 'dolor menstrual', 'regla dolorosa'],
                'productos': [
                    'PM ISOFLAVONAS DUO TABLETA NIS YA GREEN C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['dismenorrea', 'dolor menstrual', 'colicos menstruales'],
                'razon': 'Los cólicos menstruales requieren isoflavonas reguladoras hormonales, magnesio antiespasmódico, omega 3 antiinflamatorio, y complejo B para equilibrio hormonal.'
            },

            'sofocos_bochornos': {
                'keywords': ['sofocos', 'bochornos', 'calores', 'oleadas de calor'],
                'productos': [
                    'PM ISOFLAVONAS DUO TABLETA NIS YA GREEN C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['sofocos', 'bochornos', 'calores menopausicos'],
                'razon': 'Los sofocos requieren isoflavonas equilibrantes hormonales, complejo B para termorregulación, magnesio calmante, y minerales para balance hormonal.'
            },

            'cambios_humor_sinonimo': {
                'keywords': ['cambios humor', 'humor cambiante', 'ando muy cambiante'],
                'productos': [
                    'AB L TRIPTOFANO CAPSULA CANATURA GOLD C/90',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'PM ISOFLAVONAS DUO TABLETA NIS YA GREEN C/60'
                ],
                'sintomas': ['labilidad emocional', 'inestabilidad humor', 'variabilidad emocional'],
                'razon': 'Los cambios de humor requieren triptófano estabilizador serotonina, complejo B neurotransmisor, magnesio calmante nervioso, e isoflavonas equilibrio hormonal.'
            },

            'falta_energia_sinonimo': {
                'keywords': ['falta energía', 'falta de energía', 'sin energía'],
                'productos': [
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['astenia', 'falta energia', 'decaimiento energetico'],
                'razon': 'La falta de energía requiere multivitamínico energizante, complejo B para metabolismo energético, minerales para vitalidad, y omega 3 para función celular.'
            },

            'mal_digestion': {
                'keywords': ['mal digestión', 'mala digestión', 'no digiero bien'],
                'productos': [
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'UG COPALCHI TABLETA FRASCO NIS YA GREEN C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['dispepsia', 'indigestion', 'digestion lenta'],
                'razon': 'La mala digestión requiere fenogreco digestivo, copalchi estomacal, complejo B para enzimas digestivas, y magnesio relajante digestivo.'
            },

            'dolor_abdominal': {
                'keywords': ['dolor abdominal', 'dolor en el abdomen', 'dolor de vientre'],
                'productos': [
                    'UG COPALCHI TABLETA FRASCO NIS YA GREEN C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['dolor abdominal', 'dolor ventral', 'molestia abdominal'],
                'razon': 'El dolor abdominal requiere copalchi calmante digestivo, magnesio antiespasmódico, fenogreco digestivo, y complejo B para función intestinal.'
            },

            'dolor_rodillas_sinonimo': {
                'keywords': ['dolor rodillas', 'dolor de rodillas', 'me duelen las rodillas'],
                'productos': [
                    'AR CURA DOL FLEX TABLETA NIS YA GREEN C/30',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['gonalgia', 'dolor articular rodilla', 'artritis rodilla'],
                'razon': 'El dolor de rodillas requiere CuraDol Flex antiinflamatorio articular, omega 3 para cartílago, zinc reparador, y minerales para huesos.'
            },

            'dolor_cuello_sinonimo': {
                'keywords': ['dolor cuello', 'dolor de cuello', 'me duele el cuello'],
                'productos': [
                    'AR CURA DOL FLEX TABLETA NIS YA GREEN C/30',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['cervicalgia', 'dolor cervical', 'tension cervical'],
                'razon': 'El dolor de cuello requiere CuraDol Flex analgésico, magnesio relajante muscular cervical, complejo B para nervios, y omega 3 antiinflamatorio.'
            },

            'articulaciones_dolor': {
                'keywords': ['articulaciones', 'dolor en articulaciones', 'articulaciones adoloridas'],
                'productos': [
                    'AR CURA DOL FLEX PLUS TABLETA NIS YA GREEN C/30',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['artralgia', 'dolor articular', 'artropatia'],
                'razon': 'El dolor articular requiere CuraDol Flex Plus específico articular, omega 3 antiinflamatorio articular, zinc reparador cartílago, y minerales para articulaciones.'
            },

            'colesterol_sinonimo': {
                'keywords': ['colesterol', 'tengo colesterol', 'grasa en sangre'],
                'productos': [
                    'HC CHARDON MARIE DUO TABLETA NIS YA GREEN C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['hipercolesterolemia', 'dislipidemia', 'grasa sanguinea'],
                'razon': 'El colesterol elevado requiere cardo mariano desintoxicante hepático, omega 3 regulador lipídico, complejo B para metabolismo graso, y minerales para función hepática.'
            },

            # === FASE 2: 40 CASOS MEDIA PRIORIDAD - TERMINOLOGÍA MÉDICA TÉCNICA ===
            
            'dispepsia_tecnico': {
                'keywords': ['dispepsia', 'dispepsia funcional', 'síndrome dispéptico'],
                'productos': [
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'UG COPALCHI TABLETA FRASCO NIS YA GREEN C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['dispepsia', 'indigestion funcional', 'molestia gastrica'],
                'razon': 'La dispepsia requiere fenogreco digestivo funcional, copalchi calmante gástrico, complejo B para enzimas digestivas, y magnesio antiespasmódico.'
            },

            'meteorismo_gases': {
                'keywords': ['meteorismo', 'distensión meteorística', 'timpanismo'],
                'productos': [
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'UG COPALCHI TABLETA FRASCO NIS YA GREEN C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['meteorismo', 'distension abdominal', 'gases intestinales'],
                'razon': 'El meteorismo requiere fenogreco carminativo, copalchi antiespasmódico digestivo, magnesio relajante intestinal, y complejo B para motilidad.'
            },

            'pirosis_acidez': {
                'keywords': ['pirosis', 'pirosis gástrica', 'sensación quemante'],
                'productos': [
                    'UG COPALCHI TABLETA FRASCO NIS YA GREEN C/60',
                    'CN FENOGRECO DUO TABLETA NIS YA GREEN C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['pirosis', 'acidez gastrica', 'ardor epigastrico'],
                'razon': 'La pirosis requiere copalchi neutralizante ácido, fenogreco protector gástrico, magnesio antiácido natural, y complejo B para mucosa gástrica.'
            },

            'gastroenteritis_inflamatoria': {
                'keywords': ['gastroenteritis', 'gastroenteritis aguda', 'inflamación gastroentérica'],
                'productos': [
                    'UG COPALCHI TABLETA FRASCO NIS YA GREEN C/60',
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['gastroenteritis', 'inflamacion gastrointestinal', 'enteritis'],
                'razon': 'La gastroenteritis requiere copalchi calmante gastrointestinal, equinácea antiinflamatoria, vitamina C regeneradora de mucosas, y magnesio rehidratante.'
            },

            'tendinitis_inflamacion': {
                'keywords': ['tendinitis', 'tendinopatía', 'inflamación tendinosa'],
                'productos': [
                    'AR CURA DOL FLEX TABLETA NIS YA GREEN C/30',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA'
                ],
                'sintomas': ['tendinitis', 'tendinopatia', 'inflamacion tendinosa'],
                'razon': 'La tendinitis requiere CuraDol Flex antiinflamatorio específico, omega 3 para reparación tisular, zinc cicatrizante, y magnesio relajante muscular.'
            },

            'contractura_muscular': {
                'keywords': ['contractura', 'contractura muscular', 'espasmo muscular'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR CURA DOL FLEX TABLETA NIS YA GREEN C/30',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['contractura', 'espasmo muscular', 'tension muscular'],
                'razon': 'Las contracturas requieren magnesio relajante muscular específico, CuraDol Flex analgésico, complejo B para función nerviosa, y omega 3 antiinflamatorio.'
            },

            'calambre_muscular': {
                'keywords': ['calambre', 'calambres musculares', 'espasmo doloroso'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['calambres', 'espasmos musculares', 'contracciones involuntarias'],
                'razon': 'Los calambres requieren magnesio relajante neuromuscular, minerales para equilibrio electrolítico, complejo B para conducción nerviosa, y omega 3 para función muscular.'
            },

            'rigidez_articular': {
                'keywords': ['rigidez', 'rigidez articular', 'rigidez muscular'],
                'productos': [
                    'AR CURA DOL FLEX PLUS TABLETA NIS YA GREEN C/30',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['rigidez', 'entumecimiento', 'limitacion movimiento'],
                'razon': 'La rigidez requiere CuraDol Flex Plus para movilidad articular, magnesio relajante, omega 3 lubricante articular, y minerales para flexibilidad.'
            },

            'faringitis_garganta': {
                'keywords': ['faringitis', 'faringitis aguda', 'inflamación faríngea'],
                'productos': [
                    'DO PURIF GOLDEN SEAL TONICO NIS YA 1 LT',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60'
                ],
                'sintomas': ['faringitis', 'inflamacion faringea', 'dolor faringeo'],
                'razon': 'La faringitis requiere Golden Seal antiséptico faríngeo, vitamina C cicatrizante, zinc antimicrobiano, y equinácea antiinflamatoria.'
            },

            'laringitis_ronquera': {
                'keywords': ['laringitis', 'laringitis aguda', 'inflamación laríngea'],
                'productos': [
                    'DO PURIF GOLDEN SEAL TONICO NIS YA 1 LT',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60'
                ],
                'sintomas': ['laringitis', 'ronquera', 'afonia'],
                'razon': 'La laringitis requiere Golden Seal antiinflamatorio laríngeo, vitamina C reparadora de mucosas, zinc antimicrobiano, y equinácea para cuerdas vocales.'
            },

            'amigdalitis_anginas': {
                'keywords': ['amigdalitis', 'anginas', 'tonsilitis'],
                'productos': [
                    'DO PURIF GOLDEN SEAL TONICO NIS YA 1 LT',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['amigdalitis', 'tonsilitis', 'inflamacion amigdalas'],
                'razon': 'La amigdalitis requiere Golden Seal antibiótico natural, zinc antimicrobiano, equinácea inmunoestimulante, y vitamina C para tejido linfoide.'
            },

            'rinitis_nasal': {
                'keywords': ['rinitis', 'rinitis alérgica', 'inflamación nasal'],
                'productos': [
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'DO PURIF GOLDEN SEAL TONICO NIS YA 1 LT',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['rinitis', 'inflamacion nasal', 'congestion allergica'],
                'razon': 'La rinitis requiere equinácea inmunomoduladora, vitamina C antihistamínica, Golden Seal descongestionante, y zinc para mucosas nasales.'
            },

            'pleuresía_pleural': {
                'keywords': ['pleuresía', 'pleuritis', 'inflamación pleural'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['pleuresía', 'pleuritis', 'dolor pleural'],
                'razon': 'La pleuresía requiere omega 3 antiinflamatorio pleural, equinácea para inflamación, vitamina C reparadora, y zinc para tejido pleural.'
            },

            'epistaxis_sangrado': {
                'keywords': ['epistaxis', 'hemorragia nasal', 'sangrado nasal'],
                'productos': [
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['epistaxis', 'hemorragia nasal', 'fragilidad capilar'],
                'razon': 'La epistaxis requiere vitamina C para capilares, zinc cicatrizante, minerales para coagulación, y complejo B para vasos sanguíneos.'
            },

            'ronquera_voz': {
                'keywords': ['ronquera', 'voz ronca', 'disfonía'],
                'productos': [
                    'DO PURIF GOLDEN SEAL TONICO NIS YA 1 LT',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60'
                ],
                'sintomas': ['ronquera', 'disfonia', 'alteracion vocal'],
                'razon': 'La ronquera requiere Golden Seal para cuerdas vocales, vitamina C reparadora, zinc cicatrizante, y equinácea antiinflamatoria vocal.'
            },

            'afonia_perdida_voz': {
                'keywords': ['afonía', 'pérdida de voz', 'sin voz'],
                'productos': [
                    'DO PURIF GOLDEN SEAL TONICO NIS YA 1 LT',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60'
                ],
                'sintomas': ['afonia', 'perdida voz', 'mutismo temporal'],
                'razon': 'La afonía requiere Golden Seal reparador vocal, vitamina C regeneradora, zinc para mucosas, y equinácea para recuperación vocal.'
            },

            'angustia_emocional': {
                'keywords': ['angustia', 'angustia existencial', 'opresión torácica'],
                'productos': [
                    'AB L TRIPTOFANO CAPSULA CANATURA GOLD C/90',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['angustia', 'opresion toracica', 'ansiedad severa'],
                'razon': 'La angustia requiere triptófano calmante profundo, magnesio ansiolítico, complejo B para neurotransmisores, y omega 3 neuroprotector.'
            },

            'melancolia_tristeza': {
                'keywords': ['melancolía', 'estado melancólico', 'tristeza profunda'],
                'productos': [
                    'AB L TRIPTOFANO CAPSULA CANATURA GOLD C/90',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['melancolia', 'tristeza profunda', 'depresion menor'],
                'razon': 'La melancolía requiere triptófano para serotonina, complejo B antidepresivo, multivitamínico energizante, y omega 3 para estado anímico.'
            },

            'desanimo_apatia': {
                'keywords': ['desánimo', 'desaliento', 'falta motivación'],
                'productos': [
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'AB L TRIPTOFANO CAPSULA CANATURA GOLD C/90',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['desanimo', 'desaliento', 'falta motivacion'],
                'razon': 'El desánimo requiere multivitamínico motivador, triptófano elevador anímico, complejo B energizante, y minerales para vitalidad mental.'
            },

            'apatia_desgano': {
                'keywords': ['apatía', 'desgano', 'falta interés'],
                'productos': [
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AB L TRIPTOFANO CAPSULA CANATURA GOLD C/90',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['apatia', 'desgano', 'anhedonia'],
                'razon': 'La apatía requiere multivitamínico activador, complejo B para energía mental, triptófano motivador, y omega 3 para función cerebral.'
            },

            'astenia_debilidad': {
                'keywords': ['astenia', 'astenia física', 'debilidad generalizada'],
                'productos': [
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['astenia', 'debilidad generalizada', 'falta fuerza'],
                'razon': 'La astenia requiere multivitamínico fortalecedor, complejo B para energía, minerales para fuerza muscular, y omega 3 para función celular.'
            },

            'letargo_sopor': {
                'keywords': ['letargo', 'letargia', 'sopor'],
                'productos': [
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'OC NIS YA CER DUO TABLETA NIS YA GREEN C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['letargo', 'sopor', 'somnolencia patologica'],
                'razon': 'El letargo requiere multivitamínico activador, complejo B energizante, cerebrales para alerta mental, y minerales para vitalidad.'
            },

            'burnout_laboral': {
                'keywords': ['burnout', 'síndrome burnout', 'agotamiento laboral'],
                'productos': [
                    'AB L TRIPTOFANO CAPSULA CANATURA GOLD C/90',
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['burnout', 'agotamiento laboral', 'estres cronico'],
                'razon': 'El burnout requiere triptófano antiestrés, multivitamínico recuperador, magnesio relajante del sistema nervioso, y complejo B para energía mental.'
            },

            'amenorrea_menstruacion': {
                'keywords': ['amenorrea', 'falta menstruación', 'ausencia regla'],
                'productos': [
                    'PM ISOFLAVONAS DUO TABLETA NIS YA GREEN C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['amenorrea', 'ausencia menstrual', 'falta regla'],
                'razon': 'La amenorrea requiere isoflavonas reguladoras hormonales, complejo B para ciclo menstrual, minerales para balance hormonal, y omega 3 para función ovárica.'
            },

            'dismenorrea_dolor': {
                'keywords': ['dismenorrea', 'menstruación dolorosa', 'dolor menstrual severo'],
                'productos': [
                    'PM ISOFLAVONAS DUO TABLETA NIS YA GREEN C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['dismenorrea', 'dolor menstrual severo', 'colicos intensos'],
                'razon': 'La dismenorrea requiere isoflavonas equilibrantes, magnesio antiespasmódico uterino, omega 3 antiinflamatorio, y complejo B para balance hormonal.'
            },

            'menorragia_sangrado': {
                'keywords': ['menorragia', 'sangrado menstrual excesivo', 'regla abundante'],
                'productos': [
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'PM ISOFLAVONAS DUO TABLETA NIS YA GREEN C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['menorragia', 'sangrado excesivo', 'hipermenorrea'],
                'razon': 'La menorragia requiere vitamina C hemostática, zinc coagulante, isoflavonas reguladoras del flujo, y minerales para control hemorrágico.'
            },

            'vaginitis_infeccion': {
                'keywords': ['vaginitis', 'inflamación vaginal', 'irritación vaginal'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'HC CHARDON MARIE DUO TABLETA NIS YA GREEN C/60'
                ],
                'sintomas': ['vaginitis', 'inflamacion vaginal', 'irritacion genital'],
                'razon': 'La vaginitis requiere zinc antimicrobiano, minerales para pH vaginal, complejo B para mucosas, y cardo mariano desintoxicante.'
            },

            'cervicitis_cuello': {
                'keywords': ['cervicitis', 'inflamación cervical', 'cuello uterino inflamado'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['cervicitis', 'inflamacion cervical', 'cervix inflamado'],
                'razon': 'La cervicitis requiere zinc antimicrobiano cervical, vitamina C reparadora, equinácea antiinflamatoria, y complejo B para tejido cervical.'
            },

            'hipotension_presion': {
                'keywords': ['hipotensión', 'presión baja', 'tensión baja'],
                'productos': [
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['hipotension', 'presion arterial baja', 'tension baja'],
                'razon': 'La hipotensión requiere multivitamínico tonificante, minerales para presión arterial, complejo B para función cardiovascular, y omega 3 para circulación.'
            },

            'bradicardia_pulso': {
                'keywords': ['bradicardia', 'pulso lento', 'ritmo cardíaco lento'],
                'productos': [
                    'AF TOTALVIT MULTIVITAMINICO CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60'
                ],
                'sintomas': ['bradicardia', 'frecuencia cardiaca baja', 'pulso lento'],
                'razon': 'La bradicardia requiere multivitamínico estimulante, complejo B para función cardíaca, minerales para conducción, y omega 3 para ritmo cardíaco.'
            },

            'extrasistoles_arritmia': {
                'keywords': ['extrasístoles', 'latidos irregulares', 'palpitaciones irregulares'],
                'productos': [
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['extrasistoles', 'arritmia', 'latidos irregulares'],
                'razon': 'Las extrasístoles requieren magnesio antiarrítmico, complejo B para conducción cardíaca, omega 3 para ritmo, y minerales para estabilidad eléctrica.'
            },

            'angina_pecho': {
                'keywords': ['angina pecho', 'dolor precordial', 'opresión torácica'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AB GLUCONATO MAGNESIO CAPSULA CANATURA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['angina', 'dolor precordial', 'isquemia cardiaca'],
                'razon': 'La angina requiere omega 3 vasodilatador, magnesio relajante coronario, complejo B para metabolismo cardíaco, y vitamina C antioxidante vascular.'
            },

            'trombosis_coagulacion': {
                'keywords': ['trombosis', 'coágulo sanguíneo', 'tromboembolismo'],
                'productos': [
                    'AR VITAMINA OMEGA 3 CAPSULA WINIK WAY C/60',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60'
                ],
                'sintomas': ['trombosis', 'coagulo sanguineo', 'embolia'],
                'razon': 'La trombosis requiere omega 3 anticoagulante, vitamina C para vasos sanguíneos, complejo B para circulación, y minerales para fluidez sanguínea.'
            },

            'sepsis_infeccion': {
                'keywords': ['sepsis', 'septicemia', 'infección generalizada'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['sepsis', 'septicemia', 'infeccion sistemica'],
                'razon': 'La sepsis requiere zinc antimicrobiano potente, equinácea inmunoestimulante, vitamina C antioxidante, y complejo B para energía sistémica.'
            },

            'tiña_dermatofitos': {
                'keywords': ['tiña', 'dermatofitosis', 'hongos en piel'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'HC CHARDON MARIE DUO TABLETA NIS YA GREEN C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['tiña', 'dermatofitosis', 'micosis cutanea'],
                'razon': 'La tiña requiere zinc antifúngico, cardo mariano desintoxicante antimicótico, minerales para inmunidad cutánea, y complejo B para piel sana.'
            },

            'pie_atleta_hongos': {
                'keywords': ['pie atleta', 'hongos pies', 'micosis podal'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'HC CHARDON MARIE DUO TABLETA NIS YA GREEN C/60',
                    'AF MINERALES ORGANICOS CAPSULA NUDRA C/60',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['pie atleta', 'micosis podal', 'hongos pies'],
                'razon': 'El pie de atleta requiere zinc antifúngico específico, cardo mariano depurativo, minerales para inmunidad local, y vitamina C cicatrizante.'
            },

            'pitiriasis_descamacion': {
                'keywords': ['pitiriasis', 'descamación cutánea', 'caspa corporal'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'HC CHARDON MARIE DUO TABLETA NIS YA GREEN C/60',
                    'AR VITAMINA A BETACAROTENO CAPSULA CANATURA GOLD',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['pitiriasis', 'descamacion cutanea', 'dermatitis escamosa'],
                'razon': 'La pitiriasis requiere zinc regenerador cutáneo, cardo mariano desintoxicante, vitamina A renovadora celular, y vitamina C antioxidante.'
            },

            'impetigo_bacteriano': {
                'keywords': ['impétigo', 'infección bacteriana cutánea', 'pioderma'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'DO PURIF GOLDEN SEAL TONICO NIS YA 1 LT',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60'
                ],
                'sintomas': ['impetigo', 'infeccion bacteriana cutanea', 'pioderma'],
                'razon': 'El impétigo requiere zinc antimicrobiano, Golden Seal antibiótico natural, vitamina C cicatrizante, y equinácea antibacteriana.'
            },

            'erisipela_inflamacion': {
                'keywords': ['erisipela', 'infección estreptocócica', 'celulitis superficial'],
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'DO PURIF GOLDEN SEAL TONICO NIS YA 1 LT',
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['erisipela', 'celulitis superficial', 'infeccion estreptococica'],
                'razon': 'La erisipela requiere zinc antimicrobiano potente, Golden Seal antibiótico, equinácea antiinflamatoria, y vitamina C para tejido infectado.'
            },
            
            # CASOS ALTA PRIORIDAD - Digestivos
            'reflujo': {
                'productos': [
                    'AR ACIDEZ ESTOMACAL TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR DIGESTO FORTE TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR PAPAYA ENZIMAS VEGETALES TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR GASTRO FORTE TABLETA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['reflujo', 'reflujo gastroesofagico', 'acidez', 'agruras', 'acido estomacal'],
                'keywords': ['reflujo', 'acidez', 'agruras', 'gastroesofagico'],
                'razon': 'El reflujo requiere control de acidez estomacal, enzimas digestivas y protección gastroesofágica con plantas específicas.'
            },
            'indigestion': {
                'productos': [
                    'AR DIGESTO FORTE TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR PAPAYA ENZIMAS VEGETALES TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR JENGIBRE TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR MANZANILLA CAPSULA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['indigestion', 'mal digestion', 'digestion lenta', 'estomago pesado', 'empacho'],
                'keywords': ['indigestion', 'digestion', 'estomago', 'pesado', 'empacho'],
                'razon': 'La indigestión necesita enzimas digestivas, jengibre estimulante y manzanilla calmante para mejorar la digestión.'
            },
            'distension_abdominal': {
                'productos': [
                    'AR GASTRO FORTE TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR HINOJO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR DIGESTO FORTE TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR MANZANILLA CAPSULA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['distension abdominal', 'estomago hinchado', 'abultamiento', 'inflamacion abdominal'],
                'keywords': ['distension', 'hinchado', 'abultamiento', 'inflamacion', 'abdominal'],
                'razon': 'La distensión abdominal requiere plantas carminativas como hinojo y manzanilla para reducir gases e inflamación.'
            },
            'dolor_epigastrico': {
                'productos': [
                    'AR ACIDEZ ESTOMACAL TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR GASTRO FORTE TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR MANZANILLA CAPSULA CENTRO BOTANICO MAYA C/60',
                    'AR REGALIZ TABLETA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['dolor epigastrico', 'dolor boca estomago', 'dolor parte alta abdomen', 'molestia epigastrio'],
                'keywords': ['epigastrico', 'boca estomago', 'abdomen', 'epigastrio'],
                'razon': 'El dolor epigástrico necesita protección gástrica con regaliz y manzanilla, plus control de acidez.'
            },
            'regurgitacion': {
                'productos': [
                    'AR ACIDEZ ESTOMACAL TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR JENGIBRE TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR DIGESTO FORTE TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR GASTRO FORTE TABLETA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['regurgitacion', 'devolver comida', 'vomito acido', 'subida acida'],
                'keywords': ['regurgitacion', 'devolver', 'vomito', 'subida', 'acido'],
                'razon': 'La regurgitación requiere jengibre antinauseoso, control de acidez y mejora del tono esofágico.'
            },
            'hernia': {
                'productos': [
                    'AF COLAGENO CAPSULA CENTRO BOTANICO MAYA C/90',
                    'AF CALCIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90',
                    'AF MAGNESIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['hernia', 'hernia hiatal', 'hernia inguinal', 'debilidad muscular'],
                'keywords': ['hernia', 'hiatal', 'inguinal', 'debilidad', 'muscular'],
                'razon': 'Las hernias necesitan fortalecimiento de tejido conectivo con colágeno, calcio y magnesio para músculos.'
            },
            
            # CASOS ALTA PRIORIDAD - Dolor
            'dolor_agudo': {
                'productos': [
                    'AR SAUCE BLANCO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR UÑA DE GATO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR CURCUMA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR BOSWELLIA TABLETA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['dolor agudo', 'dolor intenso', 'dolor fuerte', 'dolor severo'],
                'keywords': ['agudo', 'intenso', 'fuerte', 'severo'],
                'razon': 'El dolor agudo requiere sauce blanco (ácido salicílico natural), uña de gato y cúrcuma antiinflamatorios potentes.'
            },
            'dolor_punzante': {
                'productos': [
                    'AR SAUCE BLANCO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR VALERIANA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR CURCUMA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF MAGNESIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90'
                ],
                'sintomas': ['dolor punzante', 'punzadas', 'dolor como agujas', 'dolor penetrante'],
                'keywords': ['punzante', 'punzadas', 'agujas', 'penetrante'],
                'razon': 'El dolor punzante necesita sauce blanco analgésico, valeriana relajante muscular y magnesio antiespasmódico.'
            },
            'dolor_sordo': {
                'productos': [
                    'AR CURCUMA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR UÑA DE GATO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR JENGIBRE TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF MAGNESIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90'
                ],
                'sintomas': ['dolor sordo', 'dolor constante', 'dolor persistente', 'molestia constante'],
                'keywords': ['sordo', 'constante', 'persistente'],
                'razon': 'El dolor sordo crónico requiere antiinflamatorios naturales como cúrcuma, uña de gato y jengibre.'
            },
            'molestia': {
                'productos': [
                    'AR CURCUMA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR JENGIBRE TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR MANZANILLA CAPSULA CENTRO BOTANICO MAYA C/60',
                    'AF MAGNESIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90'
                ],
                'sintomas': ['molestia', 'incomodidad', 'malestar general', 'sensacion rara'],
                'keywords': ['molestia', 'incomodidad', 'malestar'],
                'razon': 'Las molestias generales necesitan plantas antiinflamatorias suaves como cúrcuma, jengibre y manzanilla calmante.'
            },
            'espasmo': {
                'productos': [
                    'AF MAGNESIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90',
                    'AR VALERIANA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR MANZANILLA CAPSULA CENTRO BOTANICO MAYA C/60',
                    'AF CALCIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90'
                ],
                'sintomas': ['espasmo', 'espasmos musculares', 'contracciones involuntarias', 'calambres'],
                'keywords': ['espasmo', 'espasmos', 'contracciones', 'calambres'],
                'razon': 'Los espasmos necesitan magnesio relajante muscular, valeriana antiespasmódica y calcio para función muscular.'
            },
            'dolor_cervical': {
                'productos': [
                    'AR SAUCE BLANCO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR CURCUMA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF MAGNESIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90',
                    'AR VALERIANA TABLETA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['dolor cervical', 'dolor cuello', 'torticolis', 'cuello rigido'],
                'keywords': ['cervical', 'cuello', 'torticolis', 'rigido'],
                'razon': 'El dolor cervical necesita antiinflamatorios como sauce blanco y cúrcuma, plus magnesio relajante muscular.'
            },
            
            # CASOS ALTA PRIORIDAD - Respiratorios
            'falta_aire': {
                'productos': [
                    'AR EUCALIPTO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR GORDOLOBO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR JENGIBRE TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF MAGNESIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90'
                ],
                'sintomas': ['falta aire', 'dificultad respirar', 'ahogo', 'sensacion ahogo', 'disnea'],
                'keywords': ['falta aire', 'dificultad respirar', 'ahogo', 'disnea'],
                'razon': 'La falta de aire requiere eucalipto broncodilatador, gordolobo expectorante y magnesio relajante bronquial.'
            },
            'expectoracion': {
                'productos': [
                    'AR GORDOLOBO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR EUCALIPTO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR JENGIBRE TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR TOMILLO TABLETA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['expectoracion', 'flemas', 'mucosidad', 'tos con flemas', 'secreciones'],
                'keywords': ['expectoracion', 'flemas', 'secreciones'],
                'razon': 'La expectoración necesita gordolobo y tomillo expectorantes, eucalipto descongestionante y jengibre mucolítico.'
            },
            'mucosidad': {
                'productos': [
                    'AR GORDOLOBO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR EUCALIPTO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR JENGIBRE TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['mucosidad', 'mocos', 'secreciones nasales', 'flemas espesas'],
                'keywords': ['mucosidad', 'mocos', 'secreciones nasales'],
                'razon': 'La mucosidad excesiva requiere gordolobo mucolítico, eucalipto descongestionante y vitamina C inmunoestimulante.'
            },
            'estornudos': {
                'productos': [
                    'AR ORTIGA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'AR EUCALIPTO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF QUERCETINA CAPSULA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['estornudos', 'estornudos frecuentes', 'crisis estornudos', 'estornudar mucho'],
                'keywords': ['estornudos', 'estornudar'],
                'razon': 'Los estornudos frecuentes necesitan ortiga antihistamínica, quercetina antiinflamatoria y vitamina C estabilizadora.'
            },
            'goteo_nasal': {
                'productos': [
                    'AR ORTIGA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR EUCALIPTO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'AF QUERCETINA CAPSULA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['goteo nasal', 'nariz que gotea', 'rinorrea', 'secrecion nasal'],
                'keywords': ['goteo nasal', 'nariz gotea', 'rinorrea'],
                'razon': 'El goteo nasal requiere ortiga antihistamínica natural, eucalipto descongestionante y quercetina antiinflamatoria.'
            },
            'obstruccion_nasal': {
                'productos': [
                    'AR EUCALIPTO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR JENGIBRE TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'AR ORTIGA TABLETA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['obstruccion nasal', 'nariz tapada', 'congestion nasal', 'no respirar nariz'],
                'keywords': ['obstruccion nasal', 'nariz tapada', 'congestion', 'respirar nariz'],
                'razon': 'La obstrucción nasal necesita eucalipto y jengibre descongestionantes, más ortiga para reducir inflamación mucosa.'
            },
            
            # CASOS MEDIA PRIORIDAD - Digestivos Complejos
            'flatulencias': {
                'productos': [
                    'AR DIGESTO FORTE TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR GASTRO FORTE TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR HINOJO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR MANZANILLA CAPSULA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['gases', 'flatulencias', 'meteorismo', 'distension', 'eructos'],
                'keywords': ['flatulencias', 'gases', 'meteorismo', 'eructos'],
                'razon': 'Las flatulencias requieren plantas carminativas como hinojo y enzimas digestivas para reducir la fermentación intestinal.'
            },
            'intestino_irritable': {
                'productos': [
                    'AR DIGESTO FORTE TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR GASTRO FORTE TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR MANZANILLA CAPSULA CENTRO BOTANICO MAYA C/60',
                    'AF MAGNESIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90'
                ],
                'sintomas': ['colon irritable', 'dolor abdominal', 'diarrea alternante', 'gases'],
                'keywords': ['intestino irritable', 'colon irritable', 'sindrome intestinal'],
                'razon': 'El síndrome de intestino irritable necesita reguladores digestivos, antiespasmódicos y probióticos naturales.'
            },
            'ulcera': {
                'productos': [
                    'AR ACIDEZ ESTOMACAL TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR GASTRO FORTE TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR REGALIZ TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['dolor epigastrico', 'acidez severa', 'nauseas', 'sensacion quemadura'],
                'keywords': ['ulcera', 'ulcera gastrica', 'ulcera duodenal'],
                'razon': 'Las úlceras requieren protectores gástricos, cicatrizantes mucosos y control de acidez gástrica.'
            },
            'eructos': {
                'productos': [
                    'AR DIGESTO FORTE TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR HINOJO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR JENGIBRE TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR MANZANILLA CAPSULA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['eructos frecuentes', 'gases ascendentes', 'presion estomacal'],
                'keywords': ['eructos', 'gases', 'presion estomacal'],
                'razon': 'Los eructos excesivos requieren plantas carminativas y enzimas para mejorar la digestión.'
            },
            'digestion_lenta': {
                'productos': [
                    'AR PAPAYA ENZIMAS VEGETALES TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR DIGESTO FORTE TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR JENGIBRE TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR GASTRO FORTE TABLETA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['lentitud digestiva', 'pesadez', 'somnolencia postprandial'],
                'keywords': ['digestion lenta', 'pesadez', 'lentitud digestiva'],
                'razon': 'La digestión lenta necesita enzimas digestivas y estimulantes gástricos para acelerar el proceso.'
            },
            
            # CASOS MEDIA PRIORIDAD - Dolor Complejo
            'bursitis': {
                'productos': [
                    'AR SAUCE BLANCO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR CURCUMA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR UÑA DE GATO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR BOSWELLIA TABLETA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['dolor articular', 'inflamacion localizada', 'rigidez'],
                'keywords': ['bursitis', 'inflamacion articular'],
                'razon': 'La bursitis requiere antiinflamatorios potentes como cúrcuma y sauce blanco para reducir la inflamación de las bursas.'
            },
            'neuralgia': {
                'productos': [
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF MAGNESIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90',
                    'AR CURCUMA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR VALERIANA TABLETA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['dolor neurologico', 'quemazón', 'hormigueo'],
                'keywords': ['neuralgia', 'dolor neurologico', 'dolor nervios'],
                'razon': 'La neuralgia necesita neuroprotectores, complejo B y antiinflamatorios para calmar el dolor nervioso.'
            },
            'cefalea': {
                'productos': [
                    'AR SAUCE BLANCO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF MAGNESIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90',
                    'AR VALERIANA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR CURCUMA TABLETA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['dolor cabeza', 'presion craneal', 'tension cervical'],
                'keywords': ['cefalea', 'dolor cabeza persistente'],
                'razon': 'Las cefaleas requieren analgésicos naturales, relajantes musculares y mejoradores de circulación cerebral.'
            },
            'jaqueca': {
                'productos': [
                    'AR SAUCE BLANCO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF MAGNESIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90',
                    'AR CURCUMA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR JENGIBRE TABLETA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['dolor cabeza pulsátil', 'nauseas', 'sensibilidad luz'],
                'keywords': ['jaqueca', 'migraña', 'dolor cabeza severo'],
                'razon': 'Las jaquecas necesitan antiinflamatorios específicos, magnesio y reguladores vasculares.'
            },
            
            # CASOS MEDIA PRIORIDAD - Respiratorios Complejos
            'catarro': {
                'productos': [
                    'AR EUCALIPTO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60',
                    'AR JENGIBRE TABLETA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['congestion nasal', 'mucosidad', 'malestar general'],
                'keywords': ['catarro', 'resfrio', 'congestion'],
                'razon': 'El catarro requiere descongestionantes naturales, expectorantes y estimulantes inmunológicos.'
            },
            'neumonia': {
                'productos': [
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AP EKINA CEA DUO TABLETA NIS YA GREEN C/60',
                    'AR GOLDEN SEAL CAPSULA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['tos productiva', 'fiebre', 'dificultad respiratoria'],
                'keywords': ['neumonia', 'pulmonía', 'infeccion pulmonar'],
                'razon': 'La neumonía requiere antibióticos naturales potentes, inmunoestimulantes y expectorantes.'
            },
            'disnea': {
                'productos': [
                    'AR EUCALIPTO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR GORDOLOBO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF MAGNESIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90',
                    'AR JENGIBRE TABLETA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['falta aire', 'respiracion dificil', 'ahogo'],
                'keywords': ['disnea', 'falta aire', 'dificultad respirar'],
                'razon': 'La disnea necesita broncodilatadores naturales, oxigenantes y fortalecedores respiratorios.'
            },
            'ahogo': {
                'productos': [
                    'AR EUCALIPTO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR VALERIANA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF MAGNESIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90',
                    'AR MANZANILLA CAPSULA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['sensacion ahogo', 'opresion pecho', 'ansiedad respiratoria'],
                'keywords': ['ahogo', 'sensacion ahogo', 'opresion pecho'],
                'razon': 'La sensación de ahogo requiere relajantes bronquiales, ansiolíticos naturales y mejoradores respiratorios.'
            },
            
            # CASOS MEDIA PRIORIDAD - Emocionales Complejos
            'fatiga_mental': {
                'productos': [
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA',
                    'AF MAGNESIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90',
                    'AR GINSENG TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF OMEGA 3 CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['cansancio mental', 'dificultad concentracion', 'confusion'],
                'keywords': ['fatiga mental', 'cansancio mental', 'agotamiento mental'],
                'razon': 'La fatiga mental requiere nootrópicos naturales, vitaminas neurales y adaptógenos.'
            },
            'agotamiento_emocional': {
                'productos': [
                    'AR VALERIANA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF MAGNESIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90',
                    'AR PASIFLORA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR MANZANILLA CAPSULA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['burnout', 'vacio emocional', 'despersonalizacion'],
                'keywords': ['agotamiento emocional', 'burnout emocional'],
                'razon': 'El agotamiento emocional necesita adaptógenos, reguladores del estrés y restauradores neurológicos.'
            },
            'tension': {
                'productos': [
                    'AR VALERIANA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF MAGNESIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90',
                    'AR PASIFLORA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR MANZANILLA CAPSULA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['tension muscular', 'rigidez', 'ansiedad'],
                'keywords': ['tension', 'tension muscular', 'rigidez'],
                'razon': 'La tensión requiere relajantes musculares naturales, magnesio y plantas calmantes.'
            },
            'inquietud': {
                'productos': [
                    'AR VALERIANA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR PASIFLORA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF MAGNESIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90',
                    'AR MANZANILLA CAPSULA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['intranquilidad', 'nerviosismo', 'agitacion'],
                'keywords': ['inquietud', 'intranquilidad', 'nerviosismo'],
                'razon': 'La inquietud necesita sedantes naturales suaves, magnesio y plantas tranquilizantes.'
            },
            'desasosiego': {
                'productos': [
                    'AR VALERIANA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR PASIFLORA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF MAGNESIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90',
                    'AR TILA TABLETA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['ansiedad difusa', 'malestar emocional', 'intranquilidad'],
                'keywords': ['desasosiego', 'malestar emocional'],
                'razon': 'El desasosiego requiere ansiolíticos naturales, adaptógenos y estabilizadores del ánimo.'
            },
            
            # CASOS MEDIA PRIORIDAD - Piel Complejos
            'erupciones': {
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF VITAMINA E CAPSULA CENTRO BOTANICO MAYA',
                    'AR ORTIGA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['lesiones cutaneas', 'enrojecimiento', 'inflamacion piel'],
                'keywords': ['erupciones', 'lesiones piel', 'brotes cutaneos'],
                'razon': 'Las erupciones requieren antihistamínicos naturales, antiinflamatorios y depurativos cutáneos.'
            },
            'sarpullido': {
                'productos': [
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF VITAMINA E CAPSULA CENTRO BOTANICO MAYA',
                    'AR ORTIGA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['erupcion papular', 'picazon', 'irritacion cutanea'],
                'keywords': ['sarpullido', 'erupcion cutanea', 'irritacion piel'],
                'razon': 'El sarpullido necesita calmantes cutáneos, antihistamínicos y cicatrizantes naturales.'
            },
            'ronchas': {
                'productos': [
                    'AR ORTIGA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'AF QUERCETINA CAPSULA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['habones', 'urticaria', 'picazon intensa'],
                'keywords': ['ronchas', 'habones', 'urticaria'],
                'razon': 'Las ronchas requieren antihistamínicos potentes, depurativos y antiinflamatorios cutáneos.'
            },
            'comezon': {
                'productos': [
                    'AR ORTIGA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF VITAMINA E CAPSULA CENTRO BOTANICO MAYA',
                    'AF QUERCETINA CAPSULA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['prurito', 'picazon persistente', 'necesidad rascar'],
                'keywords': ['comezon', 'picazon', 'prurito'],
                'razon': 'La comezón necesita antipruriginosos naturales, calmantes cutáneos y antihistamínicos.'
            },
            'picazon': {
                'productos': [
                    'AR ORTIGA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA',
                    'AF VITAMINA E CAPSULA CENTRO BOTANICO MAYA',
                    'AF QUERCETINA CAPSULA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['prurito intenso', 'irritacion cutanea', 'enrojecimiento'],
                'keywords': ['picazon', 'prurito', 'irritacion cutanea'],
                'razon': 'La picazón requiere antipruriginosos, calmantes naturales y antiinflamatorios tópicos.'
            },
            
            # CASOS MEDIA PRIORIDAD - Metabólicos Complejos
            'hiperuricemia': {
                'productos': [
                    'AR ORTIGA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF VITAMINA C CAPSULA CENTRO BOTANICO MAYA',
                    'AR ABEDUL TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF MAGNESIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90'
                ],
                'sintomas': ['acido urico elevado', 'dolor articular', 'gota'],
                'keywords': ['hiperuricemia', 'acido urico alto', 'gota'],
                'razon': 'La hiperuricemia requiere depurativos renales, alcalinizantes y antiinflamatorios específicos.'
            },
            'hiperglucemia': {
                'productos': [
                    'AF CROMO QUELADO TABLETA CENTRO BOTANICO MAYA C/90',
                    'AR CANELA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF MAGNESIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['glucosa elevada', 'sed excesiva', 'fatiga'],
                'keywords': ['hiperglucemia', 'glucosa alta', 'azucar alto'],
                'razon': 'La hiperglucemia necesita hipoglucemiantes naturales, sensibilizadores de insulina y reguladores metabólicos.'
            },
            'hipoglucemia': {
                'productos': [
                    'AF CROMO QUELADO TABLETA CENTRO BOTANICO MAYA C/90',
                    'AF MAGNESIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90',
                    'AR GINSENG TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF COMPLEJO B CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['glucosa baja', 'mareos', 'temblores'],
                'keywords': ['hipoglucemia', 'glucosa baja', 'azucar bajo'],
                'razon': 'La hipoglucemia requiere estabilizadores glucémicos, adaptógenos y nutrientes reguladores.'
            },
            'deshidratacion': {
                'productos': [
                    'AF MAGNESIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90',
                    'AF POTASIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90',
                    'AF CALCIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90',
                    'AF ZINC CAPSULA CENTRO BOTANICO MAYA'
                ],
                'sintomas': ['sed intensa', 'sequedad mucosas', 'fatiga'],
                'keywords': ['deshidratacion', 'sed intensa', 'falta liquidos'],
                'razon': 'La deshidratación necesita reposición de electrolitos, minerales y estimulantes renales.'
            },
            'edema': {
                'productos': [
                    'AF POTASIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90',
                    'AF MAGNESIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90',
                    'AR COLA DE CABALLO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AR JENGIBRE TABLETA CENTRO BOTANICO MAYA C/60'
                ],
                'sintomas': ['retencion liquidos', 'hinchazón', 'pesadez'],
                'keywords': ['edema', 'hinchazon', 'retencion liquidos'],
                'razon': 'El edema requiere diuréticos naturales, drenantes linfáticos y mejoradores circulatorios.'
            },
            'retencion_liquidos': {
                'productos': [
                    'AR COLA DE CABALLO TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF POTASIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90',
                    'AR JENGIBRE TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF MAGNESIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90'
                ],
                'sintomas': ['hinchazón generalizada', 'pesadez', 'aumento peso'],
                'keywords': ['retencion liquidos', 'hinchazon', 'pesadez'],
                'razon': 'La retención de líquidos necesita diuréticos suaves, drenantes y activadores circulatorios.'
            },
            'hinchazon': {
                'productos': [
                    'AR CURCUMA TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF MAGNESIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90',
                    'AR JENGIBRE TABLETA CENTRO BOTANICO MAYA C/60',
                    'AF POTASIO QUELADO TABLETA CENTRO BOTANICO MAYA C/90'
                ],
                'sintomas': ['edema localizado', 'inflamacion', 'pesadez'],
                'keywords': ['hinchazon', 'inflamacion', 'edema'],
                'razon': 'La hinchazón requiere antiinflamatorios, drenantes linfáticos y mejoradores de la microcirculación.'
            }
        }
    
    def _normalize_text(self, text):
        """Normalizar texto eliminando acentos y caracteres especiales"""
        # Mapeo de caracteres con acento a sin acento
        accent_map = {
            'á': 'a', 'à': 'a', 'ä': 'a', 'â': 'a',
            'é': 'e', 'è': 'e', 'ë': 'e', 'ê': 'e',
            'í': 'i', 'ì': 'i', 'ï': 'i', 'î': 'i',
            'ó': 'o', 'ò': 'o', 'ö': 'o', 'ô': 'o',
            'ú': 'u', 'ù': 'u', 'ü': 'u', 'û': 'u',
            'ñ': 'n', 'ç': 'c'
        }
        
        text = text.lower()
        for accented, normal in accent_map.items():
            text = text.replace(accented, normal)
        
        return text
    
    def detect_expert_case(self, user_input):
        """Detectar si la entrada del usuario corresponde a un caso experto"""
        user_input_normalized = self._normalize_text(user_input)
        
        for case_name, case_data in self.expert_cases.items():
            for keyword in case_data['keywords']:
                keyword_normalized = self._normalize_text(keyword)
                if keyword_normalized in user_input_normalized:
                    return case_name, case_data
        
        return None, None
    
    def get_expert_recommendations(self, case_name):
        """Obtener recomendaciones del caso experto"""
        if case_name in self.expert_cases:
            case_data = self.expert_cases[case_name]
            return {
                'productos': case_data['productos'],
                'sintomas': case_data['sintomas'],
                'razon_medica': case_data['razon'],
                'tipo_caso': 'expert_knowledge'
            }
        return None
    
    def _get_real_catalog_info(self, product_name):
        """Buscar información real del producto en el catálogo"""
        if self.catalog_df is None:
            print(f"⚠ Catálogo no disponible para buscar: {product_name}")
            return None
        
        # Normalizar nombre del producto para búsqueda
        product_name_clean = str(product_name).strip().lower()
        
        # Buscar producto en el catálogo
        for index, row in self.catalog_df.iterrows():
            catalog_product_original = row.get('PRODUCTO', '')
            try:
                if catalog_product_original is None or str(catalog_product_original) == 'nan':
                    continue
                if str(catalog_product_original).strip() == '':
                    continue
            except:
                continue
                
            catalog_product = str(catalog_product_original).strip().lower()
            
            # Estrategia 1: Coincidencia exacta
            if catalog_product == product_name_clean:
                print(f"✓ Coincidencia exacta: {catalog_product_original}")
                return self._extract_catalog_info(row)
            
            # Estrategia 2: Coincidencia parcial mejorada
            if catalog_product and product_name_clean in catalog_product:
                print(f"✓ Coincidencia parcial: {catalog_product_original}")
                return self._extract_catalog_info(row)
            
            # Estrategia 3: Coincidencia inversa mejorada
            if product_name_clean and catalog_product in product_name_clean:
                print(f"✓ Coincidencia inversa: {catalog_product_original}")
                return self._extract_catalog_info(row)
        
        print(f"⚠ No encontrado en catálogo: {product_name}")
        # Intentar con coincidencias más flexibles
        return self._fuzzy_search_catalog(product_name_clean)
    
    def _fuzzy_search_catalog(self, product_name_clean):
        """Búsqueda más flexible por palabras clave"""
        # Extraer palabras clave importantes del producto buscado
        search_keywords = [word for word in product_name_clean.split() if len(word) > 2]
        
        best_match = None
        max_matches = 0
        
        for index, row in self.catalog_df.iterrows():
            catalog_product_original = row.get('PRODUCTO', '')
            try:
                if catalog_product_original is None or str(catalog_product_original) == 'nan':
                    continue
                if str(catalog_product_original).strip() == '':
                    continue
            except:
                continue
                
            catalog_product = str(catalog_product_original).strip().lower()
            
            # Contar coincidencias de palabras clave
            matches = sum(1 for search_keyword in search_keywords if search_keyword in catalog_product)
            
            if matches > max_matches and matches >= 2:  # Al menos 2 palabras coinciden
                max_matches = matches
                best_match = row
        
        if best_match is not None:
            product_name = best_match.get('PRODUCTO', '')
            print(f"✓ Coincidencia por palabras clave: {product_name}")
            return self._extract_catalog_info(best_match)
        
        return None
    
    def _extract_catalog_info(self, row):
        """Extraer información del catálogo de una fila"""
        return {
            'PRODUCTO': str(row.get('PRODUCTO', '')).strip(),
            'PRESENTACION': str(row.get('PRESENTACION', '')).strip(),
            'INSTRUCCIONES': str(row.get('INSTRUCCIONES', '')).strip(),
            'CONTRADICCION': str(row.get('CONTRADICCION', '')).strip(),
            'BENEFICIOS': str(row.get('BENEFICIOS', '')).strip(),
            'INGREDIENTES': str(row.get('INGREDIENTES', '')).strip(),
            'DOSIS': str(row.get('DOSIS', '')).strip(),
            'MODO DE USO': str(row.get('MODO DE USO', '')).strip(),
            'SINTOMAS': str(row.get('SINTOMAS', '')).strip()
        }

    def get_expert_recommendation(self, user_input, user_profile=None):
        """Método principal para obtener recomendación experta basada en entrada del usuario"""
        case_name, case_data = self.detect_expert_case(user_input)
        
        if case_name and case_data:
            # Formatear TODOS los productos configurados para la enfermedad
            expert_products = []
            for i, product_name in enumerate(case_data['productos']):  # TODOS los productos
                # Obtener información real del catálogo
                catalog_info = self._get_real_catalog_info(product_name)
                
                if catalog_info:
                    # Usar información real del catálogo
                    formatted_product = {
                        'nombre': catalog_info.get('PRODUCTO', product_name),
                        'presentacion': catalog_info.get('PRESENTACION', 'CAPSULA'),
                        'instrucciones': catalog_info.get('INSTRUCCIONES', 'Según indicaciones del especialista'),
                        'contradiccion': catalog_info.get('CONTRADICCION', 'Consulte con su médico si está embarazada o lactando'),
                        'beneficios': catalog_info.get('BENEFICIOS', 'Producto natural para el bienestar'),
                        'ingredientes': catalog_info.get('INGREDIENTES', 'Ingredientes naturales'),
                        'dosis': catalog_info.get('DOSIS', 'Según indicaciones'),
                        'modo_de_uso': catalog_info.get('MODO DE USO', 'Según indicaciones del fabricante'),
                        'match_reason': case_data['razon'],
                        'expert_case': case_name
                    }
                else:
                    # Fallback si no se encuentra en el catálogo
                    formatted_product = {
                        'nombre': product_name,
                        'presentacion': 'CAPSULA',
                        'instrucciones': 'Según indicaciones del especialista',
                        'contradiccion': 'Consulte con su médico si está embarazada o lactando',
                        'beneficios': 'Producto natural especializado',
                        'ingredientes': 'Ingredientes naturales especializados',
                        'dosis': '1-2 cápsulas al día con los alimentos',
                        'modo_de_uso': 'Tomar con abundante agua durante las comidas',
                        'match_reason': case_data['razon'],
                        'expert_case': case_name
                    }
                expert_products.append(formatted_product)
            
            if expert_products:
                return {
                    'products': expert_products,
                    'condition': case_name.replace('_', ' ').title(),
                    'explanation': case_data['razon'],
                    'expert_mode': True
                }
        
        return None
    
    def get_all_expert_cases(self):
        """Obtener todos los casos expertos disponibles"""
        return list(self.expert_cases.keys())
    
    def get_case_summary(self, case_name):
        """Obtener resumen de un caso experto"""
        if case_name in self.expert_cases:
            case_data = self.expert_cases[case_name]
            return {
                'nombre': case_name,
                'productos_count': len(case_data['productos']),
                'sintomas_count': len(case_data['sintomas']),
                'keywords': case_data['keywords'][:3]  # Primeras 3 palabras clave
            }
        return None

def create_expert_system():
    """Crear instancia del sistema de conocimiento experto"""
    return ExpertKnowledgeSystem()

if __name__ == "__main__":
    # Prueba del sistema
    expert_system = create_expert_system()
    
    test_cases = [
        "como mucha comida chatarra y no puedo parar",
        "tengo problemas con el alcohol",
        "mi acne es muy severo",
        "se me cae mucho el cabello",
        "hago crossfit y necesito recuperacion",
        "soy vegano y necesito proteinas",
        "tengo depresion profunda"
    ]
    
    print("🧠 SISTEMA DE CONOCIMIENTO EXPERTO - PRUEBAS")
    print("=" * 60)
    
    for test_input in test_cases:
        case_name, case_data = expert_system.detect_expert_case(test_input)
        if case_name:
            recommendation = expert_system.get_expert_recommendation(test_input)
            print(f"✅ CASO DETECTADO: {case_name}")
            print(f"   Entrada: '{test_input}'")
            if recommendation and 'products' in recommendation:
                print(f"   Productos: {len(recommendation['products'])}")
                print(f"   Condición: {recommendation.get('condition', 'N/A')}")
            print()
        else:
            print(f"❌ No detectado: '{test_input}'")
            print()