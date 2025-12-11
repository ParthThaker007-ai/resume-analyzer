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
    """Extract skills using case-insensitive regex + normalization."""
    import re
    from nltk.corpus import stopwords
    nltk.download('stopwords', quiet=True)
    stop_words = set(stopwords.words('english'))
    
    # Expanded skills patterns (case-insensitive)
    skills_patterns = [
        r'(python|java|javascript|js|react|node\.js|nodejs|sql|docker|aws|amazon web services|azure|kubernetes|k8s)',
        r'(machine learning|deep learning|nlp|natural language|computer vision|tensorflow|tf|pytorch|scikit-learn|sklearn)',
        r'(git|github|gitlab|jenkins|docker|kubernetes|k8s|terraform|ansible)',
        r'(flask|django|fastapi|express|spring boot|springboot|laravel|rails)',
        r'(pandas|numpy|matplotlib|seaborn|plotly|jupyter)'
    ]
    
    skills = []
    text_lower = text.lower()
    
    for pattern in skills_patterns:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        skills.extend(matches)
    
    # Normalize and deduplicate (preserve casing from original text)
    normalized_skills = []
    for skill in skills:
        # Capitalize properly
        if skill.lower() == 'aws':
            normalized_skills.append('AWS')
        elif skill.lower() == 'k8s':
            normalized_skills.append('Kubernetes')
        elif skill.lower() == 'js':
            normalized_skills.append('JavaScript')
        elif skill.lower() == 'nodejs':
            normalized_skills.append('Node.js')
        elif skill.lower() == 'tf':
            normalized_skills.append('TensorFlow')
        elif skill.lower() == 'sklearn':
            normalized_skills.append('Scikit-learn')
        else:
            normalized_skills.append(skill.capitalize())
    
    unique_skills = list(dict.fromkeys(normalized_skills))  # Preserve order
    
    return {'Technical Skills': unique_skills[:25]}, len(unique_skills)

