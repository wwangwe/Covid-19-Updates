from django.urls import path
from analysis.views import index, news, article

app_name = 'analysis'

urlpatterns = [
    path('', index, name='index'),
    path('news/', news, name='news'),
    path('news/article/<str:url>/', article, name='article'),
]