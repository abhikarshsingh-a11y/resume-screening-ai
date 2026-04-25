# Suppress all unnecessary warnings and logs
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import warnings
warnings.filterwarnings('ignore')

import logging
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)



# Import libraries
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import sys

# Add paths to find our files
sys.path.append(r"C:\Users\singh\resume-screening-ai\person1_work")

from read_resume import read_resume
from clean_text import clean_text

# Load AI model
# This model understands meaning of text
print("Loading AI model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ AI Model loaded successfully")

# Function to get semantic score
def get_semantic_score(resume_text, job_text):
    
    # Convert both texts to embeddings (numbers)
    resume_embedding = model.encode([resume_text])
    job_embedding = model.encode([job_text])
    
    # Measure similarity between both embeddings
    score = cosine_similarity(resume_embedding, job_embedding)
    
    # Convert to percentage
    percentage = round(float(score[0][0]) * 100, 2)
    
    return percentage

# Function to find matched and missing skills
def find_skill_details(resume_text, job_skills):
    
    matched = []
    missing = []
    
    for skill in job_skills:
        # Get embedding for skill
        skill_embedding = model.encode([skill])
        resume_embedding = model.encode([resume_text])
        
        # Check similarity
        similarity = cosine_similarity(skill_embedding, resume_embedding)
        score = float(similarity[0][0])
        
        # If similarity is above 0.3 consider it matched
        if score > 0.3:
            matched.append(skill)
        else:
            missing.append(skill)
    
    return matched, missing

# Job requirements
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

# Run the analysis
print("\n🔍 Analyzing resume with AI...")
print("=" * 50)

# Step 1 - Read and clean resume
raw_text = read_resume(r"C:\Users\singh\resume-screening-ai\data\resume.pdf")
cleaned_text = clean_text(raw_text)

# Step 2 - Get overall semantic score
overall_score = get_semantic_score(cleaned_text, job_description)

# Step 3 - Find matched and missing skills
matched, missing = find_skill_details(cleaned_text, job_skills)

# Step 4 - Show results
print(f"\n📄 Candidate: Abhikarsh Singh")
print(f"\n✅ Matched Skills: {matched}")
print(f"\n❌ Missing Skills: {missing}")
print(f"\n🎯 AI Match Score: {overall_score}%")

# Step 5 - Give recommendation
print("\n📊 Recommendation:")
if overall_score >= 70:
    print("✅ STRONG MATCH - Recommend for interview")
elif overall_score >= 50:
    print("⚠️  MODERATE MATCH - Consider for interview")
else:
    print("❌ WEAK MATCH - Does not meet requirements")

print("=" * 50)