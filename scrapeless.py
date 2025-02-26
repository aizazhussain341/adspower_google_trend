import json
import requests
import sys

class Payload:
    def __init__(self, actor, input_data, proxy):
        self.actor = actor
        self.input = input_data
        self.proxy = proxy


def send_request():
    host = "api.scrapeless.com"
    url = f"https://{host}/api/v1/scraper/request"
    token = "sk_0iSYlGnxgYAhpReJPNQvpJyitHhN47GiJsRg80bwDQ7ZpbMb9Rz0bt59K0889yxk"

    headers = {
        "x-api-token": token
    }

    input_data = {
        "q":         sys.argv[1],
        "date":      "today 1-m",
        "data_type": "interest_over_time",
        "hl":        "en-sg",
        "tz":        "-480",
        "geo":       "",
        "cat":       "",
        "property":  "",
    }

    proxy = {
        "country": "ANY",
    }

    payload = Payload("scraper.google.trends", input_data, proxy)

    json_payload = json.dumps(payload.__dict__)

    response = requests.post(url, headers=headers, data=json_payload)

    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return

    print(response.text)

if __name__ == "__main__":
    send_request()