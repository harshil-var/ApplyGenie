# 💼 AI Job Application Assistant - ApplyGenie

An AI-powered job application assistant that analyzes a **job posting and a candidate's resume** to generate personalized application materials.

The application uses **Playwright** to extract information from dynamically rendered job posting pages, **PyPDF** to extract resume content, and **Mistral AI** to generate a personalized application email, cover letter, and concise job summary.

---

## 🚀 Features

* 🔗 **Job URL Analysis**
  Extracts job information from publicly accessible job posting pages using Playwright.

* 📄 **Resume PDF Upload**
  Upload your resume in PDF format and automatically extract its text.

* 📧 **Personalized Application Email**
  Generates a professional email tailored to the job and candidate's resume.

* 📝 **AI Cover Letter Generator**
  Creates a personalized cover letter based on the job requirements and candidate's background.

* 📋 **Job Summary**
  Provides a concise summary of the position, responsibilities, requirements, and important skills.

* ⬇️ **Download Generated Content**
  Download the generated email, cover letter, and job summary as text files.

---

## 🏗️ Project Architecture

```text
                     👤 USER
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
        🔗 Job URL          📄 Resume PDF
             │                   │
             ▼                   ▼
        ┌───────────┐      ┌───────────┐
        │ Playwright│      │   PyPDF   │
        │ Web Scraper│     │PDF Parser │
        └─────┬─────┘      └─────┬─────┘
              │                  │
              ▼                  ▼
        Job Information      Resume Text
              │                  │
              └────────┬─────────┘
                       ▼
                ┌──────────────┐
                │ Mistral AI   │
                │     LLM      │
                └──────┬───────┘
                       │
             ┌─────────┼──────────┐
             ▼         ▼          ▼
          📧 Email   📝 Cover   📋 Job
                     Letter     Summary
             │         │          │
             └─────────┼──────────┘
                       ▼
                ┌─────────────┐
                │  FastAPI    │
                │   Backend   │
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │  Streamlit  │
                │  Frontend   │
                └─────────────┘
```

---

## 🔄 Application Flow

### 1. Enter Job URL

The user provides the URL of a publicly accessible job posting.

### 2. Upload Resume

The user uploads their resume as a PDF.

### 3. Extract Job Information

Playwright opens the job page in a browser and extracts the rendered page content.

The system retrieves information such as:

* Job title
* Job description
* Responsibilities
* Requirements
* Skills
* Qualifications

### 4. Extract Resume Information

PyPDF extracts the text from the uploaded resume.

The extracted content may contain:

* Name
* Education
* Skills
* Projects
* Experience
* Achievements

### 5. AI Processing

The job information and resume content are provided to the Mistral language model.

The model is instructed to use only the information available in the provided data and avoid inventing qualifications or experience.

### 6. Generate Application Materials

The system generates:

```text
📧 Application Email
📝 Cover Letter
📋 Job Summary
```

### 7. Display Results

The generated content is displayed in the Streamlit interface and can be downloaded.

---

## 🛠️ Tech Stack

| Technology        | Purpose                                     |
| ----------------- | ------------------------------------------- |
| **Python**        | Core programming language                   |
| **Streamlit**     | Frontend/UI                                 |
| **FastAPI**       | Backend REST API                            |
| **Playwright**    | Browser automation & job-page extraction    |
| **PyPDF**         | Resume PDF text extraction                  |
| **Mistral AI**    | LLM-powered content generation              |
| **Requests**      | Communication between Streamlit and FastAPI |
| **python-dotenv** | Environment variable management             |

---

## 📁 Project Structure

```text
AI-Job-Application-Assistant/
│
├── backend/
│   ├── main.py
│   └── .env
│
├── frontend/
│   └── streamlit_app.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/AI-Job-Application-Assistant.git
```

Move into the project:

```bash
cd AI-Job-Application-Assistant
```

---

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Install Playwright browser

```bash
python -m playwright install chromium
```

---

## 🔑 Environment Variables

Create a `.env` file inside the `backend` folder:

```text
MISTRAL_API_KEY=your_mistral_api_key
```

Make sure `.env` is included in `.gitignore`.

**Never commit your API key to GitHub.**

---

## ▶️ Running the Application

The application consists of two parts:

* FastAPI backend
* Streamlit frontend

### Start FastAPI

Open a terminal:

```bash
cd backend
```

Run:

```bash
uvicorn main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

### Start Streamlit

Open another terminal:

```bash
streamlit run frontend/streamlit_app.py
```

The Streamlit application will open in your browser.

---

## 🖥️ How to Use

### Step 1

Enter the job posting URL.

### Step 2

Upload your resume in PDF format.

### Step 3

Click:

```text
🚀 Generate Application
```

### Step 4

The application processes the job posting and resume.

### Step 5

View the generated:

```text
📋 Job Summary
📧 Application Email
📝 Cover Letter
```

You can also download each result.

---

## 📤 Example Output

### 📋 Job Summary

```text
Position: AI Engineer

Key Responsibilities:
- Develop machine learning solutions
- Build AI-powered applications
- Work with Python-based technologies

Required Skills:
- Python
- Machine Learning
- FastAPI
- SQL
```

### 📧 Application Email

```text
Dear Hiring Manager,

I am writing to express my interest in the AI Engineer
position. My background in Python, machine learning, and
backend development aligns well with the requirements
of this role...

Best regards,
Candidate Name
```

### 📝 Cover Letter

The system generates a longer, personalized cover letter connecting the candidate's relevant skills and experience with the requirements of the position.

---

## ⚠️ Limitations

* The application is designed for **publicly accessible job postings**.
* Websites requiring login, CAPTCHA, or other access restrictions may not be accessible.
* Job websites can have different page structures, so extraction may vary between websites.
* Image-based/scanned resumes may not contain extractable text.
* AI-generated content should always be reviewed before sending to an employer.
* The system should not be relied upon to verify the accuracy of job postings or resume information.


---

## 🔮 Future Improvements

Potential improvements include:

* 🎯 Job-resume matching score
* 📊 Skill gap analysis
* 💬 LinkedIn message generation
* 📄 DOCX/PDF export
* 🎨 Multiple email and cover-letter tones
* 🌐 Support for additional job websites
* 📑 Better structured job information extraction
* 🧠 Resume section analysis
* 📌 Highlight matched and missing skills

---

## 📌 Key Learning Outcomes

This project demonstrates practical experience with:

* REST API development
* FastAPI
* Streamlit
* Browser automation with Playwright
* PDF processing
* LLM API integration
* Prompt engineering
* Structured LLM outputs
* Frontend-backend communication
* AI-powered text generation

---

## ⭐ Project Goal

The goal of this project is to simplify the job application process by combining **web automation, document processing, and generative AI** into a single application.

Instead of manually reading a job posting and writing application materials from scratch, users can provide their **job URL + resume** and receive personalized application content in seconds.

---

## 👨‍💻 Author

**Harshil Varshney**

If you find this project useful or interesting, consider giving the repository a ⭐.
