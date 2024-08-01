from django.urls import path

from .views import (index, services, contacts, masters, notes, payment,
                    reviews, service_finally)

app_name = 'salon'
urlpatterns = [
    path('', index, name='index'),
    path('contacts/', contacts, name='contacts'),
    path('masters/', masters, name='masters'),
    path('reviews/', reviews, name='reviews'),
    path('services/', services, name='services'),
    path('service-finally/', service_finally, name='service-finally'),
    path('notes/', notes, name='notes'),
    path('payment/', payment, name='payment'),
]
