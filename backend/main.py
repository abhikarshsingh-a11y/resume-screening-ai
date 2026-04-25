import os
import sys
import shutil
import warnings
import logging

# Suppress logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)

# FastAPI imports
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

# Add paths
sys.path.append(
    r"C:\Users\singh\resume-screening-ai\person1_work"
)
sys.path.append(
    r"C:\Users\singh\resume-screening-ai\combined"
)

# Import your functions
from read_resume import read_resume
from clean_text import clean_text
from extract_skills import extract_skills
from smart_match import get_semantic_score, find_skill_details
from bias_detector import detect_bias

# Create app
app = FastAPI(
    title="Resume Screening AI",
    description="AI powered resume screening platform",
    version="1.0.0"
)

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ─────────────────────────
# ENDPOINT 1 — Home
# ─────────────────────────
@app.get("/")
def home():
    return {
        "message": "Resume Screening AI is running",
        "status": "active",
        "version": "1.0.0"
    }

# ─────────────────────────
# ENDPOINT 2 — Analyze
# ─────────────────────────
@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    # Save file temporarily
    temp_path = f"temp_{resume.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    try:
        # Read and process resume
        raw_text = read_resume(temp_path)
        cleaned_text = clean_text(raw_text)

        # Extract skills
        resume_skills = extract_skills(cleaned_text)
        job_skills = extract_skills(job_description.lower())

        # Get AI match score
        match_score = get_semantic_score(
            cleaned_text,
            job_description
        )

        # Get matched and missing skills
        matched, missing = find_skill_details(
            cleaned_text,
            job_skills
        )

        # Detect bias
        original, debiased, bias_impact = detect_bias(
            temp_path,
            job_description
        )

        # Recommendation
        if match_score >= 70:
            recommendation = "STRONG MATCH"
        elif match_score >= 50:
            recommendation = "MODERATE MATCH"
        else:
            recommendation = "WEAK MATCH"

        return {
            "status": "success",
            "match_score": match_score,
            "resume_skills": resume_skills,
            "matched_skills": matched,
            "missing_skills": missing,
            "bias_original_score": original,
            "bias_free_score": debiased,
            "bias_impact": abs(bias_impact),
            "recommendation": recommendation
        }

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

# ─────────────────────────
# ENDPOINT 3 — Health
# ─────────────────────────
@app.get("/health")
def health():
    return {"status": "healthy"}