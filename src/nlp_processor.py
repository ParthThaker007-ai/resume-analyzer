"""NLP processing for resume analysis"""

import re
import spacy
from typing import List, Dict, Tuple
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

class NLPProcessor:
    """Process resume text with NLP techniques"""
    
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            import os
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
    
    def extract_entities(self, text: str) -> Dict:
        """Extract named entities from text"""
        doc = self.nlp(text[:1000000])
        
        entities = {
            "PERSON": [],
            "ORG": [],
            "GPE": [],
            "DATE": [],
        }
        
        for ent in doc.ents:
            ent_type = ent.label_
            if ent_type in entities:
                if ent.text.lower() not in [e.lower() for e in entities[ent_type]]:
                    entities[ent_type].append(ent.text)
        
        return entities
    
    def extract_contact_info(self, text: str) -> Dict:
        """Extract contact information"""
        contact = {
            "email": None,
            "phone": None,
            "linkedin": None,
            "github": None,
            "website": None
        }
        
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact["email"] = email_match.group()
        
        phone_patterns = [
            r'\+?91?\s?\d{10}',
            r'\(\d{3}\)\s?\d{3}-\d{4}',
            r'\d{10}',
        ]
        for pattern in phone_patterns:
            phone_match = re.search(pattern, text)
            if phone_match:
                contact["phone"] = phone_match.group()
                break
        
        linkedin_pattern = r'linkedin\.com/in/([\w-]+)'
        linkedin_match = re.search(linkedin_pattern, text, re.IGNORECASE)
        if linkedin_match:
            contact["linkedin"] = linkedin_match.group(1)
        
        github_pattern = r'github\.com/([\w-]+)'
        github_match = re.search(github_pattern, text, re.IGNORECASE)
        if github_match:
            contact["github"] = github_match.group(1)
        
        website_pattern = r'(https?://)?([\w.-]+\.[a-zA-Z]{2,})'
        website_match = re.search(website_pattern, text)
        if website_match:
            contact["website"] = website_match.group(2)
        
        return contact
    
    def extract_education(self, text: str) -> List[Dict]:
        """Extract education details"""
        education = []
        
        degree_pattern = r'(B\.(?:Tech|Sc|A|Com)|M\.(?:Tech|Sc|BA|Com|B\.Tech)|PhD|Bachelor|Master|Diploma|Associate)'
        degree_matches = re.finditer(degree_pattern, text, re.IGNORECASE)
        
        for match in degree_matches:
            degree = match.group()
            education.append({
                "degree": degree,
                "context": text[max(0, match.start()-50):min(len(text), match.end()+50)]
            })
        
        return education[:5]
    
    def extract_years_experience(self, text: str) -> Tuple[int, int]:
        """Estimate years of experience"""
        year_pattern = r'\b(19|20)\d{2}\b'
        years = [int(match.group()) for match in re.finditer(year_pattern, text)]
        
        if len(years) >= 2:
            years.sort()
            return (years, years[-1])
        return (None, None)
    def extract_projects(self, text: str):
       
                projects = []

                # Common headings used for project sections
                heading_patterns = [
                    "projects",
                    "project experience",
                    "academic projects",
                    "personal projects",
                    "key projects",
                    "relevant projects",
                ]

                lines = [l.rstrip() for l in text.split("\n")]
                lower_lines = [l.lower() for l in lines]

                # Find where a projects section likely starts
                start_idx = None
                for i, l in enumerate(lower_lines):
                    if any(h in l for h in heading_patterns):
                        start_idx = i + 1
                        break

                if start_idx is None:
                    return []

                # Collect lines after the heading until next major section
                for line in lines[start_idx:]:
                    raw = line.strip()
                    low = raw.lower()
                    if not raw:
                        continue
                    # Stop if we hit another major section heading
                    if any(
                        h in low
                        for h in [
                            "experience",
                            "work history",
                            "professional experience",
                            "education",
                            "skills",
                            "technical skills",
                            "summary",
                            "profile",
                        ]
                    ):
                        break

                    # Treat bullet-like or short title-like lines as project entries
                    if raw.startswith(("-", "•", "*")) or 2 <= len(raw.split()) <= 12:
                        projects.append(raw.lstrip("-•* ").strip())

                # De-duplicate while preserving order
                seen = set()
                unique_projects = []
                for p in projects:
                    if p and p not in seen:
                        seen.add(p)
                        unique_projects.append(p)

                # Limit to at most 10 projects
                return unique_projects[:10]



class SkillExtractor:
    """Extract skills from resume text"""
    
    SKILLS_DB = {
        "Python": ["python", "py"],
        "Java": ["java"],
        "JavaScript": ["javascript", "js"],
        "SQL": ["sql"],
        "Machine Learning": ["machine learning", "ml"],
        "Deep Learning": ["deep learning", "neural network"],
        "TensorFlow": ["tensorflow", "tf"],
        "PyTorch": ["pytorch", "torch"],
        "Docker": ["docker"],
        "Kubernetes": ["kubernetes", "k8s"],
        "AWS": ["aws", "amazon web services"],
        "React": ["react", "reactjs"],
        "Node.js": ["node", "nodejs"],
        "Django": ["django"],
        "Flask": ["flask"],
        "Git": ["git", "github"],
    }
    
    @staticmethod
    def extract_skills(text: str) -> Tuple[Dict[str, List[str]], int]:
        """Extract skills from resume text"""
        text_lower = text.lower()
        found_skills = {}
        
        for skill_name, keywords in SkillExtractor.SKILLS_DB.items():
            found = False
            for keyword in keywords:
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, text_lower):
                    found = True
                    break
            
            if found:
                if skill_name not in found_skills:
                    found_skills[skill_name] = []
                found_skills[skill_name].append(keyword)
        
        return found_skills, len(found_skills)
    