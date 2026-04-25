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
from smart_match import get_semantic_score

def remove_bias_elements(text):
    cleaned = text
    
    # Remove email
    cleaned = re.sub(r'\S+@\S+', '[EMAIL REMOVED]', cleaned)
    
    # Remove phone numbers
    cleaned = re.sub(
        r'[\+\(]?[1-9][0-9\s\-\(\)]{8,20}[0-9]',
        '[PHONE REMOVED]', cleaned
    )
    
    # Remove LinkedIn
    cleaned = re.sub(
        r'http\S+|www\S+|linkedin\S+',
        '[LINK REMOVED]', cleaned,
        flags=re.IGNORECASE
    )
    
    # Remove university names
    universities = [
        "galgotias university", "amity university",
        "bennett university", "sharda university",
        "iit delhi", "iit bombay", "nit trichy",
        "bits pilani", "vit vellore", "srm university"
    ]
    for uni in universities:
        cleaned = re.sub(
            uni, '[COLLEGE REMOVED]',
            cleaned, flags=re.IGNORECASE
        )
    
    # Remove first line (candidate name)
    lines = cleaned.split('\n')
    if len(lines) > 0:
        lines[0] = '[NAME REMOVED]'
    cleaned = '\n'.join(lines)
    
    return cleaned


def detect_bias(resume_path, job_description):
    # Read resume
    raw_text = read_resume(resume_path)
    cleaned_text = clean_text(raw_text)
    
    # Score WITH personal info
    original_score = get_semantic_score(
        cleaned_text, job_description
    )
    
    # Remove bias elements
    debiased_text = remove_bias_elements(cleaned_text)
    
    # Score WITHOUT personal info
    debiased_score = get_semantic_score(
        debiased_text, job_description
    )
    
    # Calculate bias impact
    bias_impact = round(original_score - debiased_score, 2)
    
    # Return only 3 values
    return original_score, debiased_score, bias_impact


# ↓ ALL TEST CODE INSIDE HERE
if __name__ == "__main__":
    job_description = """
    Looking for a developer with skills in:
    Python, SQL, cybersecurity, machine learning,
    networking, docker, aws, data analysis
    """

    resume_path = r"C:\Users\singh\resume-screening-ai\data\resume.pdf"

    original, debiased, impact = detect_bias(
        resume_path,
        job_description
    )

    print("\n" + "=" * 50)
    print(f"👤 Score WITH personal info   : {original}%")
    print(f"🎭 Score WITHOUT personal info : {debiased}%")
    print(f"⚖️  Bias Impact                : {abs(impact)}%")

    if impact > 5:
        print("🚨 HIGH BIAS DETECTED")
    elif impact > 2:
        print("⚠️  MODERATE BIAS DETECTED")
    else:
        print("✅ LOW BIAS")

    print("\n📋 What was removed:")
    print("   → Candidate name")
    print("   → Email address")
    print("   → Phone number")
    print("   → College/University name")
    print("   → LinkedIn profile")
    print("=" * 50)