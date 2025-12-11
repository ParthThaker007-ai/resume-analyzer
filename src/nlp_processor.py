import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)

class NLPProcessor:
    """NLP Processor - regex + NLTK (cloud deploy ready)."""
    
    def __init__(self):
        self.nlp = None

    def extract_contact_info(self, text):
        emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        phones = re.findall(r'[\+]?[1-9][\d]{7,15}', text)
        return {
            'email': emails[0] if emails else None,
            'phone': phones[0] if phones else None
        }

    def extract_education(self, text):
        edu_keywords = ['bachelor', 'master', 'm.tech', 'phd', 'b.tech']
        lines = [line.strip() for line in text.lower().split('\n')]
        education = []
        for line in lines:
            if any(keyword in line for keyword in edu_keywords):
                education.append({'degree': line.title()})
                if len(education) >= 3:
                    break
        return education

    def extract_years_experience(self, text):
        year_patterns = [
            r'(\d{4})\s*[-–—]\s*(\d{4})',
            r'(\d{4})\s+to\s+(\d{4})'
        ]
        for pattern in year_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                start_year = int(matches[0][0])
                end_year = int(matches[0][1])
                if end_year > start_year:
                    return start_year, end_year
        return None, None

    def extract_projects(self, text):
        project_keywords = ['project', 'projects']
        lines = text.split('\n')
        projects = []
        for line in lines:
            line_lower = line.lower().strip()
            if any(keyword in line_lower for keyword in project_keywords) and len(line.strip()) > 10:
                projects.append(line.strip())
            if len(projects) >= 5:
                break
        return projects

    def extract_skills(self, text):
        stop_words = set(stopwords.words('english'))
        skills_patterns = [
            r'(python|java|javascript|react|nodejs?|sql|docker|aws|azure|kubernetes?|k8s?)',
            r'(machine learning|deep learning|nlp|tensorflow|pytorch|scikit[-_]?learn)',
            r'(git|github|jenkins|flask|django|fastapi)'
        ]
        
        all_skills = []
        text_lower = text.lower()
        
        for pattern in skills_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    skill_str = '.'.join(str(x) for x in match if x)
                else:
                    skill_str = str(match)
                all_skills.append(skill_str)
        
        skill_mapping = {
            'js': 'JavaScript',
            'node js': 'Node.js',
            'tf': 'TensorFlow',
            'k8s': 'Kubernetes',
            'aws': 'AWS'
        }
        
        normalized_skills = []
        seen = set()
        for skill in all_skills:
            skill_lower = skill.lower().strip()
            if skill_lower in skill_mapping:
                mapped_skill = skill_mapping[skill_lower]
                if mapped_skill not in seen:
                    normalized_skills.append(mapped_skill)
                    seen.add(mapped_skill)
            elif skill_lower not in seen and len(skill_lower) > 1:
                normalized_skills.append(skill.title())
                seen.add(skill_lower)
        
        return {'Technical Skills': normalized_skills[:20]}, len(normalized_skills)
