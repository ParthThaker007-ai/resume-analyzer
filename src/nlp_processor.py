import re
import nltk
from nltk.corpus import stopwords

# Download NLTK data on first run
nltk.download('stopwords', quiet=True)

class NLPProcessor:
    """NLP Processor using regex + NLTK (no spaCy - cloud deploy ready)."""
    
    def __init__(self):
        """Initialize without spaCy."""
        self.nlp = None  # No spaCy for cloud deployment

    def extract_contact_info(self, text):
        """Extract email and phone using regex."""
        emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        phones = re.findall(r'[\+]?[1-9][\d]{7,15}', text)
        return {
            'email': emails[0] if emails else None,
            'phone': phones[0] if phones else None,
            'linkedin': None
        }

    def extract_education(self, text):
        """Extract education using keyword matching."""
        edu_keywords = ['bachelor', 'master', 'm.tech', 'phd', 'b.tech', 'b.e.', 'm.s.', 'm.e.']
        lines = [line.strip() for line in text.lower().split('\n')]
        education = []
        
        for line in lines:
            if any(keyword in line for keyword in edu_keywords):
                education.append({'degree': line.title()})
                if len(education) >= 3:
                    break
        
        return education

    def extract_years_experience(self, text):
        """Extract experience years using date ranges."""
        # Match 2018-2023, 2018 - 2023, 2018 to 2023
        year_patterns = [
            r'(\d{4})\s*[-–—]\s*(\d{4})',
            r'(\d{4})\s+to\s+(\d{4})',
            r'from\s+(\d{4})\s+to\s+(\d{4})'
        ]
        
        for pattern in year_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                start_year = int(matches[0][0])
                end_year = int(matches[0][1])
                if end_year > start_year and end_year - start_year <= 20:
                    return start_year, end_year
        
        return None, None

    def extract_projects(self, text):
        """Extract projects section."""
        project_keywords = ['project', 'projects', 'academic project', 'personal project']
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
        """Extract skills using case-insensitive regex + normalization."""
        stop_words = set(stopwords.words('english'))
        
        # Comprehensive skills patterns (case-insensitive)
        skills_patterns = [
            r'(python|java|javascript|js?|typescript|react|vue|angular|node\.?(js)?|nodejs|sql|mysql|postgresql|mongodb)',
            r'(machine learning|deep learning|nlp|ai|computer vision|tensorflow|tf?|pytorch|scikit[-_]?learn|sklearn|keras|huggingface)',
            r'(git|github|gitlab|docker|aws|amazon web services|azure|gcp|google cloud|kubernetes|k8s?|terraform|ansible|jenkins|ci/?cd)',
            r'(flask|django|fastapi|express|spring boot|springboot|laravel|ruby on rails?|next\.?js?|nuxt\.?js?)',
            r'(pandas|numpy|matplotlib|seaborn|plotly|jupyter|colab|linux|windows|macos)'
        ]
        
        all_skills = []
        text_lower = text.lower()
        
        for pattern in skills_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            all_skills.extend(matches)
        
        # Normalize skill names (preserve proper casing)
        normalized_skills = []
        skill_mapping = {
            'js': 'JavaScript',
            'nodejs': 'Node.js',
            'tf': 'TensorFlow',
            'sklearn': 'Scikit-learn',
            'k8s': 'Kubernetes',
            'aws': 'AWS'
        }
        
        for skill in all_skills:
            clean_skill = skill_mapping.get(skill.lower(), skill.capitalize())
            if clean_skill not in normalized_skills:
                normalized_skills.append(clean_skill)
        
        return {
            'Technical Skills': normalized_skills[:25]
        }, len(normalized_skills)
