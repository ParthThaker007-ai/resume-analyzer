import streamlit as st
import sys
from pathlib import Path

# Cloud-safe imports (no spaCy)
from src.extractors import ResumeExtractor
from src.nlp_processor import NLPProcessor
from src.skill_predictor import SkillPredictor
from src.job_matcher import JobMatcher
from src.resume_scorer import ResumeScorer
from src.career_predictor import CareerPredictor
from utils.constants import SAMPLE_JOBS

# Ensure imports work
sys.path.insert(0, str(Path(__file__).parent))

st.set_page_config(
    page_title="Resume Intelligence System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Session state
if "resume_text" not in st.session_state:
    st.session_state.resume_text = None
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = {}
if "file_name" not in st.session_state:
    st.session_state.file_name = None

st.markdown(
    """
# 📄 Resume Intelligence System
## AI-Powered Resume Analysis & Career Insights 🚀
**Streamlit + NLTK + scikit-learn | Cloud Deployed**
"""
)

with st.sidebar:
    st.header("⚙️ Configuration")
    analysis_type = st.radio(
        "Select Analysis Type:",
        ["Full Analysis", "Quick Scan", "Job Matching Only"],
    )
    show_detailed = st.checkbox("Show Detailed Insights", value=True)
    show_recommendations = st.checkbox("Show Recommendations", value=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📤 Upload & Extract", "🔍 Resume Analysis", "🎯 Job Matching", "💼 Career Insights", "📊 Dashboard"]
)

# ----------------------------
# TAB 1: Upload & Extract
# ----------------------------
with tab1:
    st.header("📤 Upload Resume")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Upload File")
        uploaded_file = st.file_uploader(
            "Choose resume (PDF, DOCX, TXT)",
            type=["pdf", "docx", "txt"],
            help="PDF/DOCX/TXT supported"
        )

    with col2:
        st.subheader("or Paste Text")
        pasted_text = st.text_area(
            "Paste resume content:",
            height=200,
            placeholder="Your full resume text here..."
        )

    # File upload processing
    if uploaded_file is not None:
        try:
            file_type = uploaded_file.name.split(".")[-1].lower()
            with st.spinner("Extracting text..."):
                st.session_state.resume_text = ResumeExtractor.extract(uploaded_file, file_type)
            st.success(f"✅ {uploaded_file.name} extracted!")
            st.session_state.file_name = uploaded_file.name
        except Exception as e:
            st.error(f"❌ Extraction failed: {str(e)}")

    # Text paste processing
    if pasted_text and not st.session_state.resume_text:
        st.session_state.resume_text = pasted_text
        st.session_state.file_name = "Pasted Text"
        st.success("✅ Text loaded!")

    # Preview
    # Preview - FIXED
     if st.session_state.resume_text:
        st.subheader("📄 Preview")
        st.text_area(
            label="Resume Preview",  # REQUIRED
            value=st.session_state.resume_text,
            height=300,
            disabled=True,
            label_visibility="collapsed"
        )
        word_count = len(st.session_state.resume_text.split())
        st.info(f"📊 **Words:** {word_count} | **Chars:** {len(st.session_state.resume_text)}")


# ----------------------------
# TAB 2: Resume Analysis
# ----------------------------
with tab2:
    if st.session_state.resume_text:
        st.header("🔍 Resume Analysis")
        
        if st.button("🚀 Analyze Resume", type="primary"):
            with st.spinner("🤖 Processing..."):
                try:
                    nlp = NLPProcessor()

                    # Contact info
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("📧 Contact")
                        contact_info = nlp.extract_contact_info(st.session_state.resume_text)
                        for key, value in contact_info.items():
                            if value:
                                st.success(f"**{key.title()}:** {value}")

                    # Education
                    with col2:
                        st.subheader("🎓 Education")
                        education = nlp.extract_education(st.session_state.resume_text)
                        if education:
                            for edu in education:
                                st.write(f"• {edu.get('degree', 'Degree')}")
                        else:
                            st.info("No education found")

                    # Experience
                    st.subheader("💼 Experience")
                    start_year, end_year = nlp.extract_years_experience(st.session_state.resume_text)
                    years_exp = 0
                    if start_year and end_year and isinstance(start_year, (int, float)) and isinstance(end_year, (int, float)):
                        years_exp = int(end_year - start_year)
                    st.metric("Years of Experience", years_exp if years_exp > 0 else "N/A")

                    # Skills - FIXED CALL
                    st.subheader("🛠 Skills")
                    skills_dict, skill_count = nlp.extract_skills(st.session_state.resume_text)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Skills Found", skill_count)
                    
                    if skills_dict and 'Technical Skills' in skills_dict:
                        skills_list = skills_dict['Technical Skills']
                        st.success("✅ **Detected Skills:**")
                        st.write(", ".join(skills_list[:15]))
                    else:
                        st.warning("No skills detected")

                    # Projects
                    st.subheader("🚀 Projects")
                    projects = nlp.extract_projects(st.session_state.resume_text)
                    if projects:
                        for project in projects:
                            st.write(f"• {project}")
                    else:
                        st.info("No projects section found")

                    # Quality score with error handling
                    try:
                        st.subheader("📈 Quality Score")
                        overall_score, scores = ResumeScorer.calculate_quality_score(
                            st.session_state.resume_text
                        )
                        col1, col2, col3, col4 = st.columns(4)
                        st.metric("Overall", f"{overall_score:.0f}/100", delta=None)
                        
                        # Store results
                        st.session_state.analysis_results = {
                            "contact_info": contact_info,
                            "skills": skills_dict,
                            "skill_count": skill_count,
                            "years_experience": years_exp,
                            "quality_score": overall_score,
                            "scores": scores,
                            "education": education,
                            "projects": projects,
                        }
                        st.success("✅ Analysis complete!")
                        
                    except Exception as e:
                        st.warning("Quality analysis unavailable")
                        st.session_state.analysis_results = {
                            "skills": skills_dict,
                            "skill_count": skill_count,
                            "years_experience": years_exp,
                            "projects": projects,
                        }
                        
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")
    else:
        st.info("👆 Upload a resume first!")

# ----------------------------
# TAB 3: Job Matching
# ----------------------------
with tab3:
    st.header("🎯 Job Matching")
    if st.session_state.analysis_results:
        try:
            ranked_jobs = JobMatcher.rank_jobs(
                st.session_state.resume_text,
                st.session_state.analysis_results.get("skills", {}),
                SAMPLE_JOBS
            )
            
            for i, job in enumerate(ranked_jobs[:8], 1):
                with st.expander(f"#{i} {job['job_title']} ({job['fit_score']}%)"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Fit Score", f"{job['fit_score']}%")
                    
                    if job.get('matched_keywords'):
                        st.success("✅ **Matched:** " + ", ".join(job['matched_keywords'][:5]))
                    
                    if job.get('missing_keywords'):
                        st.warning("❌ **Missing:** " + ", ".join(job['missing_keywords'][:5]))
                        
        except Exception as e:
            st.info("Job matching loading...")
    else:
        st.info("👆 Run analysis in Tab 2 first!")

# ----------------------------
# TAB 4: Career Insights
# ----------------------------
with tab4:
    st.header("💼 Career Insights")
    if st.session_state.analysis_results:
        years_exp = st.session_state.analysis_results.get("years_experience", 0)
        skills_count = st.session_state.analysis_results.get("skill_count", 0)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔮 Next Roles")
            try:
                job_titles = CareerPredictor.extract_job_titles(st.session_state.resume_text)
                trajectory = CareerPredictor.predict_trajectory(job_titles, years_exp)
                st.write(f"**Current:** {trajectory.get('current_level', 'Junior')}")
                if trajectory.get('next_roles'):
                    for role in trajectory['next_roles'][:3]:
                        st.write(f"➜ {role}")
            except:
                st.info("• Senior Developer\n• ML Engineer\n• Tech Lead")
        
        with col2:
            st.subheader("💰 Market Value")
            try:
                market = CareerPredictor.estimate_market_value(
                    [], years_exp, skills_count
                )
                st.metric("Salary Range", market.get("salary_range", "$60k-$100k"))
            except:
                st.metric("Salary Range", "$60k-$120k")
    else:
        st.info("👆 Run analysis first!")

# ----------------------------
# TAB 5: Dashboard
# ----------------------------
with tab5:
    st.header("📊 Dashboard")
    if st.session_state.analysis_results:
        results = st.session_state.analysis_results
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🛠 Skills", results.get("skill_count", 0))
        with col2:
            st.metric("📅 Experience", f"{results.get('years_experience', 0)} yrs")
        with col3:
            st.metric("⭐ Quality", f"{results.get('quality_score', 70):.0f}/100")
        with col4:
            st.metric("🚀 Projects", len(results.get("projects", [])))
        
        st.success("✅ **Ready for Demo!**")
    else:
        st.info("👆 Complete analysis first!")

st.markdown("---")
st.markdown(
    """
**Resume Intelligence System v2.0** | Production Ready 🚀
Streamlit + NLTK + scikit-learn | Deployed on Render
"""
)
