import uuid

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Advertising, Salon, Master, Service, Time, Feedback, Order, ServiceCategory
from django.contrib.auth.decorators import login_required
from environs import Env
from yookassa import Configuration, Payment

from .models import Order

env = Env()
env.read_env()


def index(request):
    salons = Salon.objects.all()
    main_salons = []
    for salon in salons:
        main_salon = {
            'id': salon.id,
            'name': salon.name,
            'foto': salon.foto.url,
            'address': salon.address
        }
        main_salons.append(main_salon)
    data = {'main_salons': main_salons}
    return render(request, "salon/index.html", context=data)


@login_required
def contacts(request):
    return render(request, "salon/contacts.html")


@login_required
def reviews(request):
    feedbacks = Feedback.objects.all()
    viewed_feedbacks = []
    for feedback in feedbacks:
        viewed_feedback = {
            'id': feedback.id,
            'user': feedback.user,
            'master': feedback.master,
            'feedback': feedback.feedback
        }
        viewed_feedbacks.append(viewed_feedback)
    data = {'viewed_feedbacks': viewed_feedbacks}

    return render(request, "salon/reviews.html", context=data)


@login_required
def masters(request):
    masters = Master.objects.all()
    displayed_masters = []
    for master in masters:
        displayed_master = {
            'id': master.id,
            'firstname': master.firstname,
            'lastname': master.lastname,
            'speciality': master.speciality,
            'foto': master.foto.url,
            'experience': master.experience(),
            'feedback': master.feedbacks.count(),
        }
        displayed_masters.append(displayed_master)
    data = {'displayed_masters': displayed_masters}

    return render(request, "salon/master.html", context=data)


@login_required
def services(request):
    salons = Salon.objects.all()
    cats = ServiceCategory.objects.all()
    pointed_salons = []
    pointed_cats = []
    for salon in salons:
        pointed_salon = {
            'salon': salon.name,
            'address': salon.address,
        }
        pointed_salons.append(pointed_salon)
    for cat in cats:
        pointed_cat = {
            'name': cat.name,
        }
        pointed_services = []
        for serv in cat.services.all():
            pointed_service = {
                'serv_name': serv.name,
                'price': serv.price
            }
            pointed_services.append(pointed_service)
            pointed_cat['services'] = pointed_services
            service_masters = []
            for master in serv.master_services.all():
                service_master = {
                    'master_name': f'{master.firstname} {master.lastname}'
                }
                service_masters.append(service_master)
                pointed_cat['masters'] = service_masters
        pointed_cats.append(pointed_cat)


    data = {'pointed_salons': pointed_salons,
            'pointed_cats': pointed_cats,
            }

    return render(request, "salon/service.html", context=data)

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
