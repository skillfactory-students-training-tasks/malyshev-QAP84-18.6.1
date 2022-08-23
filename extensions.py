import requests
from config import keys

class api:

    def get_price(base,quote,amount):

        r = requests.get(f'https://v6.exchangerate-api.com/v6/826ab1e60c1d5b5ce322f241/pair/{keys[quote]}/{keys[base]}/{amount}')
        r = r.json()
        return r.get('conversion_result')

    def get_values():
        return keys

class ConvertException(Exception):
    pass

