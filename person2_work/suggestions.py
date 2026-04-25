def get_missing_skills(resume_skills, job_skills):
    
    resume_skills = [s.lower() for s in resume_skills]
    job_skills = [s.lower() for s in job_skills]
    
    missing = []
    
    for skill in job_skills:
        if skill not in resume_skills:
            missing.append(skill)
    
    return missing

def suggest_resources(missing_skills):
    
    resource_map = {
        "python"        : "https://python.org/doc",
        "sql"           : "https://sqlzoo.net",
        "docker"        : "https://docs.docker.com",
        "fastapi"       : "https://fastapi.tiangolo.com",
        "git"           : "https://learngitbranching.js.org",
        "javascript"    : "https://javascript.info",
        "html"          : "https://www.w3schools.com/html",
        "css"           : "https://www.w3schools.com/css",
        "machine learning": "https://www.kaggle.com/learn",
        "tensorflow"    : "https://www.tensorflow.org/tutorials",
        "pandas"        : "https://pandas.pydata.org/docs",
        "postgresql"    : "https://www.postgresqltutorial.com",
        "mongodb"       : "https://learn.mongodb.com",
        "aws"           : "https://aws.amazon.com/training",
        "linux"         : "https://linuxjourney.com"
    }
    
    suggestions = []
    
    for skill in missing_skills:
        if skill in resource_map:
            suggestions.append({
                "skill"   : skill,
                "resource": resource_map[skill]
            })
        else:
            suggestions.append({
                "skill"   : skill,
                "resource": "Search on YouTube or Google"
            })
    
    return suggestions


if __name__ == "__main__":
    resume = ["python", "sql", "git"]
    job    = ["python", "sql", "docker", "fastapi", "aws"]
    
    missing     = get_missing_skills(resume, job)
    suggestions = suggest_resources(missing)
    
    print("Missing skills:", missing)
    print("\nSuggestions:")
    for s in suggestions:
        print(f"  Learn {s['skill']} → {s['resource']}")