import os
import sys

# Works on both Windows and Linux
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "person1_work"))
sys.path.append(os.path.join(BASE_DIR, "person2_work"))

from read_resume import read_resume
from clean_text import clean_text
from extract_skills import extract_skills as get_resume_skills


def get_job_skills():
    job_text = """
    Looking for developer with Python, SQL, 
    cybersecurity, aws, docker, networking skills.
    Knowledge of DSA and OOP required.
    """.lower()
    
    all_skills = [
        "python", "java", "c++", "c", "sql",
        "javascript", "html", "css",
        "machine learning", "deep learning",
        "cybersecurity", "digital forensics",
        "networking", "ethical hacking",
        "dsa", "oop", "data structures",
        "git", "docker", "linux", "aws"
    ]
    
    found = []
    for skill in all_skills:
        if skill in job_text:
            found.append(skill)
    return found


def match_skills(resume_skills, job_skills):
    matched = []
    for skill in resume_skills:
        if skill in job_skills:
            matched.append(skill)
    
    missing = []
    for skill in job_skills:
        if skill not in resume_skills:
            missing.append(skill)
    
    if len(job_skills) == 0:
        score = 0
    else:
        score = (len(matched) / len(job_skills)) * 100
    
    return matched, missing, round(score, 2)


# ALL test code inside here - never runs on server
if __name__ == "__main__":
    print("🔍 Analyzing resume...")
    print("=" * 40)

    raw = read_resume(r"C:\Users\singh\resume-screening-ai\data\resume.pdf")
    cleaned = clean_text(raw)
    resume_skills = get_resume_skills(cleaned)

    job_skills = get_job_skills()
    matched, missing, score = match_skills(resume_skills, job_skills)

    print(f"\n📄 Resume Skills Found: {resume_skills}")
    print(f"\n💼 Job Required Skills: {job_skills}")
    print(f"\n✅ Matched Skills: {matched}")
    print(f"\n❌ Missing Skills: {missing}")
    print(f"\n🎯 Match Score: {score}%")
    print("=" * 40)