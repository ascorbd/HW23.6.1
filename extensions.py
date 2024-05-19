import requests
import json
from config import *


class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}. ')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту, возможно вы сделали ошибку в написании {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту, возможно вы сделали ошибку в написании {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать валюту, возможно вы сделали ошибку в написании {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        print(json.loads(r.content))
        total_base = json.loads(r.content)[keys[base]]

        return total_base * amount
