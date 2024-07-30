import uuid

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from environs import Env
from yookassa import Configuration, Payment

from .models import Order

env = Env()
env.read_env()


def index(request):
    return render(request, "salon/index.html")


@login_required
def contacts(request):
    return render(request, "salon/contacts.html")


@login_required
def reviews(request):
    return render(request, "salon/reviews.html")


@login_required
def masters(request):
    return render(request, "salon/master.html")


@login_required
def services(request):
    return render(request, "salon/service.html")


def popup(request):
    return render(request, "salon/popup.html")


@login_required
def service(request):
    return render(request, "salon/service.html")


def notes(request):
    return render(request, "salon/notes.html")


def payment(request):
    """Оплата заказа."""
    Configuration.account_id = env.int('YOOKASSA_ACCOUNT_ID')
    Configuration.secret_key = env.str('YOOKASSA_SECRET_KEY')

    # order = Order.objects.get(user=request.user)  # получение заказа текущего пользователя

    payment = Payment.create({
        "amount": {
            "value": "3900",  # str(order.price)
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://beauty_salon.com/"  # страница редиректа после оплаты, только https
        },
        "capture": True,
        "description": "Оплата заказа"
    }, uuid.uuid4())

    return HttpResponseRedirect(payment.confirmation.confirmation_url)
