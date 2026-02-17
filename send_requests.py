import requests

URL = "http://127.0.0.1:5000/generate"

def send_request(i):
    payload = {"startup": f"Startup_{i}"}
    response = requests.post(URL, json=payload)
    print(f"Request {i}: {response.json()}")

if __name__ == "__main__":
    total_requests = 30

    for i in range(1, total_requests + 1):
        send_request(i)
