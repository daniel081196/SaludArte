// ===== MAIN JAVASCRIPT FOR SALUDARTE APP =====

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// ===== APP INITIALIZATION =====
function initializeApp() {
    initializeHoji();
    initializeFormValidation();
    initializeAnimations();
    initializeTooltips();
    console.log('SaludArte App initialized successfully');
}

// ===== HOJI MASCOT FUNCTIONALITY =====
function initializeHoji() {
    const hojiContainer = document.getElementById('hojiContainer');
    const hojiMascot = document.getElementById('hojiMascot');
    const hojiBubble = document.getElementById('hojiBubble');
    
    if (!hojiContainer || !hojiMascot || !hojiBubble) {
        return;
    }
    
    // Show bubble on hover
    hojiMascot.addEventListener('mouseenter', function() {
        hojiBubble.classList.add('show');
    });
    
    // Hide bubble when not hovering
    hojiMascot.addEventListener('mouseleave', function() {
        setTimeout(() => {
            if (!hojiBubble.matches(':hover')) {
                hojiBubble.classList.remove('show');
            }
        }, 500);
    });
    
    // Keep bubble visible when hovering over it
    hojiBubble.addEventListener('mouseenter', function() {
        this.classList.add('show');
    });
    
    hojiBubble.addEventListener('mouseleave', function() {
        this.classList.remove('show');
    });
    
    // Auto-show bubble periodically
    setInterval(() => {
        if (!hojiBubble.classList.contains('show')) {
            hojiBubble.classList.add('show');
            setTimeout(() => {
                hojiBubble.classList.remove('show');
            }, 4000);
        }
    }, 15000);
    
    // Animate Hoji on click
    hojiMascot.addEventListener('click', function() {
        const hojiImage = this.querySelector('.hoji-image');
        hojiImage.style.transform = 'scale(1.2) rotate(10deg)';
        setTimeout(() => {
            hojiImage.style.transform = 'scale(1) rotate(0deg)';
        }, 300);
        
        // Show encouraging message
        const encouragingMessages = [
            "Hoji está aquí para ayudarte",
            "Encontraremos la solución natural perfecta",
            "Tu bienestar es mi prioridad",
            "Juntos lograremos que te sientas mejor",
            "Los mejores productos naturales te esperan",
            "Confía en mi experiencia",
            "Tu salud natural está en buenas manos"
        ];
        
        const randomMessage = encouragingMessages[Math.floor(Math.random() * encouragingMessages.length)];
        updateHojiMessage(randomMessage);
    });
}

// Update Hoji's message
function updateHojiMessage(message) {
    const hojiMessage = document.getElementById('hojiMessage');
    if (hojiMessage) {
        hojiMessage.textContent = message;
        const hojiBubble = document.getElementById('hojiBubble');
        if (hojiBubble) {
            hojiBubble.classList.add('show');
            setTimeout(() => {
                hojiBubble.classList.remove('show');
            }, 5000);
        }
    }
}

// ===== FORM VALIDATION =====
function initializeFormValidation() {
    // Age validation
    const ageInput = document.getElementById('age');
    if (ageInput) {
        ageInput.addEventListener('input', function() {
            validateAge(this);
        });
    }
    
    // Weight validation
    const weightInput = document.getElementById('weight');
    if (weightInput) {
        weightInput.addEventListener('input', function() {
            validateWeight(this);
        });
    }
    
    // Symptoms textarea validation
    const symptomsTextarea = document.getElementById('symptoms');
    if (symptomsTextarea) {
        symptomsTextarea.addEventListener('input', function() {
            validateSymptoms(this);
        });
    }
}

function validateAge(input) {
    const age = parseInt(input.value);
    const feedback = getOrCreateFeedback(input);
    
    if (age < 1 || age > 120) {
        input.classList.add('is-invalid');
        feedback.textContent = 'Por favor ingresa una edad válida (1-120 años)';
        feedback.className = 'invalid-feedback';
    } else {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        feedback.textContent = '¡Perfecto!';
        feedback.className = 'valid-feedback';
    }
}

