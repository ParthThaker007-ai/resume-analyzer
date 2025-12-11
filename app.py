import streamlit as st
import sys
from pathlib import Path

# Fix imports for cloud deployment (no spaCy)
from src.extractors import ResumeExtractor
from src.nlp_processor import NLPProcessor  # Handles skills too
from src.skill_predictor import SkillPredictor
from src.job_matcher import JobMatcher
from src.resume_scorer import ResumeScorer
from src.career_predictor import CareerPredictor
from utils.constants import SAMPLE_JOBS

# Ensure imports work when running directly
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

# Global default for years_exp to avoid NameError
years_exp = 0

st.markdown(
    """
# 📄 Resume Intelligence System
## AI-Powered Resume Analysis & Career Insights (NLTK Edition)
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
    st.header("Upload Resume")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Upload File")
        uploaded_file = st.file_uploader(
            "Choose a resume file (PDF, DOCX, TXT)",
            type=["pdf", "docx", "txt"],  # Removed image (no pytesseract)
        )

    with col2:
        st.subheader("or Paste Text")
        pasted_text = st.text_area(
            "Paste resume text here:",
            height=200,
            placeholder="Enter resume content here...",
        )

    if uploaded_file is not None:
        try:
            file_type = uploaded_file.name.split(".")[-1].lower()
            with st.spinner("Extracting text..."):
                st.session_state.resume_text = ResumeExtractor.extract(uploaded_file, file_type)
            st.success("✅ Resume extracted successfully!")
            st.session_state.file_name = uploaded_file.name
        except Exception as e:
            st.error(f"❌ Error extracting file: {str(e)}")

    if pasted_text:
        st.session_state.resume_text = pasted_text
        st.session_state.file_name = "Pasted Text"
        st.success("✅ Text loaded successfully!")

    if st.session_state.resume_text:
        st.subheader("📄 Extracted Resume Text")
        st.text_area(
            "Preview:",
            st.session_state.resume_text,
            height=300,
            disabled=True,
        )
        st.info(f"📊 Word count: {len(st.session_state.resume_text.split())}")

# ----------------------------
# TAB 2: Resume Analysis
# ----------------------------
with tab2:
    if st.session_state.resume_text:
        st.header("🔍 Resume Analysis")

        with st.spinner("🤖 Analyzing resume..."):
            nlp = NLPProcessor()

            col1, col2 = st.columns(2)

            # CONTACT INFO
            with col1:
                st.subheader("📧 Contact Information")
                contact_info = nlp.extract_contact_info(st.session_state.resume_text)
                for key, value in contact_info.items():
                    if value:
                        st.write(f"**{key.title()}:** {value}")

            # EDUCATION
            with col2:
                st.subheader("🎓 Education")
                education = nlp.extract_education(st.session_state.resume_text)
                if education:
                    for edu in education[:3]:
                        if "degree" in edu:
                            st.write(f"• {edu['degree']}")
                else:
                    st.info("No education details found.")

            # EXPERIENCE / YEARS - FIXED
            st.subheader("💼 Experience")
            start_year, end_year = nlp.extract_years_experience(st.session_state.resume_text)
            years_exp = 0  # FIXED: Proper assignment
            if (
                start_year
                and end_year
                and isinstance(start_year, (int, float))
                and isinstance(end_year, (int, float))
            ):
                years_exp = int(end_year - start_year)
            st.metric("Years of Experience", years_exp if years_exp > 0 else "N/A")

            # SKILLS - FIXED
            st.subheader("🛠 Extracted Skills")
            skills_dict, skill_count = nlp.extract_skills(st.session_state.resume_text)

            if skills_dict:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Skills Found", skill_count)
                for category, skills in list(skills_dict.items())[:3]:
                    st.write(f"**{category}**")
                    st.write(", ".join(skills[:8]))
            else:
                st.warning("No skills detected.")

            # PROJECTS
            st.subheader("🚀 Projects")
            projects = nlp.extract_projects(st.session_state.resume_text)
            if projects:
                for p in projects:
                    st.write(f"• {p}")
            else:
                st.info("No projects section detected.")

            # QUALITY SCORE
            try:
                st.subheader("📈 Resume Quality Assessment")
                overall_score, scores = ResumeScorer.calculate_quality_score(
                    st.session_state.resume_text
                )

                col1, col2, col3, col4, col5 = st.columns(5)
                metrics = [
                    ("Length", scores.get("length", 50), col1),
                    ("Structure", scores.get("structure", 50), col2),
                    ("Grammar", scores.get("grammar", 50), col3),
                    ("Keywords", scores.get("keywords", 50), col4),
                    ("Formatting", scores.get("formatting", 50), col5),
                ]
                for name, score, col in metrics:
                    with col:
                        st.metric(name, f"{score:.0f}%")

                st.subheader(f"🎯 Overall Quality Score: {overall_score:.1f}/100")
                feedback = ResumeScorer.get_quality_feedback(scores)
                for msg in feedback[:5]:
                    st.write(f"• {msg}")
            except:
                st.warning("Quality scorer not available.")

            # Store for other tabs
            st.session_state.analysis_results = {
                "contact_info": contact_info,
                "skills": skills_dict,
                "skill_count": skill_count,
                "years_experience": years_exp,
                "quality_score": getattr(scores, 'get', lambda x: 70)(scores, "quality_score", 70),
                "scores": scores if 'scores' in locals() else {},
                "education": education,
                "projects": projects,
            }
    else:
        st.info("👆 Please upload a resume in Tab 1 first.")

# ----------------------------
# TAB 3: Job Matching
# ----------------------------
with tab3:
    if st.session_state.resume_text and st.session_state.analysis_results:
        st.header("🎯 Job Matching Analysis")

        try:
            ranked_jobs = JobMatcher.rank_jobs(
                st.session_state.resume_text,
                st.session_state.analysis_results["skills"],
                SAMPLE_JOBS,
            )

            for idx, job in enumerate(ranked_jobs[:10], 1):
                with st.expander(
                    f"#{idx} {job['job_title']} - Fit Score: {job.get('fit_score', 0)}%",
                    expanded=idx <= 3,
                ):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Overall Fit", f"{job.get('fit_score', 0)}%")
                    with col2:
                        st.metric("Keyword Match", f"{job.get('keyword_match', 0):.1f}%")
                    with col3:
                        st.metric(
                            "Skills Matched",
                            f"{job.get('matched_count', 0)}/{job.get('keywords_count', 1)}",
                        )

                    if job.get("matched_keywords"):
                        st.success("✅ **Matched Keywords:**")
                        st.write(", ".join(job["matched_keywords"][:10]))

                    if job.get("missing_keywords"):
                        st.warning("❌ **Missing Keywords:**")
                        st.write(", ".join(job["missing_keywords"][:7]))
        except:
            st.info("Job matching module loading...")
    else:
        st.info("Please analyze resume in Tab 2 first.")

# ----------------------------
# TAB 4: Career Insights
# ----------------------------
with tab4:
    if st.session_state.analysis_results:
        st.header("💼 Career Trajectory & Growth")

        years_exp_local = st.session_state.analysis_results.get("years_experience", 0)
        skills_dict = st.session_state.analysis_results.get("skills", {})

        col1, col2 = st.columns(2)

        # Predicted skills
        with col1:
            st.subheader("🔮 Predicted Complementary Skills")
            try:
                predicted_skills = SkillPredictor.predict_skills(skills_dict, years_exp_local)
                if predicted_skills:
                    for skill, confidence in predicted_skills[:6]:
                        st.metric(skill, f"{confidence*100:.0f}%")
                else:
                    st.info("No additional skills predicted.")
            except:
                st.info("Skills predictor loading...")

        # Career trajectory & market value
        with col2:
            st.subheader("📈 Career Progression & Market Value")
            try:
                job_titles = CareerPredictor.extract_job_titles(st.session_state.resume_text)
                trajectory = CareerPredictor.predict_trajectory(job_titles, years_exp_local)

                st.write(f"**Current Level:** {trajectory.get('current_level', 'Junior')}")
                if trajectory.get("next_roles"):
                    st.write("**Potential Next Roles:**")
                    for role in trajectory["next_roles"][:3]:
                        st.write(f"• {role}")
                    st.write(f"**Timeline:** {trajectory.get('timeline', '2-4 years')}")

                market = CareerPredictor.estimate_market_value(
                    job_titles, years_exp_local, st.session_state.analysis_results["skill_count"]
                )
                st.metric("💰 Estimated Market Value", market.get("salary_range", "$60k-$100k"))
            except:
                st.info("Career predictor loading...")

        # Growth recommendations
        if show_recommendations:
            st.subheader("🎯 Growth Recommendations")
            try:
                recommendations = CareerPredictor.get_growth_recommendations(
                    trajectory, skills_dict
                )
                for i, rec in enumerate(recommendations[:6], 1):
                    st.write(f"{i}. {rec}")
            except:
                st.info("- Build 3-5 portfolio projects")
                st.info("- Learn Docker & cloud platforms")
                st.info("- Contribute to open source")
    else:
        st.info("Please analyze resume in Tab 2 first.")

# ----------------------------
# TAB 5: Dashboard
# ----------------------------
with tab5:
    if st.session_state.analysis_results:
        st.header("📊 Resume Analytics Dashboard")

        results = st.session_state.analysis_results

        st.subheader("📈 Summary Metrics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🛠 Skills Found", results.get("skill_count", 0))
        with col2:
            st.metric("💼 Experience (Years)", results.get("years_experience", "N/A"))
        with col3:
            st.metric("⭐ Quality Score", f"{results.get('quality_score', 70):.1f}/100")
        with col4:
            label = "Strong" if results.get("quality_score", 0) >= 70 else "Fair"
            st.metric("🎯 Overall Assessment", label)

        st.subheader("📋 Quick Summary")
        st.success(f"""
        ✅ **Skills Detected:** {results.get('skill_count', 0)}  
        ✅ **Experience:** {results.get('years_experience', 0)} years
        ✅ **Quality Score:** {results.get('quality_score', 70):.0f}/100
        ✅ **Projects Found:** {len(results.get('projects', []))}
        """)
    else:
        st.info("Please analyze resume in Tab 2 first.")

st.markdown("---")
st.markdown(
    """
    **Resume Intelligence System v2.0** | Streamlit + NLTK + scikit-learn  
    🚀 Cloud Deployed | No spaCy | Production Ready
    """
)
