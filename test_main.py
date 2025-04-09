from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app
from tasks import process_data_task

# Create a test client
client = TestClient(app)


# Mock for Celery AsyncResult
class MockAsyncResult:
    def __init__(self, task_id, status, result=None):
        self.id = task_id
        self.status = status
        self._result = result

    def get(self):
        return self._result


# Test the root endpoint
def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "FastAPI with Celery Integration"}


# Test the process endpoint with mocked Celery task
@patch("main.process_data_task")
def test_process_data(mock_process_task):
    # Setup mock
    mock_task = MagicMock()
    mock_task.id = "test-task-id-123"
    mock_process_task.delay.return_value = mock_task

    # Make request
    test_data = {"text": "Hello, Test!"}
    response = client.post("/process", json=test_data)

    # Assert response
    assert response.status_code == 200
    result = response.json()
    assert "task_id" in result
    assert result["task_id"] == "test-task-id-123"
    assert result["message"] == "Task submitted successfully"

    # Assert Celery task was called with correct args
    mock_process_task.delay.assert_called_once_with("Hello, Test!")


# Test get task status - PENDING case
@patch("main.AsyncResult")
def test_get_task_status_pending(mock_async_result):
    # Setup mock
    task_id = "pending-task-id"
    mock_async_result.return_value = MockAsyncResult(task_id, "PENDING")

    # Make request
    response = client.get(f"/tasks/{task_id}")

    # Assert response
    assert response.status_code == 200
    result = response.json()
    assert result["task_id"] == task_id
    assert result["status"] == "PENDING"
    assert "result" not in result


# Test get task status - SUCCESS case
@patch("main.AsyncResult")
def test_get_task_status_success(mock_async_result):
    # Setup mock
    task_id = "success-task-id"
    task_result = {
        "processed_data": "!TSET ,OLLEH",
        "original_data": "Hello, TEST!",
        "processing_time": 5,
    }
    mock_async_result.return_value = MockAsyncResult(task_id, "SUCCESS", task_result)

    # Make request
    response = client.get(f"/tasks/{task_id}")

    # Assert response
    assert response.status_code == 200
    result = response.json()
    assert result["task_id"] == task_id
    assert result["status"] == "SUCCESS"
    assert "result" in result
    assert result["result"] == task_result


# Test actual task function directly
def test_process_data_task():
    # Test the actual task function
    input_text = "Test Task"
    result = process_data_task(input_text)

    assert result["original_data"] == input_text
    assert result["processed_data"] == "KSAT TSET"  # Reversed and uppercase
    assert result["processing_time"] == 5


# Test input validation
def test_process_data_invalid_input():
    # Missing required field
    response = client.post("/process", json={})
    assert response.status_code == 422  # Unprocessable Entity

    # Wrong data type
    response = client.post("/process", json={"text": 123})
    assert response.status_code == 422
