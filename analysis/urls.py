from django.urls import path
from analysis.views import index, news

app_name = 'analysis'

urlpatterns = [
    path('', index, name='index'),
    path('news/', news, name='news'),
]