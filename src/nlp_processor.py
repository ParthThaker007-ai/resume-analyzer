import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords', quiet=True)

class NLPProcessor:
    def __init__(self):
        self.nlp = None  # No spaCy

    def extract_contact_info(self, text):
        email = re.findall(r'[\w\.-]+@[\w\.-]+', text)
        phone = re.findall(r'[\+]?[1-9][\d]{0,15}', text)
        return {'email': email[0] if email else None, 'phone': phone[0] if phone else None}

    def extract_education(self, text):
        edu_patterns = ['bachelor', 'master', 'm.tech', 'phd', 'b.tech']
        lines = text.lower().split('\n')
        education = []
        for line in lines:
            if any(p in line for p in edu_patterns):
                education.append({'degree': line.strip()})
        return education[:3]

    def extract_years_experience(self, text):
        years = re.findall(r'(\d{4})\s*[-–to]\s*(\d{4})', text)
        if years:
            return int(years[0][0]), int(years[0][1])
        return None, None

    def extract_projects(self, text):
        projects = []
        lines = text.split('\n')
        for line in lines:
            if any(h in line.lower() for h in ['project', 'projects']) and len(line.strip()) > 10:
                projects.append(line.strip())
        return projects[:5]

    def extract_skills(self, text):
        """Extract skills using regex + NLTK."""
        stop_words = set(stopwords.words('english'))
        skills_patterns = [
            r'(python|java|javascript|react|node\.js|sql|docker|aws|azure|kubernetes)',
            r'(machine learning|deep learning|nlp|computer vision|tensorflow|pytorch)',
            r'(git|github|jenkins|docker|kubernetes|terraform)',
            r'(flask|django|fastapi|express|spring)'
        ]
        skills = []
        text_lower = text.lower()
        for pattern in skills_patterns:
            matches = re.findall(pattern, text_lower)
            skills.extend(matches)
        unique_skills = list(set([s.capitalize() for s in skills]))
        return {'Technical Skills': unique_skills[:20]}, len(unique_skills)
