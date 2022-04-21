import json
import requests

def main():

    url = "http://127.0.0.1:5000/api/v1/drink/modify"

    payload = {'api_key': '1E9RNF0TIOW2Z3L', 'drink': 'Vodka Redbull', }
    response = requests.post(url, params=payload)
    print(response.text)




if __name__ == "__main__":
    main()