
from flask import Flask, render_template, request, redirect, url_for, send_file, abort
import os
from werkzeug.utils import secure_filename
from resume_reader import extract_skills
from job_scraper import scrape_all_jobs
from generate_cover_letter import generate_cover_letter
from docx import Document
from fpdf import FPDF
from io import BytesIO

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Globals (for demo only — replace with session/db for production)
user_resume_text = ""
user_resume_skills = []
jobs_with_letters = []  # Global list to hold jobs and cover letters

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('resume')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Extract skills and summary text from resume PDF/DOCX
            extracted = extract_skills(filepath)
            global user_resume_text, user_resume_skills
            user_resume_skills = extracted.get("skills", [])
            user_resume_text = extracted.get("summary", "")

            return redirect(url_for('jobs'))
    return render_template('index.html')

@app.route('/jobs')
def jobs():
    global user_resume_text, user_resume_skills, jobs_with_letters

    scraped_jobs = scrape_all_jobs(user_resume_skills)
    jobs_with_letters = []

    for job in scraped_jobs:
        cover_letter = generate_cover_letter(
            user_name="Your Name",
            resume_summary=user_resume_text,
            skills=user_resume_skills,
            job=job
        )
        job_copy = job.copy()
        job_copy['cover_letter'] = cover_letter
        jobs_with_letters.append(job_copy)

    return render_template('results.html', jobs=jobs_with_letters)



from fpdf import FPDF
from io import BytesIO
from flask import send_file

def generate_pdf_cover_letter(text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf_output = BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin1')  # Get PDF as string, encode as bytes
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)
    return send_file(pdf_output, download_name=filename, as_attachment=True, mimetype='application/pdf')



from docx import Document
from io import BytesIO
from flask import send_file

def generate_docx_cover_letter(text, filename):
    doc = Document()
    doc.add_paragraph(text)
    doc_output = BytesIO()
    doc.save(doc_output)
    doc_output.seek(0)
    return send_file(doc_output, download_name=filename, as_attachment=True,
                     mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')



@app.route('/download/<int:index>/<string:filetype>', methods=['GET'])
def download(index, filetype):
    global jobs_with_letters
    if index < 0 or index >= len(jobs_with_letters):
        abort(404)

    job = jobs_with_letters[index]
    cover_letter = job['cover_letter']
    filename = f"{job['company'].replace(' ', '_')}_cover_letter.{filetype}"

    if filetype == 'docx':
        return generate_docx_cover_letter(cover_letter, filename)
    elif filetype == 'pdf':
        return generate_pdf_cover_letter(cover_letter, filename)
    else:
        abort(400, description="Unsupported file type requested.")

if __name__ == '__main__':
    app.run(debug=True)

