from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
import os

def generate_event_report(output_filename, event_data):
    """
    Generate a PDF report for a college event.
    
    Args:
        output_filename (str): Name of the output PDF file
        event_data (dict): Dictionary containing event information
    """
    
    # Create the PDF document
    doc = SimpleDocTemplate(output_filename, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)
    
    # Story will hold all the elements to be added to the PDF
    story = []
    
    # Get sample styles
    styles = getSampleStyleSheet()
    
    # Add custom styles
    styles.add(ParagraphStyle(name='Title', 
                             fontSize=18, 
                             leading=22, 
                             alignment=1,  # center alignment
                             spaceAfter=20))
    
    styles.add(ParagraphStyle(name='Subtitle', 
                             fontSize=14, 
                             leading=18, 
                             alignment=1,  # center alignment
                             spaceAfter=15))
    
    styles.add(ParagraphStyle(name='Heading', 
                             fontSize=12, 
                             leading=15, 
                             alignment=0,  # left alignment
                             spaceBefore=15,
                             spaceAfter=10,
                             textColor=colors.darkblue))
    
    styles.add(ParagraphStyle(name='Normal_Center', 
                             parent=styles['Normal'],
                             alignment=1))  # center alignment
    
    # Add college logo if available
    if 'college_logo' in event_data and os.path.exists(event_data['college_logo']):
        logo = Image(event_data['college_logo'], width=2*inch, height=2*inch)
        logo.hAlign = 'CENTER'
        story.append(logo)
        story.append(Spacer(1, 0.25*inch))
    
    # Add title
    title = Paragraph(event_data['event_name'], styles['Title'])
    story.append(title)
    
    # Add subtitle
    subtitle = Paragraph(event_data['college_name'], styles['Subtitle'])
    story.append(subtitle)
    
    # Add date
    date_str = f"<b>Date:</b> {event_data['event_date']}"
    date_para = Paragraph(date_str, styles['Normal_Center'])
    story.append(date_para)
    
    # Add organizer
    organizer_str = f"<b>Organized by:</b> {event_data['organizer']}"
    organizer_para = Paragraph(organizer_str, styles['Normal_Center'])
    story.append(organizer_para)
    story.append(Spacer(1, 0.5*inch))
    
    # Add event details section
    details_title = Paragraph("Event Details", styles['Heading'])
    story.append(details_title)
    
    details_content = event_data['event_description']
    details_para = Paragraph(details_content, styles['Normal'])
    story.append(details_para)
    story.append(Spacer(1, 0.25*inch))
    
    # Add schedule table if available
    if 'schedule' in event_data:
        schedule_title = Paragraph("Event Schedule", styles['Heading'])
        story.append(schedule_title)
        
        # Prepare table data
        table_data = [['Time', 'Activity', 'Speaker/Incharge']]
        for item in event_data['schedule']:
            table_data.append([item['time'], item['activity'], item.get('speaker', '')])
        
        # Create table
        table = Table(table_data, colWidths=[1.5*inch, 3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(table)
        story.append(Spacer(1, 0.5*inch))
    
    # Add participants section if available
    if 'participants' in event_data:
        participants_title = Paragraph("Participants", styles['Heading'])
        story.append(participants_title)
        
        participants_content = f"Total Participants: {event_data['participant_count']}<br/><br/>"
        participants_content += "<b>Participating Departments:</b> " + ", ".join(event_data['participants']['departments'])
        participants_para = Paragraph(participants_content, styles['Normal'])
        story.append(participants_para)
        story.append(Spacer(1, 0.25*inch))
    
    # Add outcomes section if available
    if 'outcomes' in event_data:
        outcomes_title = Paragraph("Key Outcomes", styles['Heading'])
        story.append(outcomes_title)
        
        outcomes_content = ""
        for outcome in event_data['outcomes']:
            outcomes_content += f"• {outcome}<br/>"
        outcomes_para = Paragraph(outcomes_content, styles['Normal'])
        story.append(outcomes_para)
        story.append(Spacer(1, 0.25*inch))
    
    # Add footer
    footer_text = f"Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    footer = Paragraph(footer_text, styles['Normal_Center'])
    story.append(Spacer(1, 0.5*inch))
    story.append(footer)
    
    # Build the PDF
    doc.build(story)

