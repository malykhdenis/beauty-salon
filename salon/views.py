from django.shortcuts import render
from django.contrib.auth.decorators import login_required


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
