# Resume ATS Score Checker

A web application that analyzes resumes against job descriptions and provides an ATS compatibility score with detailed feedback. Developed by **Vikram TRIVIKRAM**.

## Features

- Upload resume (PDF, DOCX, TXT)
- Input job description
- Get instant ATS compatibility score (0-100%)
- Detailed analysis including:
  - Missing keywords
  - Strengths
  - Improvement suggestions
  - Weaknesses/gaps
  - Detailed feedback paragraph

## How It Works

1. Upload your resume in PDF, DOCX, or TXT format
2. Paste the job description you're targeting
3. Receive an instant ATS compatibility score
4. Get detailed feedback on how to improve your resume for better ATS compatibility

## Technology Stack

- Backend: Python Flask
- AI: Anthropic Claude API (claude-opus-5[1m])
- Frontend: HTML, CSS (Bootstrap), JavaScript
- Document Processing: PyPDF2, python-docx

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/resume-ats-checker.git
   cd resume-ats-checker
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set environment variables:
   ```bash
   export ANTHROPIC_AUTH_TOKEN=your_anthropic_api_key
   export ANTHROPIC_BASE_URL=http://127.0.0.1:8082  # Optional, if using a proxy
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and go to `http://localhost:5000`

## Deployment

### To Deploy on GitHub Pages (for static frontend only)
Note: This application requires a backend to process resumes with Claude API, so it cannot be fully deployed on GitHub Pages alone. Consider deploying to a platform that supports Python applications like:
- Heroku
- Render
- Railway
- AWS Elastic Beanstalk
- Google Cloud Run

### Example Deployment to Heroku

1. Create a Procfile:
   ```
   web: gunicorn app:app
   ```

2. Create a requirements.txt (already included)

3. Initialize git and create Heroku app:
   ```bash
   heroku create
   git push heroku main
   heroku config:set ANTHROPIC_AUTH_TOKEN=your_anthropic_api_key
   ```

## Folder Structure

```
resume-ats-checker/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore rules
├── README.md           # This file
└── templates/
    ├── base.html       # Base template
    ├── index.html      # Home page
    └── results.html    # Results page
```

## License

This project is licensed under the MIT License.

## Contact

Developed by **Vikram TRIVIKRAM**

For questions or suggestions, please open an issue on GitHub.

--- 

**Note**: This application uses the Anthropic Claude API. You need to obtain an API key from Anthropic to use this application.