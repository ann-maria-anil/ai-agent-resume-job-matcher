#  AI Resume Job Matcher

An AI-powered web application that analyzes resumes and suggests relevant job roles, then automatically searches for matching job listings on LinkedIn.

This project combines **Generative AI**, **resume parsing**, and **browser automation** to help users quickly discover job opportunities aligned with their skills and experience.

---

## Features

* Upload resume in **PDF or DOCX format**
* Automatic **resume text extraction**
* **AI-powered profile analysis** using Gemini
* Identifies:

  * Core skills
  * Suitable job roles
  * Experience level
  * Relevant industries
* One-click **LinkedIn job search automation**

---

## Technologies Used

* **Streamlit** – Web application UI
* **Gemini AI** – Resume analysis
* **pdfplumber** – Extract text from PDF resumes
* **python-docx** – Extract text from Word documents
* **Browser Use automation agent** – LinkedIn job search
* **Python** – Core application logic

---

##  System Architecture

1. User uploads resume
2. Resume text is extracted
3. AI analyzes the resume using Gemini
4. Structured profile is generated
5. Suitable job roles are identified
6. LinkedIn automation searches for relevant jobs

---


## Installation

Clone the repository:

git clone https://github.com/ann-maria-anil/ai-agent-resume-job-matcher.git

Navigate to the project folder:

cd ai-resume-job-matcher

Install dependencies:

pip install -r requirements.txt

---

##  Environment Variables

Create a `.env` file and add your API keys:

GOOGLE_API_KEY=your_gemini_api_key
BROWSER_USE_API_KEY=your_browser_use_key

---

## Run the Application

Start the Streamlit server:

streamlit run app.py

The application will run at:

http://localhost:8501

---

##  Deployment

The application can be deployed easily using **Streamlit Cloud**.

Steps:

1. Push the project to GitHub
2. Login to Streamlit Cloud
3. Select your repository
4. Deploy using `app.py`

---

## Future Improvements

* Resume skill gap analysis
* Job recommendation ranking
* Multi-platform job search (LinkedIn, Indeed, Glassdoor)
* Direct job application automation

---


