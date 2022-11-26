import requests
from modules.configs.config import token_d2r


def clone():
    params = {
        'token': token_d2r
    }

    url = 'https://d2runewizard.com/api/diablo-clone-progress/all'

    response = requests.get(url=url, params=params)

    return {item['server']: {'server': item['server'],
                             'progres': item['progress'],
                             'ladder': item['ladder'],
                             'hardcore': item['hardcore'],
                             'region': item['region'],
                             'lastUpdate': item['lastUpdate']['seconds']}
            for item in response.json()['servers']}


if __name__ == '__main__':
    print(clone()['ladderSoftcoreAsia']['server'])
