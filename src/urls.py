from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.auth import views as acc
from django.urls import path, include

from . import settings


urlpatterns = [
    path('', include('salon.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('login', acc.LoginView.as_view(), name='login'),
    path('logout', acc.LogoutView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
