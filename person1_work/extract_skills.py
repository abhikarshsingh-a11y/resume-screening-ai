def extract_skills(text):
    
    # Our skills database
    all_skills = [
        # Programming languages
        "python", "java", "c++", "c", "sql",
        "javascript", "html", "css",
        
        # AI/ML
        "machine learning", "deep learning",
        "data analysis", "artificial intelligence",
        
        # Cybersecurity (matching your background)
        "cybersecurity", "digital forensics",
        "networking", "ethical hacking",
        
        # Concepts
        "dsa", "oop", "data structures",
        
        # Tools
        "git", "docker", "linux"
    ]
    
    found_skills = []
    
    # Check which skills appear in resume
    for skill in all_skills:
        if skill in text:
            found_skills.append(skill)
    
    return found_skills


# Test it
sample_text = "i know python and sql and cybersecurity and dsa"
result = extract_skills(sample_text)
print("Skills found:", result)