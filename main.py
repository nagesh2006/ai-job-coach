from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import logging
from groq import Groq
import os
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

# Initialize Groq client lazily
client = None

def get_groq_client():
    global client
    if client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="GROQ_API_KEY environment variable not set")
        try:
            client = Groq(api_key=api_key)
        except TypeError:
            # Fallback for older Groq versions
            import groq
            client = groq.Client(api_key=api_key)
    return client

class JobApplicationRequest(BaseModel):
    resume_text: str
    job_description: str

@app.post("/tailor")
async def tailor_application(request: JobApplicationRequest):
    try:
        prompt = f"""
You are an expert career coach. Analyze the resume and job description, then return a JSON response with exactly these keys:

RESUME:
{request.resume_text}

JOB DESCRIPTION:
{request.job_description}

Return JSON with:
- "resume_bullets": array of 5-7 tailored bullet points that match the job requirements
- "cover_letter": string under 200 words highlighting key matches
- "skills": array of top 5 skills/keywords to emphasize from the job description
- "match_score": integer from 0-100 representing how well the resume matches the job

Respond with valid JSON only, no additional text.
"""

        groq_client = get_groq_client()
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            temperature=0.3,
            max_tokens=1000
        )
        
        result = json.loads(response.choices[0].message.content)
        logger.info(f"Successfully processed application tailoring")
        return result
        
    except json.JSONDecodeError:
        logger.error("Failed to parse JSON response from AI model")
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