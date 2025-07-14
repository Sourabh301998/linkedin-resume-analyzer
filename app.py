from src.ai_utils import generate_resume_summary, extract_skills_from_resume, evaluate_job_fit
import streamlit as st
import pandas as pd
import os
import requests
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
from PIL import Image
from streamlit_lottie import st_lottie
from src.analyzer import extract_text_from_pdf
from src.matcher import match_resume_with_jobs
from openai import OpenAIError

# ---------- Page Config ----------
st.set_page_config(page_title="LinkedIn Resume Analyzer", page_icon="assets/favicon.ico", layout="wide")

# ---------- Styling ----------
st.markdown("""
<style>
body, .stApp {
    background-color: white !important;
    color: black !important;
}
.block-container {
    background-color: white !important;
    padding: 2rem 1rem;
}
.topnav {
    position: fixed;
    top: 0;
    width: 100%;
    background-color: #003366;
    overflow: hidden;
    z-index: 999;
}
.topnav a {
    float: left;
    display: block;
    color: #ffffff;
    text-align: center;
    padding: 14px 24px;
    text-decoration: none;
    font-size: 16px;
    font-family: 'Montserrat', sans-serif;
}
.topnav a:hover {
    background-color: #005999;
}
.stApp {
    margin-top: 60px !important;
}
.header-container {
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 30px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}
.glow-title {
    font-family: 'Montserrat', sans-serif;
    font-size: 40px;
    color: #003366;
    margin: 0;
}
.upload-label, .checkbox-label {
    font-size: 18px;
    font-weight: 600;
    color: black !important;  /* ✅ Fixes the visibility */
    font-family: 'Montserrat', sans-serif;
    margin-bottom: 8px;
    display: block;
}
.stAlert > div, .stSpinner, .stMarkdown, .css-1v0mbdj p, .css-1v0mbdj span {
    color: black !important;
}
div.stDownloadButton > button {
    background-color: #0072b1;
    color: white;
    font-weight: 600;
    font-family: 'Montserrat', sans-serif;
    border-radius: 8px;
    padding: 10px 20px;
    border: none;
}
div.stDownloadButton > button:hover {
    background-color: #005999;
}
.custom-skill-box {
    background-color: #f1f5f9;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #d0d7de;
    margin-bottom: 20px;
    font-family: 'Montserrat', sans-serif;
    color: #003366;
}
footer {visibility: hidden;}
.custom-footer {
    position: relative;
    bottom: 0px;
    width: 100%;
    background-color: #f8f9fa;
    color: #333;
    text-align: center;
    font-size: 14px;
    padding: 8px 16px;
    border-top: 1px solid #ddd;
    z-index: 100;
    font-family: 'Montserrat', sans-serif;
    margin-top: 50px;
}
.custom-footer a {
    text-decoration: none;
    color: #0072b1;
    font-weight: 500;
    margin: 0 6px;
}
.custom-footer a:hover {
    color: #00BFFF;
    text-decoration: underline;
}
.stCheckbox > div, .stMarkdown, .stSpinner {
    color: #003366 !important;                      
}
</style>
<div class="topnav">
  <a href="#upload">Upload</a>
  <a href="#insights">Insights</a>
  <a href="#matches">Top Matches</a>
  <a href="https://github.com/Sourabh301998" target="_blank">GitHub</a>
</div>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<div class="header-container">
    <h1 class="glow-title">LinkedIn Resume Analyzer</h1>
</div>
""", unsafe_allow_html=True)

# ---------- Lottie ----------
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_url = "https://assets3.lottiefiles.com/packages/lf20_4kx2q32n.json"
lottie_resume = load_lottie_url(lottie_url)

