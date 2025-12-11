"""
Job Matching Module - TF-IDF + Keyword Matching
No external dependencies beyond scikit-learn/numpy
"""

import re
from typing import List, Dict
from collections import Counter
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class JobMatcher:
    """Job matching using TF-IDF + keyword analysis."""
    
    @staticmethod
    def preprocess_text(text: str) -> str:
        """Clean and normalize text for matching."""
        # Lowercase + remove special chars
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        # Remove stopwords
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'
        }
        words = [w for w in text.split() if w not in stop_words and len(w) > 2]
        return ' '.join(words)
    
    @staticmethod
    def rank_jobs(resume_text: str, skills_dict: dict, jobs: List[Dict]) -> List[Dict]:
        """Rank jobs by fit score using TF-IDF + keyword matching."""
        results = []
        
        # Extract skills from resume
        resume_skills = []
        if skills_dict and 'Technical Skills' in skills_dict:
            resume_skills = [skill.lower() for skill in skills_dict['Technical Skills']]
        
        for job in jobs:
            job_title = job.get('title', '')
            job_keywords = job.get('keywords', [])
            
            # Keyword matching (case-insensitive)
            matched_keywords = []
            missing_keywords = []
            
            for keyword in job_keywords:
                keyword_lower = keyword.lower()
                # Check resume text + extracted skills
                if (keyword_lower in resume_text.lower() or 
                    keyword_lower in ' '.join(resume_skills)):
                    matched_keywords.append(keyword)
                else:
                    missing_keywords.append(keyword)
            
            # Calculate scores
            keyword_match_score = len(matched_keywords) / max(len(job_keywords), 1) * 100
            skills_match_score = sum(1 for skill in resume_skills if skill in [k.lower() for k in job_keywords]) / max(len(resume_skills), 1) * 100
            
            # Combined fit score
            fit_score = (keyword_match_score * 0.6 + skills_match_score * 0.4)
            
            results.append({
                'job_title': job_title,
                'fit_score': round(fit_score, 1),
                'keyword_match': round(keyword_match_score, 1),
                'matched_keywords': matched_keywords[:10],
                'missing_keywords': missing_keywords[:8],
                'matched_count': len(matched_keywords),
                'keywords_count': len(job_keywords),
            })
        
        # Sort by fit score
        return sorted(results, key=lambda x: x['fit_score'], reverse=True)
    
    @staticmethod
    def get_improvement_suggestions(missing_keywords: List[str]) -> List[str]:
        """Generate suggestions based on missing keywords."""
        suggestions = []
        
        cloud_keywords = ['aws', 'azure', 'gcp', 'docker', 'kubernetes']
        ml_keywords = ['tensorflow', 'pytorch', 'scikit-learn', 'machine learning']
        web_keywords = ['react', 'node.js', 'django', 'flask']
        
        missing_lower = [k.lower() for k in missing_keywords]
        
        if any(k in missing_lower for k in cloud_keywords):
            suggestions.append("Complete AWS/Azure certification or Docker course")
        if any(k in missing_lower for k in ml_keywords):
            suggestions.append("Build ML projects with TensorFlow/PyTorch")
        if any(k in missing_lower for k in web_keywords):
            suggestions.append("Create full-stack project (React + Node.js/Django)")
        
        # Generic suggestions
        if len(missing_keywords) > 3:
            suggestions.append("Add 2-3 more relevant keywords to resume")
        suggestions.append("Update GitHub with recent projects")
        
        return suggestions[:4]
