import requests

url = "http://127.0.0.1:5000/generate"

data = {
    "text": "I am very happy today!"
}

response = requests.post(url, json=data)

print(response.json())