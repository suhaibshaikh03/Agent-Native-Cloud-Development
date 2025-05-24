from fastapi.testclient import TestClient
from .main import app
from .hello import addition
client = TestClient(app)

def test_hello_message():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_addition():
    assert 0 == addition(0,0)
    assert -3 == addition(-1,-2)
    assert 3 == addition(1,2)
    assert 5 == addition(3,2)
    assert 7 == addition(1,6)
