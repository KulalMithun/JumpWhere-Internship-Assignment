import os
import re
from typing import List, Dict, Any
import pdfplumber
import PyPDF2
import docx

class DocumentExtractor:
    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""
        # Normalize whitespace and clean empty lines
        text = re.sub(r'\r\n|\r', '\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    @classmethod
    def extract_pdf(cls, file_path: str) -> List[Dict[str, Any]]:
        pages_content = []
        try:
            with pdfplumber.open(file_path) as pdf:
                for idx, page in enumerate(pdf.pages):
                    raw_text = page.extract_text() or ""
                    cleaned = cls.clean_text(raw_text)
                    if cleaned:
                        pages_content.append({
                            "page": idx + 1,
                            "content": cleaned
                        })
        except Exception as e:
            # Fallback to PyPDF2 if pdfplumber fails
            pages_content = []
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for idx, page in enumerate(reader.pages):
                    raw_text = page.extract_text() or ""
                    cleaned = cls.clean_text(raw_text)
                    if cleaned:
                        pages_content.append({
                            "page": idx + 1,
                            "content": cleaned
                        })
        return pages_content

    @classmethod
    def extract_docx(cls, file_path: str) -> List[Dict[str, Any]]:
        doc = docx.Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            if para.text.strip():
                full_text.append(para.text.strip())
        cleaned = cls.clean_text("\n".join(full_text))
        if not cleaned:
            return []
        return [{"page": 1, "content": cleaned}]

    @classmethod
    def extract_txt(cls, file_path: str) -> List[Dict[str, Any]]:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        cleaned = cls.clean_text(content)
        if not cleaned:
            return []
        return [{"page": 1, "content": cleaned}]

    @classmethod
    def extract_document(cls, file_path: str, file_type: str) -> List[Dict[str, Any]]:
        ext = file_type.lower()
        if ext == ".pdf" or ext == "pdf":
            return cls.extract_pdf(file_path)
        elif ext in [".docx", "docx", ".doc"]:
            return cls.extract_docx(file_path)
        elif ext in [".txt", "txt"]:
            return cls.extract_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_type}")
