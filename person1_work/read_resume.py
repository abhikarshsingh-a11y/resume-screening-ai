import pdfplumber

def read_resume(file_path):
    text = ""
    
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    
    return text


if __name__ == "__main__":
    from clean_text import clean_text
    from extract_skills import extract_skills

    result = read_resume(r"C:\Users\singh\resume-screening-ai\data\resume.pdf")
    print("✅ Step 1 - Resume read")

    cleaned = clean_text(result)
    print("✅ Step 2 - Text cleaned")

    skills = extract_skills(cleaned)
    print("✅ Step 3 - Skills found:")
    print(skills)