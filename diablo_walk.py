from urllib import response
import requests
from data.config import token

params = {
    'token': 'E1pjhPc7fX8OZagTPfiJww'
}

url = 'https://d2runewizard.com/api/diablo-clone-progress/planned-walks'

response = requests.get(url=url, params=params)
print(response.json())
print(token)
