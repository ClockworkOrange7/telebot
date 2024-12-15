
import json
import requests
from config import available_currency


class APIException(Exception):
    '''Класс для вызова исключений'''
    pass

class CryptoConverter:
    '''Класс для создания проверок на правильность ввода'''
    @staticmethod
    def get_price(qoute:str, base:str, amount:str):


        if qoute == base:
            raise APIException(f'Нельзя перевести одинаковые валюты')

        try:
            qoute_ticker = available_currency[qoute]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {qoute}')

        try:
            base_ticker = available_currency[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        if not amount.isfloat():
            raise APIException(f'{amount} - не является числом')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/cf1e072363249a1732969cbb/pair/{qoute_ticker}/{base_ticker}')

        text = json.loads(r.content)
        return text