import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_register_and_login_user():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1. Register user
        register_payload = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "securepassword123"
        }
        res = await ac.post("/api/v1/auth/register", json=register_payload)
        assert res.status_code in [201, 400]  # 201 created or 400 if already exists
        
        # 2. Login user
        login_data = {
            "username": "testuser",
            "password": "securepassword123"
        }
        login_res = await ac.post("/api/v1/auth/login", data=login_data)
        assert login_res.status_code == 200
        token_data = login_res.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"
