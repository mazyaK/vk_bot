import requests

api_url = "https://samples.openweathermap.org/data/2.5/weather"

class Weather:

    def main(self, city):

        params = {
            'q': city,
            'appid': '11c0d3dc6093f7442898ee49d2430d20',
        }

        res = requests.get(api_url, params=params)
        data = res.json()

        return data["main"]["temp"]
