import os
import warnings
import logging
import sys

# Suppress logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)

# Add paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "person1_work"))

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from read_resume import read_resume
from clean_text import clean_text


# Lighter model - uses less memory
model = SentenceTransformer('paraphrase-MiniLM-L3-v2')

def get_semantic_score(resume_text, job_text):
    resume_embedding = model.encode([resume_text])
    job_embedding = model.encode([job_text])
    score = cosine_similarity(resume_embedding, job_embedding)
    return round(float(score[0][0]) * 100, 2)

def find_skill_details(resume_text, job_skills):
    matched = []
    missing = []
    for skill in job_skills:
        skill_embedding = model.encode([skill])
        resume_embedding = model.encode([resume_text])
        similarity = cosine_similarity(skill_embedding, resume_embedding)
        if float(similarity[0][0]) > 0.3:
            matched.append(skill)
        else:
            missing.append(skill)
    return matched, missing

# ALL test code inside here - never runs on server
if __name__ == "__main__":
    job_description = """
    Looking for a developer with skills in:
    Python, SQL, cybersecurity, machine learning,
    networking, docker, aws, data analysis
    """
    job_skills = [
        "python", "sql", "cybersecurity",
        "machine learning", "networking",
        "docker", "aws", "data analysis"
    ]
    raw_text = read_resume(r"C:\Users\singh\resume-screening-ai\data\resume.pdf")
    cleaned_text = clean_text(raw_text)
    overall_score = get_semantic_score(cleaned_text, job_description)
    matched, missing = find_skill_details(cleaned_text, job_skills)
    print(f"Score: {overall_score}%")
    print(f"Matched: {matched}")
    print(f"Missing: {missing}")