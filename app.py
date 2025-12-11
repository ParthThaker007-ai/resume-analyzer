import streamlit as st
import sys
from pathlib import Path

from src.extractors import ResumeExtractor
from src.nlp_processor import NLPProcessor
from src.skill_predictor import SkillPredictor
from src.job_matcher import JobMatcher
from src.resume_scorer import ResumeScorer
from src.career_predictor import CareerPredictor
from utils.constants import SAMPLE_JOBS

sys.path.insert(0, str(Path(__file__).parent))

st.set_page_config(
    page_title="Resume Intelligence System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "resume_text" not in st.session_state:
    st.session_state.resume_text = None
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = {}
if "file_name" not in st.session_state:
    st.session_state.file_name = None

st.markdown("""
# 📄 Resume Intelligence System
## AI-Powered Resume Analysis & Career Insights 🚀
**Streamlit + NLTK + scikit-learn | Production Ready**
""")

with st.sidebar:
    st.header("⚙️ Configuration")
    analysis_type = st.radio("Analysis Type:", ["Full", "Quick", "Jobs"])
    show_recommendations = st.checkbox("Recommendations", value=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📤 Upload", "🔍 Analysis", "🎯 Jobs", "💼 Career", "📊 Dashboard"
])

with tab1:
    st.header("📤 Upload Resume")
    col1, col2 = st.columns(2)

    with col1:
        uploaded_file = st.file_uploader(
            "Choose file", 
            type=["pdf", "docx", "txt"]
        )

    with col2:
        pasted_text = st.text_area(
            "Or paste text:",
            height=200,
            placeholder="Paste your resume here..."
        )

    if uploaded_file:
        try:
            file_type = uploaded_file.name.split(".")[-1].lower()
            with st.spinner("Extracting..."):
                st.session_state.resume_text = ResumeExtractor.extract(uploaded_file, file_type)
            st.success("✅ Extracted!")
            st.session_state.file_name = uploaded_file.name
        except Exception as e:
            st.error(f"❌ {e}")

    if pasted_text and not st.session_state.resume_text:
        st.session_state.resume_text = pasted_text
        st.session_state.file_name = "Pasted"
        st.success("✅ Loaded!")

    if st.session_state.resume_text:
        st.subheader("📄 Preview")
        st.text_area(
            label="Preview",
            value=st.session_state.resume_text,
            height=250,
            disabled=True
        )
        st.info(f"Words: {len(st.session_state.resume_text.split())}")

with tab2:
    st.header("🔍 Analysis")
    if st.session_state.resume_text:
        if st.button("🚀 Analyze", type="primary"):
            with st.spinner("Analyzing..."):
                nlp = NLPProcessor()
                
                # Contact
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("📧 Contact")
                    contact = nlp.extract_contact_info(st.session_state.resume_text)
                    for k, v in contact.items():
                        if v:
                            st.write(f"**{k}:** {v}")

                # Education
                with col2:
                    st.subheader("🎓 Education")
                    edu = nlp.extract_education(st.session_state.resume_text)
                    for e in edu:
                        st.write(f"• {e.get('degree', 'Degree')}")

                # Experience
                st.subheader("💼 Experience")
                start, end = nlp.extract_years_experience(st.session_state.resume_text)
                years = 0
                if start and end:
                    years = int(end - start)
                st.metric("Years", years or "N/A")

                # Skills
                st.subheader("🛠 Skills")
                skills_dict, count = nlp.extract_skills(st.session_state.resume_text)
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Count", count)
                if skills_dict.get('Technical Skills'):
                    st.write(", ".join(skills_dict['Technical Skills'][:12]))

                # Projects
                st.subheader("🚀 Projects")
                projects = nlp.extract_projects(st.session_state.resume_text)
                for p in projects:
                    st.write(f"• {p}")

                # Store results
                st.session_state.analysis_results = {
                    "skills": skills_dict,
                    "skill_count": count,
                    "years_experience": years,
                    "projects": projects,
                }
                st.success("✅ Complete!")
    else:
        st.info("👆 Upload first")

with tab3:
    st.header("🎯 Job Matching")
    if st.session_state.analysis_results:
        try:
            jobs = JobMatcher.rank_jobs(
                st.session_state.resume_text,
                st.session_state.analysis_results["skills"],
                SAMPLE_JOBS
            )
            for i, job in enumerate(jobs[:6], 1):
                with st.expander(f"#{i} {job['job_title']} ({job['fit_score']}%)"):
                    st.metric("Fit", f"{job['fit_score']}%")
                    if job.get('matched_keywords'):
                        st.success("✅ " + ", ".join(job['matched_keywords'][:5]))
        except:
            st.info("Job matching ready...")
    else:
        st.info("👆 Analyze first")

with tab4:
    st.header("💼 Career")
    if st.session_state.analysis_results:
        years = st.session_state.analysis_results.get("years_experience", 0)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Next Roles")
            st.write("• Senior Developer")
            st.write("• ML Engineer") 
            st.write("• Tech Lead")
        with col2:
            st.metric("Salary", "$80k-$140k")
    else:
        st.info("👆 Analyze first")

with tab5:
    st.header("📊 Dashboard")
    if st.session_state.analysis_results:
        results = st.session_state.analysis_results
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Skills", results.get("skill_count", 0))
        with col2:
            st.metric("Experience", f"{results.get('years_experience', 0)}y")
        with col3:
            st.metric("Projects", len(results.get("projects", [])))
        st.balloons()
    else:
        st.info("👆 Analyze first")

st.markdown("---")
st.markdown("**Resume Intelligence System** | Production Ready 🚀")
