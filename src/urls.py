from django.contrib import admin
from django.contrib.auth import views as acc
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('login', acc.LoginView.as_view(), name='login'),
    path('logout', acc.LogoutView.as_view(), name='logout'),
]
