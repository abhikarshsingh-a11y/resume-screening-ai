def get_skills_list():
    skills = [
        "python", "java", "javascript", "sql", "r",
        "machine learning", "deep learning", "nlp",
        "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
        "data analysis", "data visualization", "statistics",
        "communication", "teamwork", "problem solving",
        "git", "docker", "linux", "aws", "excel"
    ]
    return skills


def extract_skills(text):
    text = text.lower()

    skills_list = get_skills_list()
    found_skills = []

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return found_skills


if __name__ == "__main__":
    from read_job import get_job_description

    job_text = get_job_description()
    skills = extract_skills(job_text)

    print("\n--- Skills Found in Job Description ---")
    if skills:
        for skill in skills:
            print("-", skill)
    else:
        print("No skills found.")