function validateWeight(input) {
    const weight = parseFloat(input.value);
    const feedback = getOrCreateFeedback(input);
    
    if (input.value && (weight < 20 || weight > 300)) {
        input.classList.add('is-invalid');
        feedback.textContent = 'Por favor ingresa un peso válido (20-300 kg)';
        feedback.className = 'invalid-feedback';
    } else if (input.value) {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        feedback.textContent = '¡Perfecto!';
        feedback.className = 'valid-feedback';
    } else {
        input.classList.remove('is-invalid', 'is-valid');
        feedback.textContent = '';
    }
}

function validateSymptoms(textarea) {
    const symptoms = textarea.value.trim();
    const feedback = getOrCreateFeedback(textarea);
    
    if (symptoms.length < 10) {
        textarea.classList.add('is-invalid');
        feedback.textContent = 'Por favor describe tus síntomas con más detalle (mínimo 10 caracteres)';
        feedback.className = 'invalid-feedback';
    } else {
        textarea.classList.remove('is-invalid');
        textarea.classList.add('is-valid');
        feedback.textContent = '¡Excelente descripción!';
        feedback.className = 'valid-feedback';
    }
}

function getOrCreateFeedback(input) {
    let feedback = input.parentNode.querySelector('.invalid-feedback, .valid-feedback');
    if (!feedback) {
        feedback = document.createElement('div');
        input.parentNode.appendChild(feedback);
    }
    return feedback;
}

// ===== ANIMATIONS =====
function initializeAnimations() {
    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);
    
    // Observe cards and sections
    document.querySelectorAll('.card, .process-step, .recommendation-section').forEach(el => {
        observer.observe(el);
    });
    
    // Add stagger animation to product cards
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach((card, index) => {
        setTimeout(() => {
            card.style.animationDelay = `${index * 0.1}s`;
            card.classList.add('slide-in-left');
        }, 100);
    });
}

// ===== TOOLTIPS =====
function initializeTooltips() {
    // Initialize Bootstrap tooltips if available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Add custom tooltips for health condition checkboxes
    const healthConditions = document.querySelectorAll('input[type="checkbox"][name$="diabetes"], input[type="checkbox"][name$="hypertension"], input[type="checkbox"][name$="pregnancy"]');
    healthConditions.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                updateHojiMessage(`Perfecto, tendré en cuenta tu ${this.name} para evitar productos contraindicados.`);
            }
        });
    });
}

// ===== UTILITY FUNCTIONS =====

// Copy to clipboard functionality
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Texto copiado al portapapeles', 'success');
        }).catch(() => {
            fallbackCopyToClipboard(text);
        });
    } else {
        fallbackCopyToClipboard(text);
    }
}

function fallbackCopyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    try {
        document.execCommand('copy');
        showNotification('Texto copiado al portapapeles', 'success');
    } catch (err) {
        showNotification('Error al copiar texto', 'error');
    }
    document.body.removeChild(textArea);
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show notification-toast`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        animation: slideInRight 0.3s ease-out;
    `;
    
    // Use textContent to prevent XSS vulnerabilities
    notification.textContent = message;
    
    // Create and append the close button safely
    const closeButton = document.createElement('button');
    closeButton.type = 'button';
    closeButton.className = 'btn-close';
    closeButton.setAttribute('data-bs-dismiss', 'alert');
    closeButton.setAttribute('aria-label', 'Close');
    notification.appendChild(closeButton);
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Format text for WhatsApp sharing
function formatForWhatsApp(text) {
    return text
        .replace(/\*\*(.*?)\*\*/g, '*$1*') // Bold formatting
        .replace(/__(.*?)__/g, '_$1_')     // Italic formatting
        .replace(/\n{3,}/g, '\n\n');       // Reduce excessive line breaks
}

// Smooth scroll to element
function smoothScrollTo(element) {
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
    }
}

// ===== PAGE-SPECIFIC FUNCTIONALITY =====

// Profile page enhancements
if (window.location.pathname.includes('/profile')) {
    document.addEventListener('DOMContentLoaded', function() {
        // Auto-focus on age input
        const ageInput = document.getElementById('age');
        if (ageInput) {
            setTimeout(() => ageInput.focus(), 500);
        }
        
        // Update Hoji message based on form progress
        const formInputs = document.querySelectorAll('#profileForm input, #profileForm select');
        let completedFields = 0;
        
        formInputs.forEach(input => {
            input.addEventListener('change', function() {
                completedFields = Array.from(formInputs).filter(i => i.value).length;
                const progress = (completedFields / formInputs.length) * 100;
                
                if (progress > 50) {
                    updateHojiMessage('¡Excelente! Ya casi terminamos con tu perfil. Esta información me ayuda mucho.');
                } else if (progress > 25) {
                    updateHojiMessage('¡Muy bien! Sigues completando tu información. Cada detalle es importante.');
                }
            });
        });
    });
}

