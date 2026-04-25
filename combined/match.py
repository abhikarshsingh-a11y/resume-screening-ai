# Import files from both teammates
import sys
sys.path.append(r"C:\Users\singh\resume-screening-ai\person1_work")
sys.path.append(r"C:\Users\singh\resume-screening-ai\person2_work")

from read_resume import read_resume
from clean_text import clean_text
from extract_skills import extract_skills as get_resume_skills

# For now we manually write job skills
# Later this will come from partner's file
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

# Match resume skills vs job skills
def match_skills(resume_skills, job_skills):
    
    # Find matching skills
    matched = []
    for skill in resume_skills:
        if skill in job_skills:
            matched.append(skill)
    
    # Find missing skills
    missing = []
    for skill in job_skills:
        if skill not in resume_skills:
            missing.append(skill)
    
    # Calculate score
    if len(job_skills) == 0:
        score = 0
    else:
        score = (len(matched) / len(job_skills)) * 100
    
    return matched, missing, round(score, 2)

# Run everything
print("🔍 Analyzing resume...")
print("=" * 40)

# Step 1 - Get resume skills
raw = read_resume(r"C:\Users\singh\resume-screening-ai\data\resume.pdf")
cleaned = clean_text(raw)
resume_skills = get_resume_skills(cleaned)

# Step 2 - Get job skills
job_skills = get_job_skills()

# Step 3 - Match them
matched, missing, score = match_skills(resume_skills, job_skills)

# Step 4 - Show results
print(f"\n📄 Resume Skills Found: {resume_skills}")
print(f"\n💼 Job Required Skills: {job_skills}")
print(f"\n✅ Matched Skills: {matched}")
print(f"\n❌ Missing Skills: {missing}")
print(f"\n🎯 Match Score: {score}%")
print("=" * 40)