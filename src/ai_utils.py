import streamlit as st
from openai import OpenAI

# ✅ Load OpenAI key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 1. Resume Summary
def generate_resume_summary(resume_text):
    prompt = f"Summarize this resume:\n\n{resume_text}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# 2. Extract Skills
def extract_skills_from_resume(resume_text):
    prompt = (
        f"Extract a list of technical and soft skills from the following resume:\n\n{resume_text}\n\n"
        "Return the result as a comma-separated list."
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# 3. Evaluate Job Fit
def evaluate_job_fit(resume_text, job_description):
    try:
        prompt = (
            f"Evaluate how well this resume matches the job description.\n\n"
            f"Resume:\n{resume_text}\n\nJob Description:\n{job_description}\n\n"
            "Return a score out of 10 and a short explanation."
        )
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error during evaluation: {str(e)}"
