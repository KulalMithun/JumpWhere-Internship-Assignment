from app.config import settings

# Pricing dictionary per 1,000 tokens (USD)
PRICING = {
    "text-embedding-3-small": {
        "embedding": 0.00002 / 1000
    },
    "text-embedding-3-large": {
        "embedding": 0.00013 / 1000
    },
    "gpt-4o-mini": {
        "prompt": 0.00015 / 1000,
        "completion": 0.00060 / 1000
    },
    "gpt-4o": {
        "prompt": 0.00250 / 1000,
        "completion": 0.01000 / 1000
    },
    "gpt-4.1": {
        "prompt": 0.00250 / 1000,
        "completion": 0.01000 / 1000
    }
}

def calculate_embedding_cost(token_count: int, model_name: str = None) -> float:
    model = model_name or settings.EMBEDDING_MODEL
    rate = PRICING.get(model, {}).get("embedding", 0.00002 / 1000)
    return round(token_count * rate, 6)

def calculate_llm_cost(prompt_tokens: int, completion_tokens: int, model_name: str = None) -> float:
    model = model_name or settings.LLM_MODEL
    rates = PRICING.get(model, PRICING["gpt-4o-mini"])
    p_cost = prompt_tokens * rates.get("prompt", 0.00015 / 1000)
    c_cost = completion_tokens * rates.get("completion", 0.00060 / 1000)
    return round(p_cost + c_cost, 6)
