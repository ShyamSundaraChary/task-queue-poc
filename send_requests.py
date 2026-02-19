import requests
from concurrent.futures import ThreadPoolExecutor

URL = "http://127.0.0.1:8000/generate"

def send_request(i):
    payload = {"startup": f"Startup_{i}"}
    response = requests.post(URL, json=payload)
    print(f"Request {i}: {response.json()}")

if __name__ == "__main__":
    total_requests = 30

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(send_request, range(1, total_requests + 1))
