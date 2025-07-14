import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_resume_with_jobs(resume_text, jobs_csv_path):
    # Load job descriptions from CSV
    jobs_df = pd.read_csv(jobs_csv_path)
    job_descriptions = jobs_df['Details'].tolist()
    job_descriptions.append(resume_text)  # Append resume text for comparison

    Vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = Vectorizer.fit_transform(job_descriptions)
    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()

    jobs_df["Match (%)"] = (cosine_similarities * 100).round(2)
    jobs_df = jobs_df.sort_values(by="Match (%)", ascending=False)
    return jobs_df

    # Combine resume and job descriptions for TF-IDF vectorization
    