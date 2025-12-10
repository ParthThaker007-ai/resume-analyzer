"""Match resume to job descriptions"""

from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class JobMatcher:
    """Match resume against job descriptions"""
    
    @staticmethod
    def calculate_fit_score(resume_text: str, job_description: str) -> float:
        """Calculate how well resume matches job description"""
        vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
        try:
            vectors = vectorizer.fit_transform([resume_text, job_description])
            similarity = cosine_similarity(vectors)
            return round(similarity * 100, 1)
        except:
            return 0.0
    
    @staticmethod
    def match_keywords(resume_skills: Dict[str, List[str]], 
                      job_keywords: List[str]) -> Tuple[List[str], List[str], float]:
        """Match resume skills with job keywords"""
        resume_skill_names = [s.lower() for s in resume_skills.keys()]
        job_keywords_lower = [k.lower() for k in job_keywords]
        
        matched = []
        for job_kw in job_keywords_lower:
            for resume_skill in resume_skill_names:
                if job_kw in resume_skill or resume_skill in job_kw:
                    matched.append(job_kw)
                    break
        
        missing = [kw for kw in job_keywords_lower if kw not in matched]
        match_percentage = (len(matched) / len(job_keywords)) * 100 if job_keywords else 0
        
        return matched, missing, round(match_percentage, 1)
    
    @staticmethod
    def rank_jobs(resume_text: str, resume_skills: Dict, 
                  jobs_list: List[Dict]) -> List[Dict]:
        """Rank jobs by fit score"""
        ranked_jobs = []
        
        for job in jobs_list:
            title = job.get("title", "Unknown")
            keywords = job.get("keywords", [])
            
            fit_score = JobMatcher.calculate_fit_score(resume_text, title)
            matched, missing, keyword_match = JobMatcher.match_keywords(
                resume_skills, keywords
            )
            
            final_score = (fit_score * 0.6) + (keyword_match * 0.4)
            
            ranked_jobs.append({
                "job_title": title,
                "fit_score": round(final_score, 1),
                "text_similarity": fit_score,
                "keyword_match": keyword_match,
                "matched_keywords": matched,
                "missing_keywords": missing,
                "keywords_count": len(keywords),
                "matched_count": len(matched)
            })
        
        ranked_jobs.sort(key=lambda x: x["fit_score"], reverse=True)
        return ranked_jobs
    
    @staticmethod
    def get_improvement_suggestions(missing_keywords: List[str]) -> List[str]:
        """Get suggestions to improve job fit"""
        if not missing_keywords:
            return ["Your resume is well-matched to this role!"]
        
        suggestions = []
        tech_keywords = [k for k in missing_keywords if any(
            x in k.lower() for x in ['python', 'java', 'node', 'react', 'aws']
        )]
        
        if tech_keywords:
            suggestions.append(f"Add technical skills: {', '.join(tech_keywords[:2])}")
        
        other = [k for k in missing_keywords if k not in tech_keywords]
        if other:
            suggestions.append(f"Consider adding: {', '.join(other[:2])}")
        
        return suggestions[:3]
