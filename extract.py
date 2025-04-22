import requests, json

def get_api():
    url = 'https://fakestoreapi.com/products'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            raw_json = response.json()
            return raw_json
        else:
            print('Error loading API')
    except Exception as a:
        print('Failed to load API')

def saving_api_json(raw_json):
    with open('new_raw.json', 'w', encoding='utf-8') as json_raw:
        json.dump(raw_json, json_raw, indent=4)
#print(response.json())
