import requests


def city_by_ip() -> str:
    url_1 = 'https://api.ipify.org?format=json'
    try:
        ip_1 = requests.get(url_1)
    except requests.exceptions.Timeout:
        return f'Извините, произошла ошибка, сервер не отвечает. \n Попробуйте ещё раз.'
    url_2 = 'https://ipinfo.io/' + ip_1.json()['ip'] +  '/geo'
    try:
        ip_2 = requests.get(url_2)
    except requests.exceptions.Timeout:
        return f'Извините, произошла ошибка, сервер не отвечает. \n Попробуйте ещё раз.'
    ip_2_json = ip_2.json()
    return ip_2_json['city']
