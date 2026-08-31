import os
import json

import os
import json
from fastapi.concurrency import run_in_threadpool
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from pypdf import PdfReader
from playwright.sync_api import sync_playwright



# Configuration

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    raise ValueError("MISTRAL_API_KEY is not set in the .env file")

mistral_client = ChatMistralAI(
    api_key=MISTRAL_API_KEY,
    model="mistral-small-latest",
    temperature=0.5
)

app = FastAPI(
    title="AI Job Application Assistant",
    description="Generate personalized job application materials using AI."
)


# Resume PDF Extraction


def extract_resume_text(file: UploadFile) -> str:
    """
    Extract text from an uploaded PDF resume.
    """

    try:
        reader = PdfReader(file.file)

        resume_text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                resume_text += page_text + "\n"

        resume_text = resume_text.strip()

        if not resume_text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the uploaded resume."
            )

        return resume_text[:12000]

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error reading resume PDF: {str(e)}"
        )


# Job Posting Extraction using Playwright


def extract_job_description(url: str):

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )

        page = browser.new_page()

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_timeout(3000)

        job_title = page.title()
        job_text = page.locator("body").inner_text()

        browser.close()

        return job_text, job_title


# Generate Application Materials

def generate_application_materials(
    job_text: str,
    resume_text: str
):
    """
    Generate:
    1. Application Email
    2. Cover Letter
    3. Job Summary
    """

    prompt = f"""
You are an AI Job Application Assistant.

Your task is to analyze a job posting and a candidate's resume
and generate personalized application materials.

JOB POSTING


{job_text}



CANDIDATE RESUME


{resume_text}



INSTRUCTIONS


Generate exactly these three outputs:

1. APPLICATION EMAIL
2. COVER LETTER
3. JOB SUMMARY


APPLICATION EMAIL:
- Professional and concise.
- Address it to "Dear Hiring Manager,".
- Mention why the candidate is interested in the role.
- Connect relevant candidate skills/projects/experience to the job.
- Keep it around 150-200 words.
- Do not invent information.


COVER LETTER:
- Professional and personalized.
- Explain why the candidate is suitable for the role.
- Highlight relevant skills, projects, education, and experience
  from the resume.
- Connect the candidate's background with the job requirements.
- Keep it around 300-450 words.
- Do not invent information.


JOB SUMMARY:
Summarize the job posting clearly.

Include:
- Position
- Company (if available)
- Location (if available)
- Main responsibilities
- Required skills
- Qualifications
- Experience requirements
- Important technologies

Keep the summary concise and useful.


IMPORTANT:
- Only use information present in the job posting and resume.
- NEVER invent skills, experience, education, projects,
  companies, achievements, or qualifications.
- If some information is unavailable, do not make it up.
- Return the result as valid JSON.
- Do not add markdown code fences.

Use exactly this JSON structure:

{{
    "email": "...",
    "cover_letter": "...",
    "job_summary": "..."
}}
"""

    try:

        response = mistral_client.invoke(prompt)

        result = response.content.strip()

        # Remove accidental markdown fences
        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

        # Convert JSON string into Python dictionary
        data = json.loads(result)

        return data

    except json.JSONDecodeError:

        raise HTTPException(
            status_code=500,
            detail="The AI returned an invalid response format."
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Mistral API error: {str(e)}"
        )



# Main API Endpoint

@app.post("/generate_application")
async def generate_application(
    link: str = Form(...),
    resume: UploadFile = File(...)
):

    if not link.startswith(("http://", "https://")):
        raise HTTPException(
            status_code=400,
            detail="Please provide a valid job posting URL."
        )

    if resume.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF resume."
        )

    # Run synchronous Playwright outside the asyncio event loop
    job_text, job_title = await run_in_threadpool(
        extract_job_description,
        link
    )

    resume_text = extract_resume_text(resume)

    generated_content = generate_application_materials(
        job_text,
        resume_text
    )

    return {
        "job_title": job_title,
        "email": generated_content.get("email", ""),
        "cover_letter": generated_content.get("cover_letter", ""),
        "job_summary": generated_content.get("job_summary", "")
    }


# Home Page


@app.get("/")
def home():

    return {
        "message": "AI Job Application Assistant API is running."
    }

