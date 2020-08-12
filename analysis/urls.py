from django.urls import path
from analysis.views import index, news, article, license

app_name = 'analysis'

urlpatterns = [
    path('', index, name='index'),
    path('license/', license, name='license'),
    path('news/', news, name='news'),
    path('news/article/<str:url>/', article, name='article'),
]