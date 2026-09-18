import requests


def dollar_exchange_rate() -> float:
    """
    Эта функция обращается к API Центрального банка Российской Федерации,
    для получения актуального курса доллара в рублях.
    :return: Курс доллара (сколько стоит 1 доллар в рублях)
    """
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    try:
        central_bank_information = requests.get(url)
    except requests.exceptions.Timeout:
        return 0
    data = central_bank_information.json()
    dollar_exchange_rate = data['Valute']['USD']['Value']
    return dollar_exchange_rate