// Symptoms page enhancements
if (window.location.pathname.includes('/symptoms')) {
    document.addEventListener('DOMContentLoaded', function() {
        // Auto-resize textarea
        const symptomsTextarea = document.getElementById('symptoms');
        if (symptomsTextarea) {
            symptomsTextarea.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = this.scrollHeight + 'px';
            });
            
            // Focus on textarea
            setTimeout(() => symptomsTextarea.focus(), 500);
        }
        
        // Enhanced symptom button functionality
        document.querySelectorAll('.symptom-btn').forEach(button => {
            button.addEventListener('click', function() {
                const symptom = this.dataset.symptom;
                const textarea = document.getElementById('symptoms');
                
                // Add symptom to textarea
                if (textarea.value.trim() === '') {
                    textarea.value = `Tengo ${symptom}`;
                } else {
                    if (!textarea.value.includes(symptom)) {
                        textarea.value += `, ${symptom}`;
                    }
                }
                
                // Trigger input event for validation
                textarea.dispatchEvent(new Event('input'));
                
                // Visual feedback
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = 'scale(1)';
                }, 150);
                
                // Update Hoji
                updateHojiMessage(`Perfecto, agregué "${symptom}" a tus síntomas. ¿Hay algo más que te moleste?`);
            });
        });
    });
}

// Recommendations page enhancements
if (window.location.pathname.includes('/recommendations')) {
    document.addEventListener('DOMContentLoaded', function() {
        // Add print-specific functionality
        window.addEventListener('beforeprint', function() {
            // Hide interactive elements
            document.querySelectorAll('.action-buttons, .hoji-container').forEach(el => {
                el.style.display = 'none';
            });
        });
        
        window.addEventListener('afterprint', function() {
            // Restore interactive elements
            document.querySelectorAll('.action-buttons, .hoji-container').forEach(el => {
                el.style.display = '';
            });
        });
        
        // Enhanced WhatsApp sharing
        window.shareWhatsApp = function() {
            const patientName = 'Paciente'; // Could be enhanced to get actual name
            const symptoms = document.querySelector('.symptoms-box p')?.textContent || '';
            const recommendations = Array.from(document.querySelectorAll('.product-name')).map(el => el.textContent.trim());
            
            let message = `🌿 *Receta Natural de SaludArte App - Canatura*\n\n`;
            message += `👤 *Paciente:* ${patientName}\n`;
            message += `📅 *Fecha:* ${new Date().toLocaleDateString('es-ES')}\n\n`;
            message += `📋 *Síntomas descritos:*\n"${symptoms}"\n\n`;
            
            if (recommendations.length > 0) {
                message += `💊 *Productos recomendados:*\n`;
                recommendations.forEach((product, index) => {
                    message += `${index + 1}. ${product}\n`;
                });
                message += `\n`;
            }
            
            message += `⚠️ *Importante:* Esta recomendación no reemplaza la consulta médica profesional.\n\n`;
            message += `🌱 *Generado por SaludArte App - Canatura*`;
            
            const encodedMessage = encodeURIComponent(message);
            window.open(`https://wa.me/?text=${encodedMessage}`, '_blank');
            
            // Analytics or tracking could be added here
            console.log('WhatsApp sharing initiated');
        };
    });
}

// ===== ERROR HANDLING =====
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    // Could send error to logging service
});

// ===== ACCESSIBILITY ENHANCEMENTS =====
document.addEventListener('keydown', function(e) {
    // Escape key to close modals or overlays
    if (e.key === 'Escape') {
        const hojiBubble = document.getElementById('hojiBubble');
        if (hojiBubble && hojiBubble.classList.contains('show')) {
            hojiBubble.classList.remove('show');
        }
    }
    
    // Enter key on Hoji mascot
    if (e.key === 'Enter' && e.target.closest('.hoji-mascot')) {
        e.target.click();
    }
});

// ===== PERFORMANCE OPTIMIZATIONS =====
// Debounce function for input events
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function for scroll events
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

console.log('SaludArte App JavaScript loaded successfully');
