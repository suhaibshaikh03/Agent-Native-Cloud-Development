from fastapi.testclient import TestClient
from .main import app

client = TestClient(app=app)

def test_chat_message():
    response = client.post("/chat", json={"message":[{"role":"ghh","content":"kkl"}]})
    assert response.status_code == 200
    assert response.json() == {"message":"Hello World"}