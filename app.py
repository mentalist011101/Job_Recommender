import streamlit as st
from src.helper import extract_text_from_pdf,ask_llm
from src.job_api import fetch_linkedin_jobs,fetch_naukri_jobs


st.set_page_config(page_title="Job Recommender", layout="wide")
st.title("Job Recommender ")

st.markdown("Upload your resume and get Job recommendations based on your profile")

uploaded_file = st.file_uploader("Upload your resume {PDF}", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text from Resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    
    with st.spinner("Summarizing your resume..."):
        summary = ask_llm(
            prompt=f"summarize this resume highlighting the skills,education and experience:\n\n {resume_text}",
            max_token=500
        )

    with st.spinner("Finding skill gaps..."):
        gaps = ask_llm(
            prompt=f"Analyse this resume highlighting missing skills,certifications and experiences needed for better Job opportunities:\n\n {resume_text}",
            max_token=400
        )

    with st.spinner("Creating Future Roadmap..."):
        roadmap = ask_llm(
            prompt=f"Based on this resume, suggest a future roadmap to improve this person career prospects(Skill to learn, Certifications needed, industry exposure):\n\n {resume_text}",
            max_token=500
        )

    # display the result
    st.markdown("---")
    st.header("Resume Summary")
    st.markdown(f"<div style='background-color:#000000;padding:15px;border-radius:10px; font-size:16px;color:white;'>{summary}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.header("Skill Gaps and Missing Areas")
    st.markdown(f"<div style='background-color:#000000;padding:15px;border-radius:10px; font-size:16px;color:white;'>{gaps}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.header("Future Roadmap and Preparation strategy")
    st.markdown(f"<div style='background-color:#000000;padding:15px;border-radius:10px; font-size:16px;color:white;'>{roadmap}</div>", unsafe_allow_html=True)

    st.success("Analysis Completed!")

    if st.button("Get Job Recommendation"):
        with st.spinner("Fetching Job Recommendation"):
            key_words = ask_llm(
                prompt=f"Based on this resume summary, suggest the best job titles and keywords for seaching jobs. Give a comma separated list only,no explanation or any other thing:\n\nSummary:{summary}",
                max_token= 100
            )
            search_keywords_clean = key_words.replace("\n", "").strip()

        st.success(f"Extracted Job keywords{search_keywords_clean}") 

        with st.spinner("Fetching Job fromLinked and Naukin"):
            linkedin_jobs = fetch_linkedin_jobs(search_keywords_clean,rows=60)
            naukri_jobs = fetch_naukri_jobs(search_keywords_clean,rows=60)

        st.markdown("---")
        st.header("Top LinkedIn Jobs (France)")

        if linkedin_jobs:
            for job in linkedin_jobs:
                st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                st.markdown(f"- {job.get('location')}")
                st.markdown(f"- [View Job]({job.get('link')})")
                st.markdown("---")
        else:
            st.warning("No linkedIn Jobs found")

        st.markdown("---")
        st.header("Top naukri Jobs (France)")

        if naukri_jobs:
            for job in naukri_jobs:
                st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                st.markdown(f"- {job.get('location')}")
                st.markdown(f"- [View Job]({job.get('link')})")
                st.markdown("---")
        else:
            st.warning("No naukri Jobs found")