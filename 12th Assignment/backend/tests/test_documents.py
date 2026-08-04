import os
import pytest
from app.rag.extractor import DocumentExtractor

def test_extract_txt_file(tmp_path):
    test_file = tmp_path / "sample.txt"
    test_file.write_text("Company Leave Policy:\nEmployees get 20 days of paid leave per year.")
    
    extracted = DocumentExtractor.extract_txt(str(test_file))
    assert len(extracted) == 1
    assert "20 days of paid leave" in extracted[0]["content"]
    assert extracted[0]["page"] == 1
