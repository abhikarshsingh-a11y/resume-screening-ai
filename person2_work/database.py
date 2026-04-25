import sqlite3

def create_connection():
    # Creates database file if it doesn't exist
    connection = sqlite3.connect("resume_screening.db")
    return connection


def create_tables():
    connection = create_connection()
    
    # cursor is like a pen that writes to database
    cursor = connection.cursor()
    
    # Table 1 — stores candidates
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name      TEXT NOT NULL,
            email     TEXT NOT NULL,
            resume    TEXT NOT NULL,
            created   TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Table 2 — stores scores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id  INTEGER NOT NULL,
            job_title     TEXT NOT NULL,
            match_score   REAL NOT NULL,
            missing_skills TEXT,
            created       TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    connection.commit()
    connection.close()
    print("Database and tables created successfully!")

def save_candidate(name, email, resume_text):
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        INSERT INTO candidates (name, email, resume)
        VALUES (?, ?, ?)
    """, (name, email, resume_text))
    
    # Get the ID of candidate just saved
    candidate_id = cursor.lastrowid
    
    connection.commit()
    connection.close()
    
    print(f"Candidate saved with ID: {candidate_id}")
    return candidate_id


def save_score(candidate_id, job_title, 
               match_score, missing_skills):
    connection = create_connection()
    cursor = connection.cursor()
    
    # Convert list to string for storage
    missing = ", ".join(missing_skills)
    
    cursor.execute("""
        INSERT INTO scores 
        (candidate_id, job_title, match_score, missing_skills)
        VALUES (?, ?, ?, ?)
    """, (candidate_id, job_title, match_score, missing))
    
    connection.commit()
    connection.close()
    print("Score saved successfully!")

def get_all_candidates():
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM candidates")
    candidates = cursor.fetchall()
    
    connection.close()
    return candidates


def get_scores_for_candidate(candidate_id):
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        SELECT * FROM scores 
        WHERE candidate_id = ?
    """, (candidate_id,))
    
    scores = cursor.fetchall()
    connection.close()
    return scores


def get_top_candidates(job_title, limit=5):
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        SELECT candidates.name, candidates.email,
               scores.match_score, scores.missing_skills
        FROM candidates
        JOIN scores ON candidates.id = scores.candidate_id
        WHERE scores.job_title = ?
        ORDER BY scores.match_score DESC
        LIMIT ?
    """, (job_title, limit))
    
    results = cursor.fetchall()
    connection.close()
    return results


if __name__ == "__main__":
    create_tables()
    
    # Show all candidates
    print("\n=== All Candidates ===")
    candidates = get_all_candidates()
    for c in candidates:
        print(c)
    
    # Show top candidates for a job
    print("\n=== Top Candidates: Backend Developer ===")
    top = get_top_candidates("Backend Developer")
    for t in top:
        print(f"Name: {t[0]} | Email: {t[1]} | "
              f"Score: {t[2]}% | Missing: {t[3]}")