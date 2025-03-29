import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_list_functions():
    """Test listing all available functions"""
    response = client.get("/functions")
    assert response.status_code == 200
    assert "functions" in response.json()
    assert len(response.json()["functions"]) > 0

def test_execute_calculator():
    """Test executing the calculator function"""
    response = client.post(
        "/execute",
        json={"prompt": "open calculator for me"}
    )
    assert response.status_code == 200
    assert "function" in response.json()
    assert "application.open_calculator" in response.json()["function"]
    assert "code" in response.json()

def test_execute_system_info():
    """Test executing the system info function"""
    response = client.post(
        "/execute",
        json={"prompt": "show me system information"}
    )
    assert response.status_code == 200
    assert "function" in response.json()
    assert "system.get_system_info" in response.json()["function"]
    assert "code" in response.json()

def test_execute_with_parameters():
    """Test executing function with explicit parameters"""
    response = client.post(
        "/execute",
        json={
            "prompt": "open notepad with a filename",
            "parameters": {"filename": "test.txt"}
        }
    )
    assert response.status_code == 200
    assert "function" in response.json()
    assert "application.open_notepad" in response.json()["function"]
    assert "execution_result" in response.json()

def test_session_context():
    """Test session context is maintained"""
    # First request
    response1 = client.post(
        "/execute?session_id=test_session",
        json={"prompt": "open calculator"}
    )
    assert response1.status_code == 200
    
    # Second request with same session
    response2 = client.post(
        "/execute?session_id=test_session",
        json={"prompt": "get cpu usage"}
    )
    assert response2.status_code == 200
    assert "context" in response2.json()
    assert "calculator" in response2.json()["context"].lower()
