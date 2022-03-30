from django.urls import path #django's path fx
from . import views #importing all views from the blog app

urlpatterns = [
    #assings a view called base_map to the root URL
    path('', views.base_map, name='base_map'),
]