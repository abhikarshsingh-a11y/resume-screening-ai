# Resume Screening AI 🤖

An intelligent resume screening system that goes beyond 
keyword matching to fairly evaluate candidates.

## 👥 Team
- Abhikarsh Singh (Person 1) - Resume Parser & Text Processing
- Tashvi Singh (Person 2) - Job Description & Skill Matching

## 🎯 Problem We Are Solving
Traditional ATS (Applicant Tracking Systems) have major flaws:
- Reject good candidates due to keyword mismatch
- Contain built-in bias based on college or name
- Cannot understand meaning — only exact words
- Miss 20-30% of qualified candidates

## 💡 Our Solution
We built a smarter system that:
- Reads and parses any resume format (PDF/DOCX)
- Understands meaning using AI embeddings
- Detects and removes bias from scoring
- Explains WHY a candidate scored high or low

## 🔧 Tech Stack
- Python 3.13
- pdfplumber (PDF reading)
- Sentence Transformers (AI matching)
- FastAPI (Backend API)
- Git & GitHub (Version control)

## 📁 Project Structure
resume-screening-ai/
├── person1_work/
│   ├── read_resume.py      → Reads PDF resume
│   ├── clean_text.py       → Cleans extracted text
│   └── extract_skills.py  → Finds skills from resume
├── person2_work/
│   ├── read_job.py         → Reads job description
│   └── extract_skills.py  → Finds required skills
├── combined/
│   └── matcher.py          → Compares and scores
└── data/                   → Resume PDF files

## 🚀 How To Run
1. Clone the repository
git clone https://github.com/abhikarshsingh-a11y/resume-screening-ai

2. Install requirements
pip install pdfplumber sentence-transformers

3. Run resume parser
cd person1_work
py read_resume.py

## 📅 Weekly Progress
- ✅ Week 1 - Resume parser, text cleaning, skill extraction
- 🔄 Week 2 - Job description parser (in progress)
- ⏳ Week 3 - Semantic matching
- ⏳ Week 4 - Scoring system
- ⏳ Week 5 - Bias detection
- ⏳ Week 6 - API
- ⏳ Week 7 - Final deployment

## 🎓 What We Learned
- PDF text extraction using pdfplumber
- Text cleaning and preprocessing
- Skill extraction using NLP
- Version control with Git

## ⚠️ Current Status
Week 1 Complete — Resume parser working successfully
