import requests
import json
from config import keys

class APIException(Exception):
    pass

class СurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount:str):

        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {quote}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')


        url_base = f'https://v6.exchangerate-api.com/v6/67d094efdcdfdb4da2c0e001/latest/{keys[quote]}'
        response = requests.get(url_base).json()
        # получаем значение курса, умножаем на количество, округляем до двух знаков
        total_base = round(response['conversion_rates'][keys[base]] * int(amount), 2)

        return total_base
