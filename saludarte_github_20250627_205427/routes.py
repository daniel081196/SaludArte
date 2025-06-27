from flask import render_template, request, redirect, url_for, session, flash, jsonify, send_file, abort
from werkzeug.utils import secure_filename
import os
import logging
import json
from datetime import datetime
from app import app
from ai_service import AIService
from catalog_service import CatalogService
from pdf_service import PDFService
from sistema_completo_alimentado import crear_sistema_completo
from dietary_restrictions_service import DietaryRestrictionsService
from expert_knowledge_system import ExpertKnowledgeSystem
from auth_service import auth_service
from admin_service import admin_service

# Initialize services
ai_service = AIService()
catalog_service = CatalogService()
pdf_service = PDFService()
canatura_ai = crear_sistema_completo()  # Sistema completo alimentado con 200+ casos
dietary_service = DietaryRestrictionsService()  # Servicio de restricciones alimentarias
expert_system = ExpertKnowledgeSystem()  # Sistema de conocimiento experto

@app.route('/')
def index():
    """Landing page with Hoji introduction"""
    return render_template('index.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """User profile collection page"""
    if request.method == 'POST':
        # Store user profile in session
        session['user_profile'] = {
            'name': request.form.get('name', '').strip(),
            'age': request.form.get('age'),
            'gender': request.form.get('gender'),
            'weight': request.form.get('weight'),
            'diabetes': 'diabetes' in request.form,
            'hypertension': 'hypertension' in request.form,
            'pregnancy': 'pregnancy' in request.form,
            'allergies': request.form.get('allergies', ''),
            'medications': request.form.get('medications', '')
        }
        return redirect(url_for('symptoms'))
    
    return render_template('profile.html')

@app.route('/symptoms', methods=['GET', 'POST'])
def symptoms():
    """Symptom input page"""
    if 'user_profile' not in session:
        flash('Por favor completa tu perfil primero.', 'warning')
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        symptoms_text = request.form.get('symptoms')
        if not symptoms_text:
            flash('Por favor describe tus síntomas.', 'error')
            return render_template('symptoms.html')
        
        session['symptoms'] = symptoms_text
        return redirect(url_for('recommendations'))
    
    return render_template('symptoms.html')

@app.route('/recommendations')
def recommendations():
    """Generate and display product recommendations"""
    if 'user_profile' not in session or 'symptoms' not in session:
        flash('Por favor completa todos los pasos previos.', 'warning')
        return redirect(url_for('profile'))
    
    try:
        # Load catalog
        catalog_data = catalog_service.load_catalog()
        if catalog_data is None:
            flash('Error: No se pudo cargar el catálogo de productos. Por favor contacta al administrador.', 'error')
            return redirect(url_for('symptoms'))
        
        # Get user data from session
        user_profile = session['user_profile']
        symptoms_text = session['symptoms']
        
        # Consultar primero el sistema experto para enfermedades específicas
        expert_recommendation = None
        case_name, case_data = expert_system.detect_expert_case(symptoms_text)
        
        if case_name and case_data:
            # Si el sistema experto detecta una enfermedad específica,
            # usar productos directos del catálogo real
            try:
                from expert_direct_products import get_expert_products_direct, get_expert_explanation
                
                # Obtener el DataFrame del catálogo completo directamente
                import pandas as pd
                try:
                    catalog_df = pd.read_excel('PLANTILLA CATALOGO CON INGREDIENTES.xlsx')
                    app.logger.info(f"Cargando catálogo completo con {len(catalog_df)} productos")
                except Exception as e:
                    app.logger.error(f"Error cargando catálogo: {e}")
                    catalog_df = None
                
                expert_products = get_expert_products_direct(case_name, catalog_df)
                explanation = get_expert_explanation(case_name)
                
                if expert_products:
                    expert_recommendation = {
                        'products': expert_products,
                        'condition': case_name.replace('_', ' ').title(),
                        'explanation': explanation,
                        'expert_mode': True
                    }
                    app.logger.info(f"Expert system found {len(expert_products)} products for {case_name}")
                else:
                    app.logger.warning(f"No products found for expert case: {case_name}")
                
            except Exception as expert_error:
                app.logger.warning(f"Expert system error: {expert_error}")
                expert_recommendation = None
        
        if expert_recommendation and expert_recommendation.get('products'):
            # Formatear productos del sistema experto para el template
            expert_products = expert_recommendation['products']
            recommendations = [{
                'symptom': expert_recommendation.get('condition', 'Condición Específica'),
                'products': expert_products,
                'message': f"Sugerencia especializada: {expert_recommendation.get('explanation', '')}"
            }]
            ultra_result = {
                'recommendations': recommendations,
                'expert_mode': True,
                'condition': expert_recommendation.get('condition', ''),
                'explanation': expert_recommendation.get('explanation', '')
            }
            app.logger.info(f"Using expert system with {len(expert_products)} products for {expert_recommendation.get('condition')}")
        else:
            # Usar el sistema completo alimentado con 200+ casos resueltos
            try:
                # Análisis completo con conocimiento especializado
                result = canatura_ai.find_products_for_symptoms_completo(
                    symptoms_text, 
                    user_profile
                )
                
                if result and len(result) > 0:
                    primer_resultado = result[0]
                    products = primer_resultado.get('products', [])
                    
                    # Formatear para compatibilidad con template existente
                    recommendations = []
                    for product in products:
                        recommendations.append({
                            'symptom': symptoms_text,
                            'products': [product],
                            'confidence': 0.95
                        })
                    
                    ultra_result = {
                        'recommendations': recommendations,
                        'sistema_completo': True,
                        'tipo_respuesta': primer_resultado.get('tipo_respuesta', 'completo'),
                        'condicion_detectada': primer_resultado.get('condicion_detectada', ''),
                        'conocimiento_especializado': primer_resultado.get('conocimiento_especializado', {}),
                        'modismo_detectado': primer_resultado.get('modismo_detectado', {}),
                        'medicina_personalizada': primer_resultado.get('medicina_personalizada_aplicada', {}),
                        'estadisticas': primer_resultado.get('estadisticas_sistema', {})
                    }
                else:
                    raise Exception("No se obtuvieron resultados del sistema completo")
                    
            except Exception as complete_error:
                # Fallback al método básico si hay errores
                app.logger.warning(f"Sistema completo error, usando fallback: {complete_error}")
                recommendations = canatura_ai.find_products_for_symptoms(
                    symptoms_text, 
                    user_profile, 
                    min_per_symptom=2, 
                    max_per_symptom=2
                )
                ultra_result = {
                    'recommendations': recommendations,
                    'fallback_mode': True,
                    'error': str(complete_error)
                }
        
        # Obtener restricciones alimentarias según síntomas detectados
        detected_symptoms = [rec['symptom'] for rec in recommendations]
        dietary_advice = dietary_service.get_dietary_recommendations(detected_symptoms, user_profile)
        
        # Store recommendations and ultra results in session for PDF generation
        session['recommendations'] = recommendations
        session['dietary_advice'] = dietary_advice
        session['symptoms_analyzed'] = symptoms_text
        session['ultra_result'] = ultra_result
        
        return render_template('recommendations_simple.html', 
                             recommendations=recommendations,
                             dietary_advice=dietary_advice,
                             user_profile=user_profile,
                             symptoms_text=symptoms_text,
                             ultra_result=ultra_result)
    
    except Exception as e:
        logging.error(f"Error generating recommendations: {str(e)}")
        flash('Ocurrió un error al generar las recomendaciones. Por favor intenta nuevamente.', 'error')
        return redirect(url_for('symptoms'))

@app.route('/download_pdf')
def download_pdf():
    """Generate and download PDF prescription"""
    if 'recommendations' not in session:
        flash('No hay recomendaciones para descargar.', 'error')
        return redirect(url_for('index'))
    
    try:
        # Generate PDF
        pdf_path = pdf_service.generate_prescription_pdf(
            session['user_profile'],
            session['symptoms'],
            session['recommendations']
        )
        
        return send_file(pdf_path, as_attachment=True, download_name='receta_saludarte.pdf')
    
    except Exception as e:
        logging.error(f"Error generating PDF: {str(e)}")
        flash('Error al generar el PDF. Por favor intenta nuevamente.', 'error')
        return redirect(url_for('recommendations'))



@app.route('/reset')
def reset():
    """Reset user session"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/download-system')
def download_system():
    """Download complete SaludArte system"""
    try:
        return send_file(
            'static/downloads/saludarte_sistema_completo.tar.gz',
            as_attachment=True,
            download_name='saludarte_sistema_completo.tar.gz',
            mimetype='application/gzip'
        )
    except FileNotFoundError:
        return "Archivo no encontrado", 404

@app.route('/test-selection')
def test_selection():
    """Test page for selection buttons"""
    return render_template('selection_test.html')

@app.route('/download_custom_pdf', methods=['POST'])
def download_custom_pdf():
    """Generate and download custom PDF with only selected products"""
    try:
        # Get selected products from form data
        selected_products_json = request.form.get('selected_products')
        if not selected_products_json:
            flash('No se han seleccionado productos para el PDF.', 'warning')
            return redirect(url_for('recommendations'))
        
        selected_products = json.loads(selected_products_json)
        
        # Get user profile and symptoms from session
        user_profile = session.get('user_profile', {})
        symptoms_text = session.get('symptoms_text', '')
        
        if not user_profile:
            flash('Información de perfil no encontrada. Por favor, complete el perfil nuevamente.', 'error')
            return redirect(url_for('profile'))
        
        # Convert selected products to the format expected by PDFService
        custom_recommendations = []
        for symptom, products in selected_products.items():
            recommendation = {
                'symptom': symptom,
                'message': f'Productos seleccionados para {symptom}',
                'products': products
            }
            custom_recommendations.append(recommendation)
        
        # Generate custom PDF
        pdf_service = PDFService()
        pdf_path = pdf_service.generate_prescription_pdf(
            user_profile, 
            symptoms_text, 
            custom_recommendations
        )
        
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"receta_personalizada_saludarte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        print(f"Error generating custom PDF: {e}")
        flash('Error al generar el PDF personalizado. Por favor, inténtelo de nuevo.', 'error')
        return redirect(url_for('recommendations'))

# ===== RUTAS DEL SISTEMA MAESTRO =====

@app.route('/master/login', methods=['GET', 'POST'])
def master_login():
    """Página de login para usuario maestro"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        print(f"DEBUG: Login attempt - Username: '{username}', Password length: {len(password) if password else 0}")
        print(f"DEBUG: Expected username: 'admin_master'")
        print(f"DEBUG: Username match: {username == 'admin_master'}")
        
        if auth_service.authenticate_master(username, password):
            auth_service.log_master_action('login', 'Acceso exitoso al panel maestro')
            return redirect(url_for('master_dashboard'))
        else:
            auth_service.log_master_action('login_failed', f'Intento fallido con usuario: {username}')
            return render_template('master_login.html', error='Credenciales incorrectas')
    
    return render_template('master_login.html')

@app.route('/master/logout')
def master_logout():
    """Cerrar sesión maestro"""
    if auth_service.is_master_logged_in():
        auth_service.log_master_action('logout', 'Sesión cerrada')
        auth_service.logout_master()
    return redirect(url_for('index'))

@app.route('/master/dashboard')
@auth_service.require_master_auth
def master_dashboard():
    """Panel principal de administración maestro"""
    auth_service.log_master_action('dashboard_access', 'Acceso al panel principal')
    
    # Obtener estadísticas del sistema
    stats = admin_service.get_system_statistics()
    master_info = auth_service.get_master_info()
    
    return render_template('master_dashboard_simple.html', 
                         stats=stats, 
                         master_info=master_info)

# ===== APIs DEL SISTEMA MAESTRO =====

@app.route('/master/api/products')
@auth_service.require_master_auth
def api_get_products():
    """API: Obtener todos los productos del catálogo"""
    products = admin_service.load_catalog()
    return jsonify(products)

@app.route('/master/api/products/search')
@auth_service.require_master_auth
def api_search_products():
    """API: Buscar productos"""
    query = request.args.get('q', '')
    filters = {
        'categoria': request.args.get('category', ''),
        'presentacion': request.args.get('presentation', '')
    }
    
    # Limpiar filtros vacíos
    filters = {k: v for k, v in filters.items() if v}
    
    products = admin_service.search_products(query, filters)
    return jsonify(products)

@app.route('/master/api/products/filter')
@auth_service.require_master_auth
def api_filter_products():
    """API: Filtrar productos por categoría"""
    category = request.args.get('category', '')
    filters = {'categoria': category} if category else None
    
    products = admin_service.search_products('', filters)
    return jsonify(products)

@app.route('/master/api/products/add', methods=['POST'])
@auth_service.require_master_auth
def api_add_product():
    """API: Agregar nuevo producto"""
    product_data = request.get_json()
    
    if not product_data or not product_data.get('PRODUCTO'):
        return jsonify({'error': 'Datos de producto inválidos'}), 400
    
    result = admin_service.add_product(product_data)
    auth_service.log_master_action('product_add', f"Producto agregado: {product_data.get('PRODUCTO')}")
    
    return jsonify(result)

@app.route('/master/api/products/delete/<int:index>', methods=['DELETE'])
@auth_service.require_master_auth
def api_delete_product(index):
    """API: Eliminar producto"""
    result = admin_service.delete_product(index)
    auth_service.log_master_action('product_delete', f"Producto eliminado en índice: {index}")
    
    return jsonify(result)

@app.route('/master/api/movements')
@auth_service.require_master_auth
def api_get_movements():
    """API: Obtener movimientos de productos"""
    days = request.args.get('days', 30, type=int)
    limit = request.args.get('limit', 100, type=int)
    
    movements = admin_service.get_product_movements(days, limit)
    return jsonify(movements)

@app.route('/master/api/unresolved')
@auth_service.require_master_auth
def api_get_unresolved():
    """API: Obtener casos sin resolver"""
    status = request.args.get('status', 'all')
    
    cases = admin_service.get_unresolved_cases(status)
    return jsonify(cases)

@app.route('/master/api/unresolved/<case_id>/resolve', methods=['POST'])
@auth_service.require_master_auth
def api_resolve_case(case_id):
    """API: Marcar caso como resuelto"""
    result = admin_service.update_unresolved_case(case_id, status='resolved')
    auth_service.log_master_action('case_resolve', f"Caso resuelto: {case_id}")
    
    return jsonify(result)

@app.route('/master/api/unresolved/<case_id>/notes', methods=['POST'])
@auth_service.require_master_auth
def api_add_case_notes(case_id):
    """API: Agregar notas a caso"""
    data = request.get_json()
    notes = data.get('notes', '') if data else ''
    
    if not notes:
        return jsonify({'error': 'Notas requeridas'}), 400
    
    result = admin_service.update_unresolved_case(case_id, notes=notes)
    auth_service.log_master_action('case_notes', f"Notas agregadas a caso: {case_id}")
    
    return jsonify(result)

@app.route('/master/api/stats')
@auth_service.require_master_auth
def api_get_stats():
    """API: Obtener estadísticas del sistema"""
    stats = admin_service.get_system_statistics()
    return jsonify(stats)

@app.route('/master/api/analytics')
@auth_service.require_master_auth
def api_get_analytics():
    """API: Obtener análisis detallado de uso"""
    days = request.args.get('days', 30, type=int)
    analytics = admin_service.get_usage_analytics(days)
    return jsonify(analytics)

@app.route('/master/api/problem-analysis')
@auth_service.require_master_auth
def api_get_problem_analysis():
    """API: Obtener análisis de problemas sin resolver"""
    analysis = admin_service.get_problem_analysis()
    return jsonify(analysis)

@app.route('/master/upload_catalog', methods=['POST'])
@auth_service.require_master_auth
def master_upload_catalog():
    """API: Subir nuevo catálogo (solo acceso maestro)"""
    if 'catalog_file' not in request.files:
        return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
    
    file = request.files['catalog_file']
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
    
    if file and file.filename.endswith('.xlsx'):
        filename = secure_filename(file.filename)
        filepath = os.path.join('uploads', 'catalog_updated.xlsx')
        
        # Crear directorio si no existe
        os.makedirs('uploads', exist_ok=True)
        file.save(filepath)
        
        # Validar estructura del catálogo
        try:
            import pandas as pd
            df = pd.read_excel(filepath)
            
            # Verificar columnas requeridas
            required_columns = ['PRODUCTO', 'SINTOMAS', 'BENEFICIOS', 'PRESENTACION']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return jsonify({'error': f'Faltan columnas requeridas: {", ".join(missing_columns)}'}), 400
            
            # Si la validación es exitosa, reemplazar el catálogo principal
            import shutil
            shutil.copy(filepath, 'PLANTILLA CATALOGO CON INGREDIENTES.xlsx')
            
            auth_service.log_master_action('catalog_upload', f'Catálogo actualizado: {filename}')
            
            return jsonify({'success': True, 'message': 'Catálogo actualizado exitosamente'})
            
        except Exception as e:
            return jsonify({'error': f'Error validando catálogo: {str(e)}'}), 400
    else:
        return jsonify({'error': 'Por favor sube un archivo Excel (.xlsx)'}), 400

# ===== INTEGRACIÓN CON SISTEMA PRINCIPAL =====

def log_user_recommendation(symptoms, products):
    """Registrar recomendación de usuario en el sistema maestro"""
    try:
        session_id = session.get('session_id', 'unknown')
        product_names = [p.get('name', 'Producto desconocido') for p in products]
        admin_service.log_recommendation(symptoms, product_names, session_id)
    except Exception as e:
        logging.error(f"Error logging recommendation: {e}")

def log_unresolved_case(symptoms):
    """Registrar caso sin resolver en el sistema maestro"""
    try:
        session_id = session.get('session_id', 'unknown')
        admin_service.add_unresolved_case(symptoms, session_id, 'Caso generado automáticamente')
    except Exception as e:
        logging.error(f"Error logging unresolved case: {e}")

@app.route('/security-test')
def security_test():
    """Security test page for XSS vulnerability verification"""
    return send_file('test_notification_security.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logging.error(f"Internal server error: {str(error)}")
    return render_template('index.html'), 500


