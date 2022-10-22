import requests
from data.config import token_d2r
from datetime import datetime

def terror_zone_def():

    params = {
        'token': token_d2r
    }

    response = requests.get('https://d2runewizard.com/api/terror-zone', params=params)
    return response.json()

if __name__ == '__main__':
    print(terror_zone_def())
    print()
    print(list(sorted(terror_zone_def()['terrorZone']['reportedZones'].items(), key=lambda x: x[1], reverse=True)))
    #print(terror_zone_def()['terrorZone']['highestProbabilityZone']['zone'])
