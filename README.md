# 🤖 Resume Screening AI

An AI-based Resume Screening System that analyzes a candidate's resume against a given job description and provides resume matching, skill analysis, missing skills, and bias analysis.

## 📌 Project Overview

The **Resume Screening AI** project is designed to assist in the initial screening of resumes by analyzing the content of a candidate's resume and comparing it with a job description.

The project combines **PDF resume extraction, text preprocessing, skill extraction, semantic similarity, bias analysis, and candidate data management**.

---

## ✨ Features

### 📄 Resume Reading

* Extracts text from PDF resumes.
* Uses `pdfplumber` for PDF text extraction.
* Processes the extracted resume text before analysis.

### 🧹 Text Cleaning

The resume text is cleaned before further processing.

The cleaning process includes:

* Converting text to lowercase
* Removing extra spaces
* Replacing new lines with spaces
* Removing unnecessary double spaces

### 🛠️ Skill Extraction

The system checks resumes and job descriptions for predefined technical and professional skills.

The skill list includes areas such as:

* Python
* Java
* C++
* C
* SQL
* JavaScript
* HTML
* CSS
* Machine Learning
* Deep Learning
* Data Analysis
* Artificial Intelligence
* Cybersecurity
* Digital Forensics
* Networking
* Ethical Hacking
* DSA
* OOP
* Data Structures
* Git
* Docker
* Linux

### 🧠 Semantic Resume Matching

The project uses the **Sentence Transformers** model:

`paraphrase-MiniLM-L3-v2`

The resume and job description are converted into embeddings and compared using **Cosine Similarity**.

This produces a semantic match score between the resume and job description.

### 🎯 Skill Matching

The system identifies:

* Skills found in the resume
* Skills required by the job
* Matched skills
* Missing skills

A skill-based matching score is also calculated by comparing the matched skills with the required job skills.

### ⚖️ Bias Detection

The project includes a bias detection module that compares resume matching scores before and after removing selected personal information.

The following information can be removed during the analysis:

* Candidate name
* Email address
* Phone number
* LinkedIn/profile links
* Selected college/university names

The system calculates:

* Original resume score
* Score after removing personal information
* Bias impact

The difference between the two scores is used to indicate the impact of the removed information on the matching score.

### 💡 Resume Improvement Suggestions

The project contains a module for identifying missing skills and providing learning-resource suggestions for those skills.

It also assigns priority levels to missing skills.

### 🗄️ Candidate Database

The project uses **SQLite** to store candidate information and screening scores.

The database stores:

**Candidate information:**

* Candidate ID
* Name
* Email
* Resume text
* Creation date

**Screening information:**

* Candidate ID
* Job title
* Match score
* Missing skills
* Creation date

### 👨‍💼 Recruiter Dashboard

The project includes a recruiter dashboard for viewing and managing candidate information.

The recruiter functionality includes:

* Viewing candidates
* Viewing candidate match scores
* Finding top candidates
* Viewing candidate screening history
* Viewing missing skills
* Viewing total candidates
* Viewing total applications
* Viewing average screening score
* Deleting candidate records

---

## 🏗️ Project Structure

```text
Resume-Screening-AI/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── resume_screening.db
│
├── combined/
│   ├── match.py
│   └── smart_match.py
│
├── person1_work/
│   ├── bias_detector.py
│   ├── clean_text.py
│   ├── extract_skills.py
│   └── read_resume.py
│
├── person2_work/
│   ├── database.py
│   ├── extract_skills.py
│   ├── read_job.py
│   └── suggestions.py
│
├── frontend/
│   ├── index.html
│   └── recruiter.html
│
├── data/
│   └── resume.pdf
│
├── docker.txt
└── README.md
```

---

## 🔄 Working Flow

```text
Resume PDF
    ↓
Resume Text Extraction
    ↓
Text Cleaning
    ↓
Skill Extraction
    ↓
Resume + Job Description
    ↓
Semantic Matching
    ↓
Match Score
    ↓
Matched Skills + Missing Skills
    ↓
Bias Analysis
    ↓
Candidate Data & Scores
    ↓
Recruiter Dashboard
```

---

## 🧰 Technologies Used

| Technology            | Purpose                     |
| --------------------- | --------------------------- |
| Python                | Core development            |
| FastAPI               | Backend API                 |
| Sentence Transformers | Semantic text matching      |
| Scikit-learn          | Cosine similarity           |
| pdfplumber            | PDF resume extraction       |
| SQLite                | Candidate and score storage |
| HTML                  | Frontend                    |
| CSS                   | Frontend styling            |
| JavaScript            | Frontend functionality      |
| Docker                | Container configuration     |

---

## 📊 Match Analysis

The system provides a semantic match score based on the similarity between:

```text
Resume Content
       ↕
Job Description
```

It also provides separate skill-level information:

```text
Required Skills
       ↓
Matched Skills
       +
Missing Skills
```

---

## ⚖️ Bias Analysis

The bias analysis compares two scores:

```text
Original Resume
       ↓
Original Match Score

        VS

Personal Information Removed
       ↓
Bias-Free Match Score
```

The difference between these scores is reported as the **Bias Impact**.

The project currently checks for the removal of:

```text
Name
Email
Phone Number
LinkedIn / Web Links
Selected University Names
```

> The bias analysis in this project is an experimental comparison of matching scores and is not intended to represent a complete fairness audit.

---

## 👥 Contributors

### Person 1 — Abhikarsh Singh

**Work:**

* Resume PDF reading
* Text cleaning
* Resume skill extraction
* Bias detection
* Semantic matching integration
* Backend integration

### Person 2 — Tashvi Singh

**Work:**

* Job description handling
* Job skill extraction
* SQLite database
* Candidate data management
* Score storage
* Missing-skill suggestions
* Learning-resource suggestions

---

## 🎯 Project Objective

The main objective of this project is to develop a resume screening system that can:

* Compare resumes with job descriptions
* Identify relevant skills
* Detect missing skills
* Calculate semantic matching scores
* Analyze the effect of selected personal information on screening scores
* Store candidate screening information
* Provide recruiters with a candidate management interface

---

## ⚠️ Limitation

The system uses predefined skill lists and a semantic similarity model for resume analysis. The bias component measures score differences after removing selected information and should therefore be considered an **experimental bias indicator**, not a definitive measurement of hiring bias.

---

## 📌 Project Status

**Project Type:** AI-Based Resume Screening System

**Major Components:**

```text
✓ Resume Processing
✓ Text Cleaning
✓ Skill Extraction
✓ Semantic Matching
✓ Missing Skill Detection
✓ Bias Analysis
✓ Candidate Database
✓ Recruiter Dashboard
✓ Resume Improvement Suggestions
```
## 🚧 Current Project Status

**Status:** 🟡 Development Completed / Deployment Pending

The core development of the Resume Screening AI project has been completed, including:

* Resume PDF processing
* Text cleaning
* Skill extraction
* Semantic resume–job matching
* Missing skill detection
* Bias analysis
* Candidate database
* Recruiter dashboard
* Resume improvement suggestions

The project is **currently not deployed** and is being maintained as a local development project.

### 🔜 Next Step

The next stage of the project is to deploy the application so that it can be accessed through a web-based platform.

**Deployment Status:** ⏳ Not deployed yet
