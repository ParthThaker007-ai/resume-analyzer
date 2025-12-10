"""Predict career trajectory and growth recommendations"""

from typing import Dict, List, Tuple
import re


class CareerPredictor:
    """Predict career trajectory and market value."""

    # Simple progression templates
    TECH_PROGRESSIONS = {
        "Junior Developer": {
            "next_roles": ["Senior Developer", "Full Stack Developer", "Tech Lead"],
            "years_to_next": (1, 3),
        },
        "Senior Developer": {
            "next_roles": ["Tech Lead", "Engineering Manager", "Architect"],
            "years_to_next": (2, 4),
        },
        "Data Scientist": {
            "next_roles": ["Senior Data Scientist", "ML Engineer", "Manager"],
            "years_to_next": (2, 3),
        },
        "ML Engineer": {
            "next_roles": ["Senior ML Engineer", "ML Architect", "AI Lead"],
            "years_to_next": (2, 4),
        },
    }

    @staticmethod
    def extract_job_titles(resume_text: str) -> List[str]:
        """Very simple heuristic job-title extractor from resume text."""
        job_titles: List[str] = []
        # Look for common role keywords
        patterns = [
            r"(Junior\s+Developer)",
            r"(Senior\s+Developer)",
            r"(Data\s+Scientist)",
            r"(ML\s+Engineer)",
            r"(Machine\s+Learning\s+Engineer)",
            r"(Software\s+Engineer)",
            r"(Backend\s+Developer)",
            r"(Frontend\s+Developer)",
            r"(Full\s*Stack\s+Developer)",
            r"(Engineering\s+Manager)",
            r"(Tech\s+Lead)",
            r"(Architect)",
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, resume_text, re.IGNORECASE)
            for match in matches:
                title = match.group(0).strip()
                if title not in job_titles:
                    job_titles.append(title)

        return job_titles[:5]

    @staticmethod
    def predict_trajectory(job_titles: List[str], years_experience: int) -> Dict:
        """Predict career trajectory dictionary given job titles and experience."""
        trajectory = {
            "current_level": "Unknown",
            "next_roles": [],
            "timeline": None,
        }

        if not job_titles:
            return trajectory

        # Try to map detected title to one of our progression templates
        best_match = None
        normalized_titles = [t.lower() for t in job_titles]

        for prog_title in CareerPredictor.TECH_PROGRESSIONS.keys():
            for resume_title in normalized_titles:
                if prog_title.lower().split()[0] in resume_title:
                    best_match = prog_title
                    break
            if best_match:
                break

        # Fallbacks if nothing matches
        if best_match is None:
            # crude guess based on years_experience
            if years_experience < 2:
                best_match = "Junior Developer"
            elif years_experience < 5:
                best_match = "Senior Developer"
            else:
                best_match = "Senior Developer"

        progression = CareerPredictor.TECH_PROGRESSIONS.get(best_match)
        trajectory["current_level"] = best_match

        if progression:
            trajectory["next_roles"] = progression["next_roles"]
            min_years, max_years = progression["years_to_next"]
            # Adjust based on current experience
            if years_experience <= 0:
                timeline = f"{min_years}-{max_years} years"
            else:
                timeline = f"{max(1, min_years - 1)}-{max_years} years"
            trajectory["timeline"] = timeline

        return trajectory

    @staticmethod
    def estimate_market_value(
        job_titles: List[str], years_experience: int, skills_count: int
    ) -> Dict:
        """Rough market value estimation in USD based on level, experience, and skills."""
        salary_ranges = {
            "Junior": (40, 70),
            "Mid-level": (70, 120),
            "Senior": (120, 180),
            "Lead": (150, 220),
        }

        # Infer level from experience
        if years_experience < 2:
            level = "Junior"
        elif years_experience < 5:
            level = "Mid-level"
        elif years_experience < 8:
            level = "Senior"
        else:
            level = "Lead"

        base_min, base_max = salary_ranges.get(level, (60, 100))

        # Simple skill-based multiplier
        skill_boost = min(1.5, 1.0 + (skills_count * 0.03))
        adjusted_min = int(base_min * skill_boost)
        adjusted_max = int(base_max * skill_boost)

        return {
            "level": level,
            "salary_range": f"${adjusted_min}k - ${adjusted_max}k",
            "currency": "USD",
        }

    @staticmethod
    def get_growth_recommendations(
        trajectory: Dict, skills: Dict[str, list]
    ) -> List[str]:
        """Generate career growth recommendations based on trajectory and skills."""
        current = trajectory.get("current_level", "Unknown").lower()
        skill_names = {s.lower() for s in skills.keys()}

        recs: List[str] = []

        # Base generic recommendations
        recs.append("Contribute to 2–3 real-world or open-source projects.")
        recs.append("Create a strong portfolio (GitHub/portfolio site) showcasing end-to-end work.")
        recs.append("Improve communication and documentation skills for better teamwork.")

        # Role-specific hints
        if "junior" in current:
            recs.append("Deepen fundamentals in data structures, algorithms, and system design.")
            recs.append("Pair with seniors for code reviews and mentorship at least once a week.")
        elif "senior" in current:
            recs.append("Take ownership of modules/features and mentor at least one junior.")
            recs.append("Start learning high-level architecture and trade-offs for production systems.")
        elif "manager" in current or "lead" in current:
            recs.append("Focus on leadership, stakeholder communication, and roadmap planning.")
            recs.append("Invest in hiring, interviewing, and team development skills.")

        # Skill-based hints
        if "python" in skill_names and "machine learning" in skill_names:
            recs.append("Build end-to-end ML pipelines including deployment and monitoring.")
        if "docker" not in skill_names:
            recs.append("Learn Docker for reproducible environments and deployments.")
        if "kubernetes" not in skill_names and "docker" in skill_names:
            recs.append("Explore Kubernetes for scalable microservice deployments.")
        if "cloud" not in skill_names and not any(
            k in skill_names for k in ["aws", "azure", "gcp"]
        ):
            recs.append("Pick one cloud platform (AWS/Azure/GCP) and complete one hands-on project.")

        # De-duplicate while preserving order
        seen = set()
        final_recs: List[str] = []
        for r in recs:
            if r not in seen:
                seen.add(r)
                final_recs.append(r)

        # Limit to 6 recommendations for UI
        return final_recs[:6]
