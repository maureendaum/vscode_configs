import requests

response = requests.post(
    "http://localhost:8000/process", json={"text": "Hello, Celery!"}
)
print(response.json())
