"""Resume quality scoring"""

import re
import numpy as np
from typing import Dict, List, Tuple

class ResumeScorer:
    """Assess resume quality"""
    
    @staticmethod
    def calculate_quality_score(resume_text: str) -> Tuple[float, Dict[str, float]]:
        """Calculate overall resume quality score"""
        scores = {}
        
        word_count = len(resume_text.split())
        if 150 <= word_count <= 1000:
            scores["length"] = 100
        elif word_count < 150:
            scores["length"] = max(0, (word_count / 150) * 100)
        else:
            scores["length"] = max(0, 100 - ((word_count - 1000) / 500) * 20)
        
        scores["structure"] = ResumeScorer._assess_structure(resume_text)
        scores["grammar"] = ResumeScorer._assess_grammar(resume_text)
        scores["keywords"] = ResumeScorer._assess_keywords(resume_text)
        scores["formatting"] = ResumeScorer._assess_formatting(resume_text)
        
        overall = (
            scores["length"] * 0.2 +
            scores["structure"] * 0.2 +
            scores["grammar"] * 0.2 +
            scores["keywords"] * 0.2 +
            scores["formatting"] * 0.2
        )
        
        return round(overall, 1), scores
    
    @staticmethod
    def _assess_structure(text: str) -> float:
        """Assess resume structure"""
        sections = ["contact", "summary", "experience", "education", "skills"]
        found_sections = sum(1 for section in sections if section in text.lower())
        
        if found_sections >= 3:
            return 100
        elif found_sections == 2:
            return 70
        elif found_sections == 1:
            return 40
        else:
            return 20
    
    @staticmethod
    def _assess_grammar(text: str) -> float:
        """Assess grammar and writing quality"""
        lines = text.split('\n')
        issues = 0
        total_checks = 0
        
        for line in lines:
            if len(line.strip()) > 10:
                total_checks += 1
                if not any(line.strip().endswith(p) for p in ['.', '!', '?', ',']):
                    if len(line.split()) > 5:
                        issues += 1
        
        if total_checks == 0:
            return 50
        
        error_rate = issues / total_checks
        grammar_score = max(0, (1 - error_rate) * 100)
        return min(100, grammar_score)
    
    @staticmethod
    def _assess_keywords(text: str) -> float:
        """Assess keyword diversity"""
        tech_keywords = [
            "python", "java", "sql", "machine learning", "api",
            "docker", "git", "aws", "react", "node"
        ]
        
        text_lower = text.lower()
        found_keywords = sum(1 for keyword in tech_keywords if keyword in text_lower)
        keyword_score = (found_keywords / len(tech_keywords)) * 100
        
        return min(100, keyword_score)
    
    @staticmethod
    def _assess_formatting(text: str) -> float:
        """Assess formatting consistency"""
        lines = text.split('\n')
        non_empty_lines = [l for l in lines if l.strip()]
        
        if not non_empty_lines:
            return 20
        
        avg_line_length = np.mean([len(line) for line in non_empty_lines])
        
        if 40 <= avg_line_length <= 100:
            formatting_score = 100
        else:
            formatting_score = max(20, 100 - abs(avg_line_length - 70) / 70 * 80)
        
        return formatting_score
    
    @staticmethod
    def get_quality_feedback(scores: Dict[str, float]) -> List[str]:
        """Get improvement suggestions"""
        feedback = []
        
        if scores["length"] < 70:
            feedback.append("Resume is too short. Aim for 150-1000 words.")
        if scores["structure"] < 70:
            feedback.append("Missing key sections. Include: Contact, Summary, Experience, Education, Skills.")
        if scores["grammar"] < 80:
            feedback.append("Review grammar and writing clarity.")
        if scores["keywords"] < 60:
            feedback.append("Add more technical keywords relevant to your field.")
        if scores["formatting"] < 70:
            feedback.append("Improve formatting consistency and readability.")
        
        if not feedback:
            feedback.append("Resume looks great! Keep it updated.")
        
        return feedback
