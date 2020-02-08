import requests

class Weather:

    def __init__(self):
        self.appid = '11c0d3dc6093f7442898ee49d2430d20'
        self.city_id = 0


    def main(self, s_city):

        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                     params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': self.appid})
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]
        self.city_id = data['list'][0]['id']


        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'id': self.city_id, 'units': 'metric', 'lang': 'ru', 'APPID': self.appid})
        data = res.json()
        conditions = data['weather'][0]['description']
        temp = data['main']['temp']
        temp_min = data['main']['temp_min']
        temp_max = data['main']['temp_max']
        return conditions, temp, temp_min, temp_max

