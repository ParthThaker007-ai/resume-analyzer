
"""Extract resume text from various file formats"""

import pdfplumber
import pytesseract
from PIL import Image
import io
import re
from pathlib import Path

class ResumeExtractor:
    """Extract text from resume files"""
    
    @staticmethod
    def extract_from_pdf(pdf_file) -> str:
        """Extract text from PDF file"""
        try:
            text = ""
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text.strip()
        except Exception as e:
            raise ValueError(f"Error extracting PDF: {str(e)}")
    
    @staticmethod
    def extract_from_image(image_file) -> str:
        """Extract text from image using OCR"""
        try:
            image = Image.open(image_file)
            image = image.resize((image.width * 2, image.height * 2))
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            raise ValueError(f"Error extracting image: {str(e)}")
    
    @staticmethod
    def extract_from_docx(docx_file) -> str:
        """Extract text from DOCX file"""
        try:
            from docx import Document
            doc = Document(docx_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            raise ValueError(f"Error extracting DOCX: {str(e)}")
    
    @staticmethod
    def extract_from_txt(txt_file) -> str:
        """Extract text from TXT file"""
        try:
            content = txt_file.read().decode('utf-8', errors='ignore')
            return content.strip()
        except Exception as e:
            raise ValueError(f"Error extracting TXT: {str(e)}")
    
    @staticmethod
    def extract(file_obj, file_type: str) -> str:
        """Main extraction method"""
        file_type = file_type.lower()
        
        if file_type == "pdf":
            return ResumeExtractor.extract_from_pdf(file_obj)
        elif file_type in ["jpg", "jpeg", "png", "bmp", "gif"]:
            return ResumeExtractor.extract_from_image(file_obj)
        elif file_type == "docx":
            return ResumeExtractor.extract_from_docx(file_obj)
        elif file_type == "txt":
            return ResumeExtractor.extract_from_txt(file_obj)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

class TextCleaner:
    """Clean and normalize extracted text"""
    
    @staticmethod
    def clean(text: str) -> str:
        """Clean extracted text"""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^a-zA-Z0-9\s\.\-+()@]', ' ', text)
        text = re.sub(r' +', ' ', text)
        return text.strip()
    
    @staticmethod
    def normalize_sections(text: str) -> dict:
        """Split text into sections"""
        sections = {
            "raw": text,
            "lines": [line.strip() for line in text.split('\n') if line.strip()],
            "paragraphs": text.split('\n\n')
        }
        return sections
