from app.rag.extractor import DocumentExtractor
from app.rag.chunker import DocumentChunker
from app.utils.cost_calculator import calculate_llm_cost, calculate_embedding_cost

def test_text_cleaning():
    raw_text = "  Hello   world \n\n\n  This is   a test. \r\n"
    cleaned = DocumentExtractor.clean_text(raw_text)
    assert cleaned == "Hello world\n\nThis is a test."

def test_chunking_logic():
    chunker = DocumentChunker(chunk_size=50, chunk_overlap=10)
    pages = [{"page": 1, "content": "This is a long sentence meant to test the text chunking mechanism in PrivateGPT."}]
    chunks = chunker.create_chunks(pages, document_id="doc1", filename="test.txt", owner_id="user1")
    assert len(chunks) > 0
    assert chunks[0].metadata["document_name"] == "test.txt"
    assert chunks[0].metadata["page"] == 1

def test_cost_calculator():
    emb_cost = calculate_embedding_cost(1000, "text-embedding-3-small")
    assert emb_cost > 0
    
    llm_cost = calculate_llm_cost(500, 200, "gpt-4o-mini")
    assert llm_cost > 0
