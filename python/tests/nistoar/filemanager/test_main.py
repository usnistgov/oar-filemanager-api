from http import client
from fastapi.testclient import TestClient


from nistoar.filemanager.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Service": "NextCloud File Manager API", "Status": "Running"}