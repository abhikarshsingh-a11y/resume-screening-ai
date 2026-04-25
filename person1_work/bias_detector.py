import re
import sys
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import warnings
warnings.filterwarnings('ignore')
import logging
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)

sys.path.append(r"C:\Users\singh\resume-screening-ai\person1_work")
sys.path.append(r"C:\Users\singh\resume-screening-ai\combined")

from read_resume import read_resume
from clean_text import clean_text
from smart_match import get_semantic_score, model

def remove_bias_elements(text):
    
    cleaned = text
    
    # Remove email addresses
    cleaned = re.sub(r'\S+@\S+', '[EMAIL REMOVED]', cleaned)
    
    # Remove phone numbers
    cleaned = re.sub(r'[\+\(]?[1-9][0-9\s\-\(\)]{8,20}[0-9]', '[PHONE REMOVED]', cleaned)
    
    # Remove URLs and LinkedIn
    cleaned = re.sub(r'http\S+|www\S+|linkedin\S+', '[LINK REMOVED]', cleaned)
    
    # Remove university names
    universities = [
        "galgotias university", "amity university",
        "bennett university", "sharda university",
        "iit delhi", "iit bombay", "nit trichy",
        "bits pilani", "vit vellore", "srm university"
    ]
    for uni in universities:
        cleaned = re.sub(uni, '[COLLEGE REMOVED]', 
                        cleaned, flags=re.IGNORECASE)
    
    # Remove first line (candidate name)
    lines = cleaned.split('\n')
    if len(lines) > 0:
        lines[0] = '[NAME REMOVED]'
    cleaned = '\n'.join(lines)
    
    return cleaned   

 
def detect_bias(resume_path, job_description):
    
    print("\n🔍 Running Bias Detection Analysis...")
    print("=" * 50)
    
    # Step 1 - Read original resume
    raw_text = read_resume(resume_path)
    cleaned_text = clean_text(raw_text)
    
    # Step 2 - Get score WITH personal info
    original_score = get_semantic_score(cleaned_text, job_description)
    
    # Step 3 - Remove bias elements
    debiased_text = remove_bias_elements(cleaned_text)
    
    # Step 4 - Get score WITHOUT personal info
    debiased_score = get_semantic_score(debiased_text, job_description)
    
    # Step 5 - Calculate bias impact
    bias_impact = round(original_score - debiased_score, 2)
    
    return original_score, debiased_score, bias_impact, debiased_text

# Job description for testing
job_description = """
Looking for a developer with skills in:
Python, SQL, cybersecurity, machine learning,
networking, docker, aws, data analysis
"""

# Run bias detection
resume_path = r"C:\Users\singh\resume-screening-ai\data\resume.pdf"

original, debiased, impact, clean_resume = detect_bias(
    resume_path, 
    job_description
)

# Show results
print(f"\n👤 Score WITH personal info  : {original}%")
print(f"🎭 Score WITHOUT personal info: {debiased}%")
print(f"\n⚖️  Bias Impact: {abs(impact)}%")

if impact > 5:
    print("🚨 HIGH BIAS DETECTED")
    print("   Personal information is significantly")
    print("   affecting this candidate's score")
elif impact > 2:
    print("⚠️  MODERATE BIAS DETECTED")
    print("   Some personal information is affecting score")
elif impact < -2:
    print("⚠️  REVERSE BIAS DETECTED")
    print("   Personal info is hurting candidate's score")
else:
    print("✅ LOW BIAS")
    print("   Score is fairly based on skills")

print("\n📋 What was removed:")
print("   → Candidate name")
print("   → Email address")
print("   → Phone number")
print("   → College/University name")
print("   → Location information")
print("   → LinkedIn profile")

print("\n" + "=" * 50)