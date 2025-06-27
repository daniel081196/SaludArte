import os
import logging
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

class PDFService:
    def __init__(self):
        # Ensure temp directory exists
        self.temp_dir = 'temp'
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def generate_prescription_pdf(self, user_profile, symptoms, recommendations):
        """Generate a medical-style prescription PDF"""
        try:
            filename = f"receta_saludarte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = os.path.join(self.temp_dir, filename)
            
            # Create PDF document
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=inch,
                leftMargin=inch,
                topMargin=inch,
                bottomMargin=inch
            )
            
            # Build the story (content)
            story = []
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=TA_CENTER,
                textColor=colors.Color(0.2, 0.6, 0.3)  # Canatura green
            )
            
            header_style = ParagraphStyle(
                'CustomHeader',
                parent=styles['Heading2'],
                fontSize=16,
                spaceAfter=12,
                textColor=colors.Color(0.1, 0.4, 0.2)  # Dark green
            )
            
            # Header
            story.append(Paragraph("SaludArte App", title_style))
            story.append(Paragraph("Asistente Digital de Salud Natural - Canatura", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Patient information
            story.append(Paragraph("INFORMACIÓN DEL PACIENTE", header_style))
            patient_data = [
                ['Nombre:', user_profile.get('name', 'No especificado')],
                ['Edad:', f"{user_profile.get('age', 'No especificada')} años"],
                ['Género:', user_profile.get('gender', 'No especificado').title()],
                ['Peso:', f"{user_profile.get('weight', 'No especificado')} kg" if user_profile.get('weight') else 'No especificado'],
                ['Fecha:', datetime.now().strftime('%d/%m/%Y')]
            ]
            
            # Add health conditions if any
            conditions = []
            if user_profile.get('diabetes'):
                conditions.append('Diabetes')
            if user_profile.get('hypertension'):
                conditions.append('Hipertensión')
            if user_profile.get('pregnancy'):
                conditions.append('Embarazo')
            
            if conditions:
                patient_data.append(['Condiciones:', ', '.join(conditions)])
            
            patient_table = Table(patient_data, colWidths=[2*inch, 4*inch])
            patient_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(patient_table)
            story.append(Spacer(1, 20))
            
            # Symptoms described
            story.append(Paragraph("SÍNTOMAS DESCRITOS", header_style))
            story.append(Paragraph(symptoms, styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Recommendations
            story.append(Paragraph("RECOMENDACIONES NATURALES", header_style))
            
            for i, recommendation in enumerate(recommendations, 1):
                if not recommendation['products']:
                    story.append(Paragraph(f"<b>Síntoma {i}: {recommendation['symptom']}</b>", styles['Normal']))
                    story.append(Paragraph(recommendation['message'], styles['Normal']))
                    story.append(Spacer(1, 10))
                    continue
                
                story.append(Paragraph(f"<b>Para: {recommendation['symptom']}</b>", styles['Normal']))
                
                # Agregar explicación médica si está disponible
                if recommendation.get('message') and 'Sugerencia especializada:' in recommendation['message']:
                    explanation = recommendation['message'].replace('Sugerencia especializada: ', '')
                    explanation_style = ParagraphStyle(
                        'Explanation',
                        parent=styles['Normal'],
                        fontSize=10,
                        textColor=colors.Color(0.1, 0.4, 0.2),
                        leftIndent=20,
                        spaceAfter=10
                    )
                    story.append(Paragraph(f"<b>Justificación médica:</b> {explanation}", explanation_style))
                
                story.append(Spacer(1, 5))
                
                for j, product in enumerate(recommendation['products'], 1):
                    # Product box with proper text wrapping
                    cell_style = ParagraphStyle(
                        'CellText',
                        parent=styles['Normal'],
                        fontSize=9,
                        alignment=TA_LEFT,
                        wordWrap='LTR'
                    )
                    
                    product_data = [
                        [Paragraph(f"<b>PRODUCTO {j}: {product['nombre']}</b>", cell_style), ""],
                        [Paragraph("<b>Beneficios:</b>", cell_style), Paragraph(product['beneficios'], cell_style)],
                        [Paragraph("<b>Ingredientes principales:</b>", cell_style), Paragraph(product['ingredientes'], cell_style)],
                        [Paragraph("<b>Dosis recomendada:</b>", cell_style), Paragraph(product['dosis'], cell_style)],
                        [Paragraph("<b>Modo de uso:</b>", cell_style), Paragraph(product['modo_de_uso'], cell_style)],
                        [Paragraph("<b>Presentación:</b>", cell_style), Paragraph(product['presentacion'], cell_style)],
                    ]
                    
                    if product['contradiccion'] and product['contradiccion'] != 'Sin contraindicaciones conocidas':
                        product_data.append([Paragraph("<b>⚠️ Contraindicaciones:</b>", cell_style), Paragraph(product['contradiccion'], cell_style)])
                    
                    product_table = Table(product_data, colWidths=[2*inch, 4*inch])
                    product_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.9, 0.95, 0.9)),
                        ('FONTSIZE', (0, 0), (-1, -1), 9),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('GRID', (0, 0), (-1, -1), 1, colors.Color(0.8, 0.8, 0.8)),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                        ('TOPPADDING', (0, 0), (-1, -1), 8),
                        ('LEFTPADDING', (0, 0), (-1, -1), 6),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.98, 0.98, 0.98)]),
                    ]))
                    story.append(product_table)
                    story.append(Spacer(1, 10))
                
                story.append(Spacer(1, 15))
            
            # Footer warnings
            story.append(Spacer(1, 20))
            warning_style = ParagraphStyle(
                'Warning',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.red,
                alignment=TA_JUSTIFY
            )
            
            warnings = [
                "⚠️ IMPORTANTE: Esta recomendación es generada por un asistente digital y no reemplaza la consulta médica profesional.",
                "⚠️ Consulte con su médico antes de iniciar cualquier suplemento, especialmente si está tomando medicamentos.",
                "⚠️ Suspenda el uso y consulte a un profesional si experimenta efectos adversos.",
                "⚠️ Los suplementos naturales pueden interactuar con medicamentos convencionales."
            ]
            
            for warning in warnings:
                story.append(Paragraph(warning, warning_style))
                story.append(Spacer(1, 5))
            
            # Footer
            story.append(Spacer(1, 20))
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=8,
                alignment=TA_CENTER,
                textColor=colors.gray
            )
            story.append(Paragraph("SaludArte App - Canatura | Asistente Digital de Salud Natural", footer_style))
            story.append(Paragraph(f"Generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}", footer_style))
            
            # Build PDF
            doc.build(story)
            logging.info(f"PDF generated successfully: {filepath}")
            return filepath
            
        except Exception as e:
            logging.error(f"Error generating PDF: {str(e)}")
            raise
