"""Constants and configuration"""

SKILL_CATEGORIES = {
    "Programming Languages": ["Python", "Java", "JavaScript", "C++", "Go", "Rust", "R", "SQL"],
    "Data Science & AI": ["Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn", "NLP"],
    "Cloud & DevOps": ["AWS", "Google Cloud", "Azure", "Docker", "Kubernetes", "Terraform"],
    "Web Development": ["React", "Vue.js", "Angular", "Node.js", "Django", "Flask"],
    "Databases": ["MySQL", "PostgreSQL", "MongoDB", "Redis", "Elasticsearch"],
}

SAMPLE_JOBS = [
    {
        "title": "Machine Learning Engineer",
        "keywords": [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "TensorFlow",
            "PyTorch",
            "Scikit-learn",
            "Data Preprocessing",
            "Model Deployment",
            "MLOps",
            "Docker",
            "Kubernetes",
            "AWS",
        ],
    },
    {
        "title": "Senior ML Engineer",
        "keywords": ["Python", "TensorFlow", "ML", "Data Analysis", "AWS"],
    },
    {
        "title": "Full Stack Developer",
        "keywords": ["JavaScript", "React", "Node.js", "SQL", "Docker"],
    },
    {
        "title": "Data Scientist",
        "keywords": ["Python", "ML", "SQL", "Statistics", "Tableau"],
    },
    {
        "title": "DevOps Engineer",
        "keywords": ["Docker", "Kubernetes", "AWS", "CI/CD", "Linux"],
    },
    {
        "title": "NLP Engineer",
        "keywords": ["NLP", "Python", "BERT", "Transformers", "Deep Learning"],
    },
    {
        "title": "Cloud Architect",
        "keywords": ["AWS", "Cloud", "Architecture", "Terraform", "DevOps"],
    },
    {
        "title": "Frontend Engineer",
        "keywords": ["React", "JavaScript", "TypeScript", "CSS", "UI/UX"],
    },
    {
        "title": "Backend Engineer",
        "keywords": ["Python", "Java", "SQL", "REST API", "Microservices"],
    },
    {
        "title": "AI Research Scientist",
        "keywords": ["ML", "Research", "TensorFlow", "PyTorch", "Papers"],
    },
    {
        "title": "Product Manager",
        "keywords": ["Product Strategy", "Analytics", "Leadership", "Communication"],
    },
]


COLOR_SCHEME = {
    "excellent": "#10B981",
    "good": "#3B82F6",
    "fair": "#F59E0B",
    "poor": "#EF4444",
}

QUALITY_METRICS = {
    "length": {"min": 150, "max": 1000},
    "keywords_min": 15,
}
