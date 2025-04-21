from fastapi.testclient import TestClient
from app.newMain import app


client=TestClient(app)

def test_root():
    test_response=client.get("/")
    print(test_response.json().get("message"))
    assert test_response.json().get('message') =="Hello World"