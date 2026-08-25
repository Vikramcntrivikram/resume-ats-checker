from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import os
import anthropic
import PyPDF2
import docx
from werkzeug.utils import secure_filename
import json
import re

app = Flask(__name__)
app.secret_key = 'vikram-trivikram-resume-ats-checker-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Anthropic client
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_AUTH_TOKEN"),
    base_url=os.environ.get("ANTHROPIC_BASE_URL")
)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_text(file_path):
    filename = file_path.lower()
    if filename.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif filename.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif filename.endswith('.txt'):
        return extract_text_from_txt(file_path)
    else:
        return ""

def analyze_resume_with_claude(resume_text, job_description):
    prompt = f"""
You are an expert ATS (Applicant Tracking System) analyzer. Your task is to evaluate how well a resume matches a job description and provide detailed feedback.

Please analyze the following resume against the job description and provide:

1. An overall match score (0-100%)
2. Missing keywords/skills from the job description that are not in the resume
3. Specific suggestions for improvement
4. Strengths of the resume for this position
5. Weaknesses/gaps identified

Resume:
{resume_text}

Job Description:
{job_description}

Please provide your analysis in JSON format with the following structure:
{{
  "score": <integer between 0-100>,
  "missing_keywords": [<list of missing keywords/skills>],
  "suggestions": [<list of specific improvement suggestions>],
  "strengths": [<list of resume strengths for this position>],
  "weaknesses": [<list of weaknesses/gaps>],
  "detailed_feedback": "<detailed paragraph explanation>"
}}
"""

    try:
        message = client.messages.create(
            model="claude-opus-5[1m]",
            max_tokens=2000,
            temperature=0.3,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Extract JSON from the response
        response_text = message.content[0].text

        # Try to find JSON in the response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            return json.loads(json_str)
        else:
            # Fallback if JSON parsing fails
            return {
                "score": 50,
                "missing_keywords": ["Unable to parse analysis"],
                "suggestions": ["Please try again with clearer formatting"],
                "strengths": ["Analysis incomplete"],
                "weaknesses": ["System error in processing"],
                "detailed_feedback": "There was an error processing your request. Please try again."
            }

    except Exception as e:
        return {
            "score": 0,
            "missing_keywords": [f"Error: {str(e)}"],
            "suggestions": ["Please check your internet connection and try again"],
            "strengths": [],
            "weaknesses": ["System error"],
            "detailed_feedback": f"An error occurred: {str(e)}"
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        flash('No resume file uploaded')
        return redirect(request.url)

    file = request.files['resume']
    job_description = request.form.get('job_description', '')

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if job_description == '':
        flash('Please provide a job description')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract text from resume
        resume_text = extract_text(file_path)

        # Clean up uploaded file
        os.remove(file_path)

        if not resume_text.strip():
            flash('Could not extract text from the resume. Please ensure it is a valid PDF, DOCX, or TXT file.')
            return redirect(request.url)

        # Analyze with Claude
        results = analyze_resume_with_claude(resume_text, job_description)

        return render_template('results.html',
                             results=results,
                             resume_text=resume_text[:500] + "..." if len(resume_text) > 500 else resume_text,
                             job_description=job_description[:500] + "..." if len(job_description) > 500 else job_description)

    else:
        flash('Allowed file types are PDF, DOCX, and TXT')
        return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)