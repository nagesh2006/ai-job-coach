# AI-Powered Job Application Coach

FastAPI backend that tailors resumes and generates cover letters using Groq's free LLaMA-3.1 API.

## Features
- ✅ Tailored resume bullet points
- ✅ AI-generated cover letter (<200 words)
- ✅ Top 5 skills/keywords extraction
- ✅ Resume-job match score (0-100)
- ✅ CORS enabled for frontend integration
- ✅ Production-ready error handling

## Setup

1. **Create virtual environment:**
```bash
python -m venv .venv
```

2. **Activate virtual environment:**
```bash
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Get Groq API key:**
   - Visit https://console.groq.com/
   - Create free account
   - Generate API key

5. **Set environment variable:**
   - Create `.env` file in project root
   - Add: `GROQ_API_KEY=your_actual_api_key_here`

6. **Run the server:**
```bash
uvicorn main:app --reload
```

## API Endpoints

### POST `/tailor`
Tailors resume for specific job posting.

**Request:**
```json
{
  "resume_text": "Software Engineer with 3 years Python experience...",
  "job_description": "Looking for Python developer with FastAPI knowledge..."
}
```

**Response:**
```json
{
  "resume_bullets": [
    "Developed scalable APIs using FastAPI and Python",
    "Built microservices handling 10k+ requests/day",
    "Implemented async programming for performance optimization"
  ],
  "cover_letter": "Dear Hiring Manager, I am excited to apply...",
  "skills": ["Python", "FastAPI", "API Development", "Async Programming", "Microservices"],
  "match_score": 87
}
```

### GET `/`
Health check endpoint.

### GET `/health`
API status endpoint.

## Testing

**Using curl (Windows CMD):**
```cmd
curl -X POST "http://localhost:8000/tailor" -H "Content-Type: application/json" -d "{\"resume_text\": \"Your resume...\", \"job_description\": \"Job posting...\"}"
```

**Using browser:**
Visit http://localhost:8000/docs for interactive API documentation.

## Deployment

**Render/Railway ready:**
- Includes `requirements.txt`
- Environment variable support
- Production CORS settings
- Comprehensive error handling

**Environment Variables:**
- `GROQ_API_KEY` - Your Groq API key (required)

## Tech Stack
- **Framework:** FastAPI
- **AI Model:** LLaMA-3.1-8B-Instant (via Groq)
- **HTTP Client:** Requests
- **Environment:** python-dotenv