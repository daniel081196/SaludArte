// JavaScript para el Panel Maestro SaludArte
class MasterDashboard {
    constructor() {
        this.init();
    }

    init() {
        this.loadInitialData();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Búsqueda de productos
        const searchInput = document.getElementById('searchProducts');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.searchProducts(e.target.value);
            });
        }

        // Filtro de categorías
        const categoryFilter = document.getElementById('filterCategory');
        if (categoryFilter) {
            categoryFilter.addEventListener('change', (e) => {
                this.filterByCategory(e.target.value);
            });
        }

        // Formulario agregar producto
        const addProductForm = document.getElementById('addProductForm');
        if (addProductForm) {
            addProductForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.addProduct(new FormData(addProductForm));
            });
        }

        // Formulario subir catálogo
        const uploadCatalogForm = document.getElementById('uploadCatalogForm');
        if (uploadCatalogForm) {
            uploadCatalogForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.uploadCatalog(new FormData(uploadCatalogForm));
            });
        }

        // Pestañas con carga dinámica
        document.querySelectorAll('[data-bs-toggle="pill"]').forEach(tab => {
            tab.addEventListener('shown.bs.tab', (e) => {
                const target = e.target.getAttribute('data-bs-target');
                this.loadTabContent(target);
            });
        });
    }

    async loadInitialData() {
        try {
            // Cargar productos en la pestaña de catálogo
            await this.loadProducts();
        } catch (error) {
            console.error('Error loading initial data:', error);
        }
    }

    async loadTabContent(tabId) {
        switch (tabId) {
            case '#movements':
                await this.loadMovements();
                break;
            case '#unresolved':
                await this.loadUnresolvedCases();
                break;
            case '#catalog':
                await this.loadProducts();
                break;
            case '#analytics':
                await this.loadAdvancedAnalytics();
                break;
        }
    }

    async loadProducts() {
        try {
            const response = await fetch('/master/api/products');
            const products = await response.json();
            
            const tbody = document.querySelector('#productsTable tbody');
            if (!tbody) return;

            tbody.innerHTML = '';
            
            products.forEach((product, index) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>
                        <strong>${product.PRODUCTO || 'Sin nombre'}</strong>
                    </td>
                    <td>
                        <span class="text-truncate d-inline-block" style="max-width: 200px;" 
                              title="${product.SINTOMAS || ''}">
                            ${product.SINTOMAS || 'Sin síntomas definidos'}
                        </span>
                    </td>
                    <td>${product.PRESENTACION || 'No especificada'}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary me-1" 
                                onclick="masterDashboard.editProduct(${index})">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" 
                                onclick="masterDashboard.deleteProduct(${index})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        } catch (error) {
            console.error('Error loading products:', error);
            this.showAlert('Error cargando productos', 'error');
        }
    }

    async loadMovements() {
        try {
            const response = await fetch('/master/api/movements');
            const movements = await response.json();
            
            const tbody = document.getElementById('movementsTable');
            if (!tbody) return;

            tbody.innerHTML = '';
            
            movements.forEach(movement => {
                const row = document.createElement('tr');
                const date = new Date(movement.timestamp).toLocaleString('es-ES');
                
                row.innerHTML = `
                    <td>${date}</td>
                    <td>${movement.product_name || 'N/A'}</td>
                    <td>
                        <span class="badge ${this.getActionBadgeClass(movement.action)}">
                            ${this.translateAction(movement.action)}
                        </span>
                    </td>
                    <td>
                        <span class="text-truncate d-inline-block" style="max-width: 200px;" 
                              title="${movement.symptoms || ''}">
                            ${movement.symptoms || 'N/A'}
                        </span>
                    </td>
                    <td>${movement.user_type || 'Sistema'}</td>
                `;
                tbody.appendChild(row);
            });
        } catch (error) {
            console.error('Error loading movements:', error);
            this.showAlert('Error cargando movimientos', 'error');
        }
    }

    async loadUnresolvedCases() {
        try {
            const response = await fetch('/master/api/unresolved');
            const cases = await response.json();
            
            const tbody = document.getElementById('unresolvedTable');
            if (!tbody) return;

            tbody.innerHTML = '';
            
            cases.forEach(case_ => {
                const row = document.createElement('tr');
                const date = new Date(case_.timestamp).toLocaleString('es-ES');
                
                row.innerHTML = `
                    <td>${date}</td>
                    <td>
                        <span class="text-truncate d-inline-block" style="max-width: 300px;" 
                              title="${case_.symptoms}">
                            ${case_.symptoms}
                        </span>
                    </td>
                    <td>
                        <span class="badge ${this.getStatusBadgeClass(case_.status)}">
                            ${this.translateStatus(case_.status)}
                        </span>
                    </td>
                    <td>${case_.notes || 'Sin notas'}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-success me-1" 
                                onclick="masterDashboard.resolveCase('${case_.id}')">
                            <i class="fas fa-check"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-primary" 
                                onclick="masterDashboard.addNotes('${case_.id}')">
                            <i class="fas fa-sticky-note"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        } catch (error) {
            console.error('Error loading unresolved cases:', error);
            this.showAlert('Error cargando casos sin resolver', 'error');
        }
    }

    async searchProducts(query) {
        try {
            const response = await fetch(`/master/api/products/search?q=${encodeURIComponent(query)}`);
            const products = await response.json();
            
            // Actualizar tabla con resultados filtrados
            this.updateProductsTable(products);
        } catch (error) {
            console.error('Error searching products:', error);
        }
    }

    async filterByCategory(category) {
        try {
            const url = category ? 
                `/master/api/products/filter?category=${encodeURIComponent(category)}` : 
                '/master/api/products';
            
            const response = await fetch(url);
            const products = await response.json();
            
            this.updateProductsTable(products);
        } catch (error) {
            console.error('Error filtering products:', error);
        }
    }

    updateProductsTable(products) {
        const tbody = document.querySelector('#productsTable tbody');
        if (!tbody) return;

        tbody.innerHTML = '';
        
        products.forEach((product, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><strong>${product.PRODUCTO || 'Sin nombre'}</strong></td>
                <td>
                    <span class="text-truncate d-inline-block" style="max-width: 200px;" 
                          title="${product.SINTOMAS || ''}">
                        ${product.SINTOMAS || 'Sin síntomas definidos'}
                    </span>
                </td>
                <td>${product.PRESENTACION || 'No especificada'}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary me-1" 
                            onclick="masterDashboard.editProduct(${index})">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" 
                            onclick="masterDashboard.deleteProduct(${index})">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    async addProduct(formData) {
        try {
            const productData = {};
            for (let [key, value] of formData.entries()) {
                productData[key] = value;
            }

            const response = await fetch('/master/api/products/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(productData)
            });

            const result = await response.json();
            
            if (result.success) {
                this.showAlert('Producto agregado exitosamente', 'success');
                // Cerrar modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('addProductModal'));
                modal.hide();
                // Recargar productos
                await this.loadProducts();
                // Limpiar formulario
                document.getElementById('addProductForm').reset();
            } else {
                this.showAlert(result.error || 'Error agregando producto', 'error');
            }
        } catch (error) {
            console.error('Error adding product:', error);
            this.showAlert('Error agregando producto', 'error');
        }
    }

    async uploadCatalog(formData) {
        try {
            // Mostrar indicador de carga
            const submitBtn = document.querySelector('#uploadCatalogForm button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Subiendo...';
            submitBtn.disabled = true;

            const response = await fetch('/master/upload_catalog', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            
            if (result.success) {
                this.showAlert('Catálogo actualizado exitosamente', 'success');
                // Cerrar modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('uploadCatalogModal'));
                modal.hide();
                // Recargar productos
                await this.loadProducts();
                // Limpiar formulario
                document.getElementById('uploadCatalogForm').reset();
                
                // Mostrar confirmación adicional
                setTimeout(() => {
                    this.showAlert('El sistema se ha actualizado con el nuevo catálogo', 'info');
                }, 2000);
            } else {
                this.showAlert(result.error || 'Error subiendo catálogo', 'error');
            }

            // Restaurar botón
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
            
        } catch (error) {
            console.error('Error uploading catalog:', error);
            this.showAlert('Error subiendo catálogo', 'error');
            
            // Restaurar botón en caso de error
            const submitBtn = document.querySelector('#uploadCatalogForm button[type="submit"]');
            submitBtn.innerHTML = '<i class="fas fa-upload me-2"></i>Subir Catálogo';
            submitBtn.disabled = false;
        }
    }

    async deleteProduct(index) {
        if (!confirm('¿Está seguro de que desea eliminar este producto?')) {
            return;
        }

        try {
            const response = await fetch(`/master/api/products/delete/${index}`, {
                method: 'DELETE'
            });

            const result = await response.json();
            
            if (result.success) {
                this.showAlert('Producto eliminado exitosamente', 'success');
                await this.loadProducts();
            } else {
                this.showAlert(result.error || 'Error eliminando producto', 'error');
            }
        } catch (error) {
            console.error('Error deleting product:', error);
            this.showAlert('Error eliminando producto', 'error');
        }
    }

    async resolveCase(caseId) {
        try {
            const response = await fetch(`/master/api/unresolved/${caseId}/resolve`, {
                method: 'POST'
            });

            const result = await response.json();
            
            if (result.success) {
                this.showAlert('Caso marcado como resuelto', 'success');
                await this.loadUnresolvedCases();
            } else {
                this.showAlert(result.error || 'Error resolviendo caso', 'error');
            }
        } catch (error) {
            console.error('Error resolving case:', error);
            this.showAlert('Error resolviendo caso', 'error');
        }
    }

    async addNotes(caseId) {
        const notes = prompt('Ingrese notas para este caso:');
        if (!notes) return;

        try {
            const response = await fetch(`/master/api/unresolved/${caseId}/notes`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ notes })
            });

            const result = await response.json();
            
            if (result.success) {
                this.showAlert('Notas agregadas exitosamente', 'success');
                await this.loadUnresolvedCases();
            } else {
                this.showAlert(result.error || 'Error agregando notas', 'error');
            }
        } catch (error) {
            console.error('Error adding notes:', error);
            this.showAlert('Error agregando notas', 'error');
        }
    }

    async loadAdvancedAnalytics() {
        try {
            // Cargar análisis de uso
            const analyticsResponse = await fetch('/master/api/analytics');
            const analytics = await analyticsResponse.json();
            
            // Cargar análisis de problemas
            const problemResponse = await fetch('/master/api/problem-analysis');
            const problemAnalysis = await problemResponse.json();
            
            // Actualizar estadísticas principales
            if (analytics.patrones_uso) {
                document.getElementById('totalConsultas').textContent = analytics.patrones_uso.total_consultas || 0;
                document.getElementById('promedioDiario').textContent = (analytics.patrones_uso.promedio_diario || 0).toFixed(1);
            }
            
            // Mostrar productos más recomendados
            this.displayTopProducts(analytics.productos_mas_recomendados || {});
            
            // Mostrar síntomas más consultados
            this.displayTopSymptoms(analytics.sintomas_mas_consultados || {});
            
            // Mostrar análisis de problemas
            this.displayProblemAnalysis(problemAnalysis);
            
        } catch (error) {
            console.error('Error loading advanced analytics:', error);
            this.showAlert('Error cargando análisis avanzado', 'error');
        }
    }

    displayTopProducts(products) {
        const container = document.getElementById('topProducts');
        if (!container) return;
        
        container.innerHTML = '';
        
        const productEntries = Object.entries(products).slice(0, 10);
        if (productEntries.length === 0) {
            container.innerHTML = '<p class="text-muted">No hay datos de productos recomendados aún.</p>';
            return;
        }
        
        productEntries.forEach(([product, count], index) => {
            const percentage = index === 0 ? 100 : (count / productEntries[0][1]) * 100;
            
            const item = document.createElement('div');
            item.className = 'mb-2';
            item.innerHTML = `
                <div class="d-flex justify-content-between mb-1">
                    <span class="text-truncate" style="max-width: 70%;" title="${product}">${product}</span>
                    <span class="badge bg-primary">${count}</span>
                </div>
                <div class="progress" style="height: 8px;">
                    <div class="progress-bar bg-success" role="progressbar" style="width: ${percentage}%"></div>
                </div>
            `;
            container.appendChild(item);
        });
    }

    displayTopSymptoms(symptoms) {
        const container = document.getElementById('topSymptoms');
        if (!container) return;
        
        container.innerHTML = '';
        
        const symptomEntries = Object.entries(symptoms).slice(0, 10);
        if (symptomEntries.length === 0) {
            container.innerHTML = '<p class="text-muted">No hay datos de síntomas consultados aún.</p>';
            return;
        }
        
        symptomEntries.forEach(([symptom, count], index) => {
            const percentage = index === 0 ? 100 : (count / symptomEntries[0][1]) * 100;
            
            const item = document.createElement('div');
            item.className = 'mb-2';
            item.innerHTML = `
                <div class="d-flex justify-content-between mb-1">
                    <span class="text-truncate" style="max-width: 70%;" title="${symptom}">${symptom}</span>
                    <span class="badge bg-info">${count}</span>
                </div>
                <div class="progress" style="height: 8px;">
                    <div class="progress-bar bg-info" role="progressbar" style="width: ${percentage}%"></div>
                </div>
            `;
            container.appendChild(item);
        });
    }

    displayProblemAnalysis(analysis) {
        // Mostrar categorías de problemas
        const categoriesContainer = document.getElementById('problemCategories');
        if (categoriesContainer && analysis.categorias_problemas) {
            categoriesContainer.innerHTML = '';
            
            const categories = Object.entries(analysis.categorias_problemas);
            if (categories.length === 0) {
                categoriesContainer.innerHTML = '<p class="text-muted">No hay casos sin resolver categorizados.</p>';
            } else {
                categories.forEach(([category, count]) => {
                    const item = document.createElement('div');
                    item.className = 'mb-1';
                    item.innerHTML = `
                        <span class="badge bg-warning me-2">${category}</span>
                        <span>${count} caso${count !== 1 ? 's' : ''}</span>
                    `;
                    categoriesContainer.appendChild(item);
                });
            }
        }
        
        // Mostrar recomendaciones de mejora
        const suggestionsContainer = document.getElementById('improvementSuggestions');
        if (suggestionsContainer && analysis.recomendaciones_mejora) {
            suggestionsContainer.innerHTML = '';
            
            if (analysis.recomendaciones_mejora.length === 0) {
                suggestionsContainer.innerHTML = '<li class="text-muted">No hay recomendaciones disponibles.</li>';
            } else {
                analysis.recomendaciones_mejora.forEach(suggestion => {
                    const item = document.createElement('li');
                    item.textContent = suggestion;
                    suggestionsContainer.appendChild(item);
                });
            }
        }
    }

    getActionBadgeClass(action) {
        switch (action) {
            case 'recommended': return 'bg-success';
            case 'added': return 'bg-primary';
            case 'updated': return 'bg-warning';
            case 'deleted': return 'bg-danger';
            default: return 'bg-secondary';
        }
    }

    translateAction(action) {
        const translations = {
            'recommended': 'Recomendado',
            'added': 'Agregado',
            'updated': 'Actualizado',
            'deleted': 'Eliminado',
            'viewed': 'Visto'
        };
        return translations[action] || action;
    }

    getStatusBadgeClass(status) {
        switch (status) {
            case 'pending': return 'bg-warning';
            case 'reviewing': return 'bg-info';
            case 'resolved': return 'bg-success';
            default: return 'bg-secondary';
        }
    }

    translateStatus(status) {
        const translations = {
            'pending': 'Pendiente',
            'reviewing': 'En revisión',
            'resolved': 'Resuelto'
        };
        return translations[status] || status;
    }

    showAlert(message, type = 'info') {
        // Crear alerta temporal
        const alertClass = type === 'error' ? 'alert-danger' : `alert-${type}`;
        const alertHtml = `
            <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        // Buscar un contenedor para la alerta o crearla en el body
        let alertContainer = document.querySelector('.alert-container');
        if (!alertContainer) {
            alertContainer = document.createElement('div');
            alertContainer.className = 'alert-container position-fixed top-0 end-0 p-3';
            alertContainer.style.zIndex = '9999';
            document.body.appendChild(alertContainer);
        }
        
        alertContainer.insertAdjacentHTML('beforeend', alertHtml);
        
        // Auto-remover después de 5 segundos
        setTimeout(() => {
            const alerts = alertContainer.querySelectorAll('.alert');
            if (alerts.length > 0) {
                alerts[0].remove();
            }
        }, 5000);
    }
}

// Inicializar cuando se carga la página
let masterDashboard;
document.addEventListener('DOMContentLoaded', function() {
    masterDashboard = new MasterDashboard();
});