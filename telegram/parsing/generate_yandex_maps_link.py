import requests


class MapsLinkBuilder:
    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'priority': 'u=1, i',
        'referer': 'https://nominatim.openstreetmap.org/ui/search.html?q=%D0%91%D0%B5%D0%BB%D0%B0%D1%80%D1%83%D1%81%D1%8C+%D0%BC%D0%B8%D0%BD%D1%81%D0%BA+%D1%83%D0%BB%D0%B8%D1%86%D0%B0+%D0%B1%D0%B5%D0%BB%D0%B5%D1%86%D0%BA%D0%BE%D0%B3%D0%BE+2',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    generate_coordinate_link = 'https://nominatim.openstreetmap.org/search.php'
    yandex_map_link = 'https://yandex.by/maps/?pt='

    def __init__(self, address: str):
        self.address = address

    def get_json_format(self):
        params = {
            'q': f'{self.address}',
            'polygon_geojson': '1',
            'format': 'jsonv2',
        }

        response = requests.get(
            self.generate_coordinate_link,
            params=params,
            headers=self.headers
        )

        data = response.json()
        return data

    def get_object(self):
        data = self.get_json_format()

        if data:
            result = data[0]

            lat = result['lat']
            lon = result['lon']

            return self.yandex_map_link + f'{lon}%2C{lat}&z=17'

        else:
            return False

    def get_link(self):
        link = self.get_object()

        return link
