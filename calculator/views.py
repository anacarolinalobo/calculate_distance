import requests
import json
from django.shortcuts import render
from .forms import DistanceForm
from geopy.distance import geodesic
from django.contrib import messages
import os

import os
import json
import requests
from django.shortcuts import render
from geopy.distance import geodesic
from django.conf import settings

HISTORY_FILE = os.path.join(settings.BASE_DIR, 'history.json')

from geopy.distance import geodesic
import requests
from django.shortcuts import render
from django.conf import settings

def calculate_distance(request):
    distance = None
    error = None
    source_lat = None
    source_lon = None
    dest_lat = None
    dest_lon = None

    if request.method == 'POST':
        source_address = request.POST.get('source_address')
        destination_address = request.POST.get('destination_address')

        try:
            def get_coords(address):
                url = "https://nominatim.openstreetmap.org/search"
                params = {
                    'q': address,
                    'format': 'json',
                    'limit': 1
                }
                headers = {'User-Agent': 'DjangoApp (analobo21ime@gmail.com)'}
                response = requests.get(url, params=params, headers=headers)
                data = response.json()
                if not data:
                    raise ValueError(f"Address not found: {address}")
                return float(data[0]['lat']), float(data[0]['lon'])

            source_coords = get_coords(source_address)
            dest_coords = get_coords(destination_address)

            source_lat, source_lon = source_coords
            dest_lat, dest_lon = dest_coords

            distance = round(geodesic(source_coords, dest_coords).km, 2)

            new_entry = {
                'source': source_address,
                'destination': destination_address,
                'distance_km': distance,
                'created_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            if os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            else:
                history = []

            history.append(new_entry)

            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=4, default=str)

        except Exception as e:
            error = str(e)

    return render(request, 'calculator.html', {
        'distance': distance, 
        'error': error,
        'source_lat': source_lat,
        'source_lon': source_lon,
        'dest_lat': dest_lat,
        'dest_lon': dest_lon
    })


def get_coordinates(address):
    url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': address,
        'format': 'json'
    }
    response = requests.get(url, params=params, headers={'User-Agent': 'distance-app (analobo21ime@gmail.com)'})
    data = response.json()
    if data:
        return float(data[0]['lat']), float(data[0]['lon'])
    return None

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_to_history(entry):
    history = load_history()
    history.append(entry)
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

from django.shortcuts import render
import requests
from .models import DistanceQuery
from geopy.distance import geodesic
import datetime


def history(request):
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            queries = json.load(f)
    else:
        queries = []

    return render(request, 'history.html', {'queries': queries})

from django.http import JsonResponse

from django.http import JsonResponse

def autocomplete_api(request):
    query = request.GET.get('q')
    if not query:
        return JsonResponse({'suggestions': []})
    
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': query,
        'format': 'json',
        'addressdetails': 1,
        'limit': 5
    }
    headers = {'User-Agent': 'DjangoApp (analobo21ime@gmail.com)'}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    
    suggestions = []
    for place in data:
        suggestions.append(place['display_name'])

    return JsonResponse({'suggestions': suggestions})

