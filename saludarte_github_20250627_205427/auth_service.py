#!/usr/bin/env python3
"""
Servicio de Autenticación Simple
Solo para usuario maestro, usuarios regulares acceden directamente
"""
from flask import session, request
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

class AuthService:
    def __init__(self):
        # Credenciales maestro hardcodeadas (cambiar en producción)
        self.master_credentials = {
            'username': 'admin_master',
            'password_hash': generate_password_hash('SaludArte2024!'),
            'email': 'admin@saludarte.com'
        }
        
    def authenticate_master(self, username, password):
        """Autenticar usuario maestro"""
        print(f"DEBUG AUTH: Received username: '{username}'")
        print(f"DEBUG AUTH: Expected username: '{self.master_credentials['username']}'")
        
        # Validación directa para solucionar el problema del hash
        if (username == 'admin_master' and password == 'SaludArte2024!'):
            # Establecer sesión maestro
            session['is_master'] = True
            session['master_username'] = username
            session['master_login_time'] = datetime.utcnow().isoformat()
            session['master_ip'] = request.remote_addr
            print("DEBUG AUTH: Session established successfully")
            return True
        
        print("DEBUG AUTH: Authentication failed")
        return False
    
    def is_master_logged_in(self):
        """Verificar si el usuario maestro está autenticado"""
        return session.get('is_master', False)
    
    def logout_master(self):
        """Cerrar sesión maestro"""
        session.pop('is_master', None)
        session.pop('master_username', None)
        session.pop('master_login_time', None)
        session.pop('master_ip', None)
    
    def get_master_info(self):
        """Obtener información del usuario maestro"""
        if self.is_master_logged_in():
            return {
                'username': session.get('master_username'),
                'login_time': session.get('master_login_time'),
                'ip_address': session.get('master_ip')
            }
        return None
    
    def log_master_action(self, action, details=None):
        """Registrar acción del usuario maestro"""
        if self.is_master_logged_in():
            log_entry = {
                'timestamp': datetime.utcnow().isoformat(),
                'username': session.get('master_username'),
                'action': action,
                'details': details,
                'ip_address': request.remote_addr
            }
            
            # Guardar en archivo de log simple
            try:
                with open('master_actions.log', 'a', encoding='utf-8') as f:
                    f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
            except Exception as e:
                print(f"Error logging action: {e}")
    
    def require_master_auth(self, f):
        """Decorador para requerir autenticación maestro"""
        from functools import wraps
        
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not self.is_master_logged_in():
                from flask import redirect, url_for
                return redirect(url_for('master_login'))
            return f(*args, **kwargs)
        return decorated_function

# Instancia global del servicio
auth_service = AuthService()