import uuid

from django.http import HttpResponseRedirect
from django.shortcuts import render
from environs import Env
from yookassa import Configuration, Payment

from .models import Order

env = Env()
env.read_env()


def index(request):
    return render(request, "salon/index.html")


def contacts(request):
    return render(request, "salon/contacts.html")


def reviews(request):
    return render(request, "salon/reviews.html")


def masters(request):
    return render(request, "salon/master.html")


def services(request):
    return render(request, "salon/service.html")


def popup(request):
    return render(request, "salon/popup.html")


def service(request):
    return render(request, "salon/service.html")


def notes(request):
    return render(request, "salon/notes.html")


def payment(request):
    """Оплата заказа."""
    Configuration.account_id = env.int('YOOKASSA_ACCOUNT_ID')
    Configuration.secret_key = env.str('YOOKASSA_SECRET_KEY')

    order = Order.objects.get(user=request.user)

    payment = Payment.create({
        "amount": {
            "value": "100",  # str(order.price)
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://beauty_salon.com/"
        },
        "capture": True,
        "description": "Оплата заказа"
    }, uuid.uuid4())

    return HttpResponseRedirect(payment.confirmation.confirmation_url)
