import json
import requests

def main():

    url = "http://127.0.0.1:5000/api/v1/drink/"

    payload = {'api_key': 'LAGJZGOFMQPEMHA'}
    response = requests.get(url, params=payload)
    print(response.text)




if __name__ == "__main__":
    main()