# 📄 LinkedIn Resume Analyzer with OpenAI GPT

A powerful AI-powered Streamlit web app that analyzes your resume against job descriptions using GPT.  
Get summaries, extracted skills, match scores, and job-fit insights — all in a clean UI with animations and visualizations.

---

## 🚀 Features

- 📄 Upload your **Resume (PDF)** and **Job Dataset (CSV)**
- 🤖 Generate **AI-powered resume summary**
- 🛠️ Extract **technical and soft skills**
- 💼 View **Top Matching Jobs** with % match score
- 🧠 GPT-powered **"Am I a Good Fit?"** evaluation
- 📈 Integrated **charts & visualizations**
- 🎨 Professional UI with tabs, icons, and Lottie animations

---

## 📁 Project Structure

linkedin-resume-analyzer/
├── app.py # Streamlit app
├── requirements.txt
├── .env.template # Template for OpenAI key
├── README.md
├── assets/ # Logo and favicon
├── resume/ # Uploaded resumes
├── data/ # Uploaded job data
└── src/
├── ai_utils.py # GPT functions
├── analyzer.py # Resume text extractor
└── matcher.py # Resume ↔ job matcher



---

## 🌟 Key Benefits

- 🤖 **AI-Powered Insights:** Get personalized, GPT-generated resume feedback.
- 🎯 **Job Matching:** Discover your top-fit jobs with intelligent match scores.
- 💡 **Visual Feedback:** Understand skill gaps and strengths through charts.
- 🔒 **Privacy First:** Your data stays local — no external storage.
- ⚙️ **Customizable:** Works with any job dataset or resume format.

---

## 💻 Local Setup (Installation)

```bash
# 1. Clone the repo
git clone https://github.com/Sourabh301998/linkedin-resume-analyzer.git
cd linkedin-resume-analyzer

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup .env
cp .env.template .env  # Then add your OpenAI API key

# 5. Run the app
streamlit run app.py

-------

Streamlit Cloud Deployment
Push your project to GitHub
----

##🌐 Go to streamlit.io/cloud

Click New App → Choose your repo → app.py

Add OPENAI_API_KEY in Secrets

Click Deploy 🚀

----

##📊 Example Visuals
🧠 AI Summary Box

🛠️ Skill List

💼 Top 5 Job Matches

📈 Match Score Bar Chart

📥 Downloadable CSV Report

--- 

##📌 Sample Job Dataset (CSV Format)
Job Title,details
Data Scientist,"Looking for Python, ML, pandas, statistics."
ML Engineer,"Expert in PyTorch, NLP, scalable ML."
Data Analyst,"Needs Excel, SQL, Tableau, data visualization."
AI Developer,"LLMs, Generative AI, LangChain, Prompt Engineering"

--------

##🧠 Built With
OpenAI GPT-3.5 Turbo

Streamlit

[matplotlib, pandas, PyPDF2, dotenv, streamlit-lottie]

----------

##👨‍💻 Author
Sourabh Ranbhise
🔗 LinkedIn |
🐙 GitHub

----------

##📜 License
MIT License – feel free to use and modify.

-------------