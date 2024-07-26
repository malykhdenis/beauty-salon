from django.shortcuts import render


def index(request):
    return render(request, "salon/index.html")


def contacts(request):
    return render(request, "salon/contacts.html")


def reviews(request):
    return render(request, "salon/reviews.html")


def masters(request):
    return render(request, "salon/masters.html")


def services(request):
    return render(request, "salon/services.html")


def popup(request):
    return render(request, "salon/popup.html")


def service(request):
    return render(request, "salon/service.html")
