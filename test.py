import requests

data = {
    "PULocationID":10,
    "DOLocationID":40,
    "trip_distance":30
}

url = "http://localhost:9696/predict"
response = requests.post(url, json=data)
print (response.json())