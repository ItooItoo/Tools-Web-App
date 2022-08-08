import requests

api = '080f0ae474b49f6788a765043df219a2'

weather = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q=Ołpiny&APPID={api}")

print(weather.json()['wind']['speed'])