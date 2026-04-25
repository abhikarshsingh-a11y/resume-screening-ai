import pdfplumber

def read_resume(file_path):
    text = ""
    
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    
    return text


result = read_resume(r"C:\Users\singh\resume-screening-ai\data\resume.pdf")
print(result)


from clean_text import clean_text
from extract_skills import extract_skills

# Step 1 - Read
result = read_resume(r"C:\Users\singh\resume-screening-ai\data\resume.pdf")
print("✅ Step 1 - Resume read")

# Step 2 - Clean
cleaned = clean_text(result)
print("✅ Step 2 - Text cleaned")

# Step 3 - Extract skills
skills = extract_skills(cleaned)
print("✅ Step 3 - Skills found:")
print(skills)