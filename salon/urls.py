from django.urls import path

from .views import index, services, contacts, masters, reviews, service

app_name = 'salon'
urlpatterns = [
    path('', index, name='index'),
    path('contacts/', contacts, name='contacts'),
    path('masters/', masters, name='masters'),
    path('reviews/', reviews, name='reviews'),
    path('services/', services, name='services'),
    path('service/', service, name='service'),
]
