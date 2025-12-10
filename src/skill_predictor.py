"""ML model to predict hidden skills"""

from typing import List, Dict, Tuple

class SkillPredictor:
    """Predict likely skills based on existing skills"""
    
    SKILL_CORRELATIONS = {
        "Python": ["Machine Learning", "Django", "Flask"],
        "Machine Learning": ["Python", "TensorFlow", "PyTorch"],
        "TensorFlow": ["Machine Learning", "Deep Learning", "Python"],
        "PyTorch": ["Machine Learning", "Deep Learning", "Python"],
        "React": ["JavaScript", "Node.js", "Docker"],
        "Docker": ["Kubernetes", "CI/CD", "Linux"],
        "Kubernetes": ["Docker", "Cloud", "DevOps"],
        "AWS": ["Cloud", "Docker", "Linux"],
        "Git": ["GitHub", "CI/CD"],
    }
    
    @staticmethod
    def predict_skills(extracted_skills: Dict[str, List[str]], 
                      experience_years: int = 0) -> List[Tuple[str, float]]:
        """Predict likely skills based on extracted skills"""
        predicted = []
        
        confidence_boosts = {
            0: 0.6, 1: 0.65, 2: 0.70, 3: 0.75, 5: 0.80, 10: 0.85,
        }
        
        exp_multiplier = confidence_boosts.get(
            experience_years, 
            min(0.90, 0.5 + experience_years * 0.02)
        )
        
        found_skill_names = list(extracted_skills.keys())
        predicted_skills = set()
        
        for skill in found_skill_names:
            if skill in SkillPredictor.SKILL_CORRELATIONS:
                for correlated in SkillPredictor.SKILL_CORRELATIONS[skill]:
                    if correlated not in found_skill_names:
                        predicted_skills.add(correlated)
        
        for skill in predicted_skills:
            base_confidence = 0.70
            
            boost = sum(
                0.05 for found_skill in found_skill_names 
                if skill in SkillPredictor.SKILL_CORRELATIONS.get(found_skill, [])
            )
            
            final_confidence = min(0.95, (base_confidence + boost) * exp_multiplier)
            predicted.append((skill, round(final_confidence, 2)))
        
        predicted.sort(key=lambda x: x, reverse=True)
        return predicted[:5]
    
    @staticmethod
    def predict_next_role(job_title: str, experience_years: int) -> Tuple[str, float]:
        """Predict next likely job role"""
        if experience_years < 2:
            return ("Senior Developer", 0.70)
        elif experience_years < 5:
            return ("Tech Lead", 0.75)
        elif experience_years < 8:
            return ("Engineering Manager", 0.75)
        else:
            return ("Director/Architect", 0.80)
