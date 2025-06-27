# SaludArte - Sistema de Salud Natural con IA

## 🌿 Descripción

SaludArte es una plataforma avanzada de salud natural que utiliza inteligencia artificial para proporcionar recomendaciones personalizadas de productos naturales basados en síntomas y condiciones de salud.

## ✨ Características Principales

- **Detección Múltiple de Síntomas**: Procesa hasta 3 síntomas simultáneos
- **Base de Datos Real**: 324 productos auténticos del catálogo Canatura
- **Interpretación Cultural**: Reconoce 50+ modismos mexicanos
- **Cobertura Médica**: 234 condiciones y síntomas detectables
- **Seguridad Robusta**: Protección XSS implementada
- **Rendimiento Optimizado**: Tiempo de respuesta <20ms
- **Interface Responsive**: Diseño web moderno y adaptable

## 🚀 Instalación

### Requisitos
- Python 3.11+
- PostgreSQL
- pip

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone [tu-repositorio]
cd saludarte
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno**
```bash
export DATABASE_URL="postgresql://user:password@host:port/database"
export SESSION_SECRET="tu-clave-secreta"
export OPENAI_API_KEY="tu-api-key" # Opcional
```

4. **Ejecutar la aplicación**
```bash
python main.py
```

5. **Acceder a la aplicación**
```
http://localhost:5000
```

## 📊 Funcionalidades

### Sistema de IA
- Motor de inteligencia artificial propio
- Detección inteligente de síntomas
- Personalización por perfil de usuario
- Análisis de contraindicaciones
- Sistema de advertencias médicas

### Interface Web
- Formulario de perfil de usuario
- Análisis de síntomas interactivo
- Generación de reportes PDF
- Panel de administración
- API REST completa

### Base de Datos
- 324 productos naturales Canatura
- 36 restricciones alimentarias
- Mapeos de síntomas en español
- Sistema de logging avanzado

## 🔧 Estructura del Proyecto

```
saludarte/
├── main.py                 # Punto de entrada
├── app.py                  # Configuración Flask
├── routes.py              # Rutas de la aplicación
├── models.py              # Modelos de base de datos
├── canatura_ai.py         # Motor de IA principal
├── static/                # Archivos estáticos
├── templates/             # Plantillas HTML
└── data/                  # Archivos de datos
```

## 🧪 Pruebas

El sistema incluye una suite completa de pruebas:

- Pruebas de funcionalidad (125 casos)
- Pruebas de seguridad XSS
- Pruebas de rendimiento
- Validación de datos

```bash
python test_sistema_completo.py
python test_xss_security.py
```

## 📈 Métricas de Rendimiento

- **Tasa de resolución**: 100%
- **Tiempo de respuesta**: <20ms promedio
- **Cobertura médica**: 234 condiciones
- **Detección múltiple**: Hasta 3 síntomas simultáneos
- **Seguridad**: 6/6 pruebas XSS exitosas

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🏥 Uso Médico

**Importante**: Este sistema es una herramienta de apoyo informativo. Siempre consulta con profesionales de la salud para decisiones médicas importantes.

## 🆘 Soporte

Para reportar bugs o solicitar nuevas funcionalidades, crea un issue en GitHub.

---

**Desarrollado con ❤️ para mejorar el acceso a la salud natural**
