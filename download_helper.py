# download_helper.py
from flask import send_file
from io import BytesIO
from fpdf import FPDF
from docx import Document

def generate_cover_letter(cover_letter_text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in cover_letter_text.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )

def generate_cover_letter(cover_letter_text, filename):
    doc = Document()
    doc.add_paragraph(cover_letter_text)
    doc_buffer = BytesIO()
    doc.save(doc_buffer)
    doc_buffer.seek(0)
    return send_file(
        doc_buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
