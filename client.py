import requests
import time

server_url = "http://127.0.0.1:51072/"

counter = 1

def send_message(message, counter):
    payload = {"message": message, "counter": counter}
    try:
        response = requests.post(f"{server_url}/submit", json=payload)
        if response.status_code == 200:
            print(f"Message sent successfully: {message}")
            return response.json().get("counter", counter)
        else:
            print(f"Message transfer failing: {message}, Status: {response.status_code}")
            return counter
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return counter

def main():
    global counter
    while True:
        message = f"Message number {counter}"
        counter = send_message(message, counter)
        counter += 1
        time.sleep(0.5)

if __name__ == "__main__":
    main()
