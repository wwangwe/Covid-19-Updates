from django.shortcuts import render

import urllib.request
import pandas as pd
import json

def summary(request):
    url = 'https://api.covid19api.com/summary'
    json_data = urllib.request.urlopen(url)
    data = json.load(json_data)

    world = data['Global']
    date = data['Date']

    total_confirmed = world['TotalConfirmed']
    total_recovered = world['TotalRecovered']
    total_deaths = world['TotalDeaths']
    new_confirmed = world['NewConfirmed']
    new_recovered = world['NewRecovered']
    new_deaths = world['NewDeaths']

    dictionary = {
        'date':date,
        'total_confirmed':total_confirmed, 
        'total_recovered':total_recovered, 
        'total_deaths':total_deaths,
        'new_confirmed':new_confirmed, 
        'new_recovered':new_recovered, 
        'new_deaths':new_deaths
    }
    return dictionary

def index(request):
    context = {
        'dict':summary(request)
    }
    return render(request, 'analysis/index.html', context)
