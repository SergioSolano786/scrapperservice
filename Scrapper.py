from bs4 import BeautifulSoup
import requests
import json
from collections import defaultdict
from flask import Flask, json
from flask import request

api = Flask(__name__)


def scrap(url):
    print('Consulting url...')
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    print('Finding headers...')
    titles = soup.find_all('h5', class_='CertDigTit2')
    info = soup.find_all('h5', class_='CertDigVal2')
    name = soup.find_all('h5', class_='CertDigVal1')

    print('Normalizing data...')

    print('Parsing data...')
    parsedInfo = []

    for j in titles:
        try:
            parsedInfo.append(j.text)
        except IndexError:
            pass
        continue


    for i in info:
        try:
            parsedInfo.append(i.text)
        except IndexError:
            pass
        continue


    for k in name:
        try:
            parsedInfo.append(k.text)
        except IndexError:
            pass
        continue

    print(parsedInfo)
    print('Writing outputs...')

    jsondataMono = {
        "id": parsedInfo[9],
        "name": parsedInfo[15],
        "viccines_info": [
            {
                "health_entity_frist_dose": parsedInfo[12],
                "vaccine_first_dose_country": parsedInfo[14],
                "vaccine_first_dose": parsedInfo[11],
                "vaccine_first_dose_batch": parsedInfo[10],
                "vaccine_first_dose_date": parsedInfo[13],
            },
        ],
    }

    if parsedInfo[11] != 'JANSSEN PHARMACEUTICA':
        try:
            jsondata = {
                "id": parsedInfo[15],
                "name": parsedInfo[26],
                "viccines_info": [
                    {
                        "health_entity_frist_dose": parsedInfo[18],
                        "vaccine_first_dose_country": parsedInfo[20],
                        "vaccine_first_dose": parsedInfo[17],
                        "vaccine_first_dose_batch": parsedInfo[16],
                        "vaccine_first_dose_date": parsedInfo[19],
                    },
                    {
                        "health_entity_second_dose": parsedInfo[23],
                        "vaccine_second_dose_country": parsedInfo[25],
                        "vaccine_second_dose": parsedInfo[22],
                        "vaccine_second_dose_batch": parsedInfo[21],
                        "vaccine_first_dose_date": parsedInfo[24],
                    }
                ],
            }
        except IndexError:
            jsondata = {
            "id": parsedInfo[9],
            "name": parsedInfo[15],
            "viccines_info": [
                {
                "health_entity_frist_dose": parsedInfo[12],
                "vaccine_first_dose_country": parsedInfo[14],
                "vaccine_first_dose": parsedInfo[11],
                "vaccine_first_dose_batch": parsedInfo[10],
                "vaccine_first_dose_date": parsedInfo[13],
            },
        ],
    }
    if parsedInfo[11] == 'JANSSEN PHARMACEUTICA':
        return json.dumps(jsondataMono)
    else:
        return json.dumps(jsondata)



@api.route('/vaccines/', methods=['GET'])
def get_info():
  return scrap(request.args.get('url'))

if __name__ == '__main__':
    api.run()


