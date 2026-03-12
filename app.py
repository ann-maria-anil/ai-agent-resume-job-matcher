import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import streamlit as st
import base64
import pdfplumber
from google import genai
import os
from dotenv import load_dotenv
import json
from docx import Document
import asyncio
from linkedin_agent import open_linkedin_jobs
# ----------------------------
# BACKGROUND IMAGE FUNCTION
# ----------------------------
def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ----------------------------
# CONFIG
# ----------------------------
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

st.set_page_config(
    page_title="Resume Job Matcher",
    layout="centered",
    initial_sidebar_state="collapsed"
)
set_background("Capture.PNG")
# ----------------------------
# DARK THEME + ANIMATION
# ----------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

.main {
    background-color: #0e1117;
    color: #ffffff;
}

h1, h2, h3 {
    color: #4da6ff;
}

.stButton>button {
    background: linear-gradient(90deg, #1f6feb, #388bfd);
    color: white;
    border-radius: 10px;
    padding: 10px 22px;
    font-weight: 600;
    border: none;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg, #388bfd, #1f6feb);
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# HEADER
# ----------------------------
st.title("Resume Job Matcher")
st.markdown("Upload your resume and instantly discover roles aligned with your profile.")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

# ----------------------------
# TEXT EXTRACTION
# ----------------------------
def extract_text(file):
    text = ""

    if file.name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

    elif file.name.endswith(".docx"):
        doc = Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"

    return text


# ----------------------------
# ANALYZE RESUME
# ----------------------------
if uploaded_file:

    text = extract_text(uploaded_file)

    if not text.strip():
        st.error("Could not extract text from file.")
        st.stop()

    st.success("Resume uploaded successfully.")

    if st.button("Analyze Resume"):

        with st.spinner("Analyzing your profile ..."):

            prompt = f"""
Return ONLY valid JSON in this format:

{{
  "profile_summary": "",
  "core_skills": [],
  "primary_roles": [],
  "experience_level": "",
  "industries": []
}}

Resume:
{text[:4000]}
"""

            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                raw_text = response.text

                start = raw_text.find("{")
                end = raw_text.rfind("}") + 1

                if start != -1 and end != -1:
                    json_string = raw_text[start:end]
                    data = json.loads(json_string)
                    st.session_state["resume_data"] = data
                else:
                    st.error("AI response formatting error.")
                    st.write(raw_text)

            except Exception as e:
                st.error(f"Error: {str(e)}")


# ----------------------------
# DISPLAY RESULTS
# ----------------------------
if "resume_data" in st.session_state:

    data = st.session_state["resume_data"]

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### Suggested Roles")
    for role in data.get("primary_roles", []):
        st.markdown(f"- {role}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### Experience Level")
    st.write(data.get("experience_level", ""))
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### Industry Focus")
    for industry in data.get("industries", []):
        st.markdown(f"- {industry}")
    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("🔍 View Detailed Resume Insights"):
        st.markdown("### Profile Summary")
        st.write(data.get("profile_summary", ""))

        st.markdown("### Core Skills")
        for skill in data.get("core_skills", []):
            st.markdown(f"- {skill}")

    st.markdown("---")

    # ----------------------------
    # LINKEDIN BUTTON
    # ----------------------------
    if st.button("🔎 Find Jobs on LinkedIn"):

        roles = data.get("primary_roles", [])
        experience = data.get("experience_level", "")
        industries = data.get("industries", [])

        role_query = " OR ".join(roles[:3]) if roles else ""
        industry = industries[0] if industries else ""

        with st.spinner(" Searching LinkedIn for the best matching roles... Please wait..."):

            asyncio.run(
                open_linkedin_jobs(role_query, experience, industry)
            )