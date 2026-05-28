import requests


for _ in range(100):

    response = requests.get(

        "http://localhost:8000/"
    )

    print(response.status_code)