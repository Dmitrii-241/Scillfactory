import requests
import json


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str) -> float:
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Неверное количество: {amount}")

        currencies = ['евро', 'доллар', 'рубль']
        if base not in currencies:
            raise APIException(f"Неподдерживаемая валюта: {base}")
        if quote not in currencies:
            raise APIException(f"Неподдерживаемая валюта: {quote}")

        symbols = {'евро': 'EUR', 'доллар': 'USD', 'рубль': 'RUB'}
        url = f"https://api.exchangerate-api.com/v4/latest/{symbols[base]}"

        response = requests.get(url)
        if response.status_code != 200:
            raise APIException("Ошибка подключения к API")

        data = response.json()
        rate = data['rates'][symbols[quote]]
        return round(rate * amount, 2)
