def get_missing_skills(resume_skills, job_skills):
    
    resume_skills = [s.lower() for s in resume_skills]
    job_skills = [s.lower() for s in job_skills]
    
    missing = []
    
    for skill in job_skills:
        if skill not in resume_skills:
            missing.append(skill)
    
    return missing


if __name__ == "__main__":
    resume = ["python", "sql", "git"]
    job    = ["python", "sql", "docker", "fastapi"]
    
    missing = get_missing_skills(resume, job)
    print("Missing skills:", missing)