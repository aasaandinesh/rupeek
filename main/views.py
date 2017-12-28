import json

from django.http import HttpResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from django.views import View
import xmltodict
from urllib.request import urlopen


def get_time(current_data, next_data):
    import dateutil.parser
    current_time = dateutil.parser.parse(current_data['time'])
    next_time = dateutil.parser.parse(next_data['time'])
    difference = (next_time - current_time).seconds
    return difference


def get_elevation(data):
    return float(data['ele'])


def get_data():
    file = urlopen(
        'https://dl.dropboxusercontent.com/s/8nvqnasci6l76nz/Problem.gpx?dl=0')
    data = file.read()
    file.close()
    data = xmltodict.parse(data)
    return data


class MapView(View):
    def get(self, request):
        data = get_data()
        simplified_data = []
        for d in data['gpx']['trk']['trkseg']['trkpt']:
            sd = {'lat': d['@lat'], 'lon': d['@lon']}
            simplified_data.append(sd)
        return render_to_response('map.html', {'data': simplified_data})


class MainView(View):
    def get(self, request):
        data = get_data()
        total_distance = 0
        index = 0
        time_elapsed = 0
        length = len(data['gpx']['trk']['trkseg']['trkpt'])
        max_speed = 0
        moving_time = 0
        max_height = 0
        max_depth = 0
        while index < length - 1:
            current_data = data['gpx']['trk']['trkseg']['trkpt'][index]
            next_data = data['gpx']['trk']['trkseg']['trkpt'][index + 1]
            current_elevation = get_elevation(current_data)
            next_elevation = get_elevation(next_data)
            time_difference = get_time(current_data, next_data)
            time_elapsed += time_difference

            distance = get_distance(current_data['@lat'], current_data['@lon'], next_data['@lat'], next_data['@lon'])
            total_distance += distance
            if distance != 0:
                moving_time += time_difference
            if time_difference != 0:
                speed = distance / time_difference
            else:
                speed = 0
            if speed > max_speed:
                max_speed = speed

            max_height = max(current_elevation, next_elevation, max_height)
            max_depth = min(current_elevation, next_elevation, max_depth)
            index += 1

        average_speed = total_distance / time_elapsed
        calculated_data = {"distance": total_distance, "max_speed": max_speed, "average_speed": average_speed,
                           "max_height": max_height, "max_depth": max_depth,
                           "moving_time": moving_time, "total_time": time_elapsed}

        return render_to_response('main.html', {'data': calculated_data})


def get_distance(lat1, lon1, lat2, lon2):
    from math import sin, cos, sqrt, atan2, radians

    # approximate radius of earth in km
    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))
    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))
    R = 6373.0
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance * 1000
