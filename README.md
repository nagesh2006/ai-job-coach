# AI-Powered Job Application Coach

FastAPI backend that tailors resumes and generates cover letters using Groq's free LLaMA-3 API.

## Setup

1. Create virtual environment:
```bash
python -m venv .venv
```

2. Activate virtual environment:
```bash
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Get your free Groq API key from https://console.groq.com/

5. Set environment variable:
```bash
export GROQ_API_KEY=your_api_key_here
```

6. Run the server:
```bash
uvicorn main:app --reload
```

## API Usage

POST `/tailor` with JSON:
```json
{
  "resume_text": "Your resume content...",
  "job_description": "Job posting content..."
}
```

Returns:
```json
{
  "resume_bullets": ["Tailored bullet point 1", "..."],
  "cover_letter": "Short cover letter draft...",
  "skills": ["skill1", "skill2", "skill3", "skill4", "skill5"],
  "match_score": 85
}
```

## Deploy

Ready for Render/Railway deployment with included requirements.txt.