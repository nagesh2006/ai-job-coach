from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import logging
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Job Application Coach", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def call_groq_api(prompt: str):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY environment variable not set")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "llama-3.1-8b-instant",
        "temperature": 0.3,
        "max_tokens": 1000
    }
    
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=data
    )
    
    if response.status_code != 200:
        raise Exception(f"Groq API error: {response.status_code} - {response.text}")
    
    return response.json()["choices"][0]["message"]["content"]

class JobApplicationRequest(BaseModel):
    resume_text: str
    job_description: str

@app.post("/tailor")
async def tailor_application(request: JobApplicationRequest):
    try:
        prompt = f"""
Analyze this resume and job description, then return ONLY a valid JSON object with no additional text or formatting:

RESUME: {request.resume_text}

JOB DESCRIPTION: {request.job_description}

Return this exact JSON structure:
{{
  "resume_bullets": ["bullet1", "bullet2", "bullet3", "bullet4", "bullet5"],
  "cover_letter": "short cover letter under 200 words",
  "skills": ["skill1", "skill2", "skill3", "skill4", "skill5"],
  "match_score": 85
}}

Respond with ONLY the JSON object, no markdown, no explanations.
"""

        response_content = call_groq_api(prompt)
        logger.info(f"AI Response: {response_content}")
        
        # Try to extract JSON if wrapped in markdown
        if "```json" in response_content:
            response_content = response_content.split("```json")[1].split("```")[0].strip()
        elif "```" in response_content:
            response_content = response_content.split("```")[1].split("```")[0].strip()
        
        result = json.loads(response_content)
        logger.info(f"Successfully processed application tailoring")
        return result
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response: {response_content[:200]}...")
        return {"error": "Failed to generate structured response"}
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return {"error": f"Processing failed: {str(e)}"}

@app.get("/")
async def root():
    return {"message": "AI Job Application Coach API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}