from django.contrib.auth import views as acc
from django.urls import path

from user.views import register

app_name = 'user'
urlpatterns = [
    path('register/', register, name='register'),
]

urlpatterns += [
    path('login', acc.LoginView.as_view(), name='login'),
    path('logout', acc.LogoutView.as_view(), name='logout'),
]
