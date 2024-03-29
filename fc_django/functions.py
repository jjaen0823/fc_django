import requests
import datetime


def get_exchange():
    today = datetime.datetime.now()
    today = today.strftime('%Y%m%d')

    auth = 'idZvXEwCUaQ05hv1caDl0ng4wRDKbTIv'
    url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={}&searchdate={}&data=AP01'
    url = url.format(auth, today)
    res = requests.get(url)

    data = res.json()

    for d in data:
        if d['cur_unit'] == 'USD':
            return d['tts']

    return
