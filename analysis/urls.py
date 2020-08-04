from django.urls import path
from analysis.views import index

app_name = 'analysis'

urlpatterns = [
    path('', index, name='index')
]