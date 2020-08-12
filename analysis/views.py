from django.shortcuts import render, redirect
from datetime import datetime

import urllib.request
import json

from bs4 import BeautifulSoup
import requests

def summary(request):
    url = 'https://api.covid19api.com/summary'
    try:
        json_data = urllib.request.urlopen(url)
        data = json.load(json_data)

        string = data['Date']
        date_obj = datetime.strptime(string, '%Y-%m-%dT%H:%M:%SZ')
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
        return {'error':error, 'msg':e}

def index(request):
    context = summary(request)
    return render(request, 'analysis/index.html', context)

def news(request):
    header = ({'User-Agent':
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'})
    url = "https://www.aljazeera.com/topics/events/coronavirus-outbreak.html"

    response = requests.get(url = url, headers = header)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        top_title = soup.find('a', 'topics-title').text
        news = soup.find_all('div', 'topics-sec-item')

        headers = []
        descriptions = []
        times = []
        images = []
        links = []

        for item in news:
            header = item.find('h2', 'topics-sec-item-head').text
            description = item.find('p', 'topics-sec-item-p').text
            try:
                image = item.find('img', 'img-responsive')['data-src']
            except Exception:
                image = '/assets/images/AljazeeraLogo.png'
            time = datetime.strptime(item.find('time').text, '%d %b %Y %H:%M GMT')
            link = item.find_all('a')[1]['href']

            headers.append(header)
            descriptions.append(description)
            images.append('https://www.aljazeera.com' + image)
            links.append(link.replace('/', '-', 4).replace('.html', ''))
            times.append(time)

        news = [{'header':header, 'description':description, 'image':image, 'link':link, 'time':time} for header, description, image, link, time in zip(headers, descriptions, images, links, times)]
        context = {
            'title':top_title,
            'news':news,
        }

        return render(request, 'analysis/news.html', context)
    except Exception as e:
        print(e)
        return render(request, 'analysis/news.html', {'error':True, 'link':link})
        
def crawl(url):
    url = url.replace('-', '/', 4)
    link = f'https://www.aljazeera.com{url}.html'
    header = ({'User-Agent':
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'})
    response = requests.get(url = link, headers = header)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    try:
        title = soup.find('h1', 'post-title').text
        heading = soup.find('p', 'article-heading-des').text
        time = datetime.strptime(soup.find('time').text, '%d %b %Y %H:%M GMT')
        image = 'https://www.aljazeera.com'+soup.find('img', 'main-article-media-img')['src']
        caption = soup.find('figcaption').text
        description = soup.find('div', 'article-p-wrapper').text

        article = {
            'title':title,'heading':heading,'time':time, 'image': image, 'caption':caption,'description':description
        }
        return article
    except Exception as e:
        print(e)
        return {'error':True, 'link':link}

def article(request, url):
    context = crawl(url)
    return render(request, 'analysis/article.html', context)