import requests
from modules.configs.config import token_d2r
from datetime import datetime

def terror_zone_def() -> str:

    params = {
        'token': token_d2r
    }

    response = requests.get('https://d2runewizard.com/api/terror-zone', params=params)
    return response.json()['terrorZone']['zone']


if __name__ == '__main__':
    print(terror_zone_def())
