from django.shortcuts import render

import urllib.request
import json
import datetime

def summary(request):
    url = 'https://api.covid19api.com/summary'
    try:
        json_data = urllib.request.urlopen(url)
        data = json.load(json_data)

        string = data['Date']
        date_obj = datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%SZ')
        date = date_obj.strftime('%d-%B-%Y')
        time = date_obj.strftime('%H:%M:%S %p')

        world = data['Global']
        countries = data['Countries']
        columns = [
            'Countries', 'Total Cases', 'New Cases', 'Total Deaths', 
            'New Deaths', 'Total Recoveries', 'New Recoveries'
        ]

        dictionary = {
            'date':date,
            'time':time,
            'world':world,
            'countries':countries,
            'columns':columns
            }

        return dictionary

    except Exception as e:
        error = True
        msg = f'{e}\n No Internert Connection'
        return error, msg
    
def index(request):
    context = summary(request)
    return render(request, 'analysis/index.html', context)
