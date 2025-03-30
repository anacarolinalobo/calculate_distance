import requests

def get_coordinates(endereco):
    url = 'http://nominatim.openstreetmap.org/search'
    params = {
        'q': endereco,
        'format': 'json',
        'limit': 1
    }
    headers = {
        'User-Agent': 'distancia-app-teste (analobo21ime@gmail.com)'  # O Nominatim exige isso
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    if data:
        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])
        return lat, lon
    return None, None


from math import radians, cos, sin, asin, sqrt

def calcular_distancia_km(lat1, lon1, lat2, lon2):
    R = 6371  # raio da Terra em km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    return R * c
