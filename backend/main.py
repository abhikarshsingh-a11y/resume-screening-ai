import os
import sys
import shutil
import warnings
import logging

# Suppress logs FIRST
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)

# Debug prints to see what's happening on Render
print("Python version:", sys.version)
print("Starting imports...")

# FastAPI imports
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

# Add paths - works on both Windows and Linux
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("BASE_DIR:", BASE_DIR)

sys.path.append(os.path.join(BASE_DIR, "person1_work"))
sys.path.append(os.path.join(BASE_DIR, "person2_work"))
sys.path.append(os.path.join(BASE_DIR, "combined"))
sys.path.append(os.path.join(BASE_DIR, "backend"))

# Import functions with debug prints
try:
    from read_resume import read_resume
    print("read_resume OK")
    from clean_text import clean_text
    print("clean_text OK")
    from extract_skills import extract_skills
    print("extract_skills OK")
    from smart_match import get_semantic_score, find_skill_details
    print("smart_match OK")
    from bias_detector import detect_bias
    print("bias_detector OK")
    from database import create_tables, save_candidate, save_score, get_all_candidates, get_top_candidates, get_scores_for_candidate
    print("database OK")
except Exception as e:
    print("IMPORT ERROR:", str(e))
    sys.exit(1)

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

# Create tables when API starts
create_tables()
print("Database tables created OK")

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
    job_description: str = Form(...),
    candidate_name: str = Form(...),
    candidate_email: str = Form(...)
):
    temp_path = f"temp_{resume.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    try:
        raw_text = read_resume(temp_path)
        cleaned_text = clean_text(raw_text)

        resume_skills = extract_skills(cleaned_text)
        job_skills = extract_skills(job_description.lower())

        match_score = get_semantic_score(cleaned_text, job_description)
        matched, missing = find_skill_details(cleaned_text, job_skills)
        original, debiased, bias_impact = detect_bias(temp_path, job_description)

        if match_score >= 70:
            recommendation = "STRONG MATCH"
        elif match_score >= 50:
            recommendation = "MODERATE MATCH"
        else:
            recommendation = "WEAK MATCH"

        candidate_id = save_candidate(candidate_name, candidate_email, cleaned_text)
        save_score(candidate_id, job_description[:50], match_score, missing)

        return {
            "status": "success",
            "candidate_id": candidate_id,
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

# ─────────────────────────
# ENDPOINT 4 — All Candidates
# ─────────────────────────
@app.get("/candidates")
def get_candidates():
    candidates = get_all_candidates()
    return {
        "status": "success",
        "total": len(candidates),
        "candidates": candidates
    }

# ─────────────────────────────────────
# RECRUITER ROUTES
# ─────────────────────────────────────

@app.get("/recruiter/candidates")
def recruiter_candidates():
    candidates = get_all_candidates()
    if not candidates:
        return {"status": "success", "total": 0, "candidates": [], "message": "No candidates yet"}
    result = []
    for c in candidates:
        result.append({"id": c[0], "name": c[1], "email": c[2], "date": c[4]})
    return {"status": "success", "total": len(result), "candidates": result}


@app.get("/recruiter/top")
def recruiter_top(job_title: str = "Developer"):
    results = get_top_candidates(job_title, limit=10)
    if not results:
        return {"status": "success", "message": f"No candidates found for {job_title}", "top_candidates": []}
    ranked = []
    for r in results:
        ranked.append({"name": r[0], "email": r[1], "match_score": f"{round(r[2], 1)}%", "missing_skills": r[3]})
    return {"status": "success", "job_title": job_title, "total": len(ranked), "top_candidates": ranked}


@app.get("/recruiter/candidate/{candidate_id}")
def get_candidate(candidate_id: int):
    scores = get_scores_for_candidate(candidate_id)
    candidates = get_all_candidates()
    candidate_info = None
    for c in candidates:
        if c[0] == candidate_id:
            candidate_info = c
            break
    if not candidate_info:
        return {"status": "error", "message": f"Candidate {candidate_id} not found"}
    score_history = []
    for s in scores:
        score_history.append({"job_title": s[2], "match_score": f"{round(s[3], 1)}%", "missing_skills": s[4], "date": s[5]})
    return {"status": "success", "candidate_id": candidate_id, "name": candidate_info[1], "email": candidate_info[2], "score_history": score_history}


@app.delete("/recruiter/candidate/{candidate_id}")
def delete_candidate(candidate_id: int):
    import sqlite3
    try:
        BASE_DB = os.path.join(BASE_DIR, "backend", "resume_screening.db")
        conn = sqlite3.connect(BASE_DB)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM scores WHERE candidate_id = ?", (candidate_id,))
        cursor.execute("DELETE FROM candidates WHERE id = ?", (candidate_id,))
        conn.commit()
        conn.close()
        return {"status": "success", "message": f"Candidate {candidate_id} deleted"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/recruiter/stats")
def get_stats():
    candidates = get_all_candidates()
    if not candidates:
        return {"status": "success", "total_candidates": 0, "message": "No data yet"}
    all_scores = []
    for c in candidates:
        scores = get_scores_for_candidate(c[0])
        for s in scores:
            all_scores.append(s[3])
    avg_score = round(sum(all_scores) / len(all_scores), 1) if all_scores else 0
    return {"status": "success", "total_candidates": len(candidates), "total_applications": len(all_scores), "average_score": f"{avg_score}%"}