st.markdown("""
<style>
.lottie-container {
    background-color: #f8f9fa;
    border: 1px solid #d0d7de;
    border-radius: 12px;
    padding: 25px;
    margin-bottom: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}
.lottie-desc {
    font-size: 15px;
    font-family: 'Montserrat', sans-serif;
    text-align: center;
    color: #333333;
    margin-top: 6px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

if lottie_resume:
    st.markdown('<div class="lottie-container">', unsafe_allow_html=True)
    st_lottie(lottie_resume, height=220, key="resume")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<p class="lottie-desc">💡 Intelligent AI Assistant evaluating your resume with GPT</p>', unsafe_allow_html=True)

# ---------- Uploads ----------
st.markdown('<a name="upload"></a>', unsafe_allow_html=True)
st.markdown('<span class="upload-label">📄 Upload your Resume (PDF)</span>', unsafe_allow_html=True)
uploaded_resume = st.file_uploader("", type=["pdf"])

st.markdown('<span class="upload-label">📊 Upload Job Dataset (CSV)</span>', unsafe_allow_html=True)
uploaded_jobs = st.file_uploader("", type=["csv"])

st.markdown('<span class="checkbox-label">🧠 Use OpenAI API (uncheck for offline demo)</span>', unsafe_allow_html=True)
use_openai = st.checkbox("", value=True)



# ---------- Resume Analysis ----------
resume_text = summary = ""
skills, matched_df = [], pd.DataFrame()
analysis_done = False

if uploaded_resume and uploaded_jobs:
    with open("resume/temp_resume.pdf", "wb") as f:
        f.write(uploaded_resume.read())
    with open("data/temp_jobs.csv", "wb") as f:
        f.write(uploaded_jobs.read())

    with st.spinner("🔍 Analyzing your resume..."):
        resume_text = extract_text_from_pdf("resume/temp_resume.pdf")
        matched_df = match_resume_with_jobs(resume_text, "data/temp_jobs.csv")
        matched_df = matched_df.rename(columns={"details": "Details"})
        analysis_done = True

if analysis_done:
    st.success("✅ Resume analysis complete!")
else:
    st.warning("⚠️ Please upload both a resume and a job dataset to start the analysis.")

# ---------- Insights ----------
if analysis_done and resume_text:
    st.markdown('<a name="insights"></a>', unsafe_allow_html=True)
    st.subheader("📄 AI Resume Insights")

    with st.spinner("🧠 Generating AI summary..."):
        if use_openai:
            try:
                summary = generate_resume_summary(resume_text)
            except OpenAIError as e:
                summary = f"❌ Failed to generate summary: {str(e)}"
        else:
            summary = "📝 Sample summary: Strong Python, ML, and data science skills."

    st.markdown(f'<div class="custom-skill-box">{summary}</div>', unsafe_allow_html=True)

    with st.spinner("🛠️ Extracting skills..."):
        if use_openai:
            try:
               skills = extract_skills_from_resume(resume_text)
            except OpenAIError as e:
               skills = [f"❌ Failed to extract skills: {str(e)}"]
        else:
            skills = ["Python", "Data Analysis", "Machine Learning"]

st.markdown(f'<div class="custom-skill-box">{", ".join(skills)}</div>', unsafe_allow_html=True)

# ---------- Job Matches ----------
st.markdown('<a name="matches"></a>', unsafe_allow_html=True)
st.subheader("💼 Top Matching Jobs")
for index, row in matched_df.head(5).iterrows():
    st.markdown(f"### 🔹 {row['Job Title']} ({row['Match (%)']}%)")
    st.write(row['Details'])

    if use_openai:
        with st.expander("🤖 AI Feedback: Am I a Good Fit?"):
            try:
                feedback = evaluate_job_fit(resume_text, row['Details'])
                st.write(feedback)
            except OpenAIError as e:
                st.error(f"❌ Fit evaluation failed: {str(e)}")

# ---------- Visualizations ----------
st.subheader("📊 Match Score Visualization")
top_jobs = matched_df.sort_values(by="Match (%)", ascending=False).head(5)
fig, ax = plt.subplots(figsize=(2, 2))
ax.barh(top_jobs["Job Title"], top_jobs["Match (%)"], color="#0072b1")
ax.set_xlabel("Match Percentage")
ax.set_title("Top 5 Matching Job Roles")
ax.invert_yaxis()
st.pyplot(fig)

st.subheader("📈 Match Score Distribution")
fig2, ax2 = plt.subplots(figsize=(2, 2))
ax2.hist(matched_df["Match (%)"], bins=10, color="#005999", edgecolor='black')
ax2.set_xlabel("Match %")
ax2.set_ylabel("Number of Jobs")
ax2.set_title("Distribution of Match Scores")
st.pyplot(fig2)

st.subheader("📌 Match Share by Job Title")
fig3, ax3 = plt.subplots(figsize=(2, 2))
ax3.pie(top_jobs["Match (%)"], labels=top_jobs["Job Title"], autopct="%1.1f%%", startangle=140, colors=plt.cm.Paired.colors)
ax3.axis('equal')
st.pyplot(fig3)

st.subheader("🔤 Word Cloud of Job Descriptions")
all_descriptions = " ".join(matched_df["Details"].astype(str).tolist())
wordcloud = WordCloud(width=400, height=400, background_color="white").generate(all_descriptions)
fig4, ax4 = plt.subplots(figsize=(2, 2))
ax4.imshow(wordcloud, interpolation='bilinear')
ax4.axis("off")
st.pyplot(fig4)

st.subheader("📊 Extracted Skill Frequency")
skill_counts = Counter(skills)
fig5, ax5 = plt.subplots(figsize=(2, 2))
ax5.bar(skill_counts.keys(), skill_counts.values(), color="#ff6600")
ax5.set_ylabel("Frequency")
ax5.set_title("Skills Extracted from Resume")
ax5.set_xticklabels(skill_counts.keys(), rotation=30)
st.pyplot(fig5)

# ---------- Download ----------
csv = matched_df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Full Match Report", data=csv, file_name="match_results.csv", mime="text/csv")

# ---------- Footer ----------
st.markdown("""
<div class="custom-footer">
    © 2025 <strong>Sourabh Ranbhise</strong> · AI Resume Analyzer · 
    <a href="https://www.linkedin.com/in/sourabh-ranbhise-67a4ba257/" target="_blank">LinkedIn</a> |
    <a href="https://github.com/Sourabh301998" target="_blank">GitHub</a> ·
    Powered by <strong>OpenAI GPT</strong>
</div>
""", unsafe_allow_html=True)
