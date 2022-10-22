from urllib import response
import requests
from data.config import token_d2r

params = {
    'token': token_d2r
}

url = 'https://d2runewizard.com/api/diablo-clone-progress/planned-walks'

response = requests.get(url=url, params=params)
print(response.json())
