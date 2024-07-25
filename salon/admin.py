from django.contrib import admin

import requests
from environs import Env

from .models import Advertising, Salon, Master, Service, Time, Feedback, Order

env = Env()
env.read_env()


class MasterinLine(admin.TabularInline):
    model = Salon.master_salons.through
    raw_id_fields = ('salon',)

class TimeinLine(admin.TabularInline):
    model = Salon.available_time.through
    raw_id_fields = ('salon',)

class ServiceinLine(admin.TabularInline):
    model = Salon.salon_services.through
    # raw_id_fields = ('salon',)
    # raw_id_fields = ('name',)

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname']
    # raw_id_fields = ('service', 'salon')


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    inlines = [
        MasterinLine,
        ServiceinLine,
        TimeinLine
    ]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Time)
class TimeAdmin(admin.ModelAdmin):
    pass


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'master',)
    raw_id_fields = ('user', 'master',)
    list_filter = ('master',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'master', 'service', 'paid')
    list_filter = ('paid', 'salon', 'master', 'time', 'service',)
    raw_id_fields = ('user', 'salon', 'master', 'time', 'service',)


@admin.register(Advertising)
class AdvertisingModel(admin.ModelAdmin):
    list_display = ('url', 'text', 'responses',)
    readonly_fields = ('url', 'responses',)

    def changelist_view(self, request, extra_context=None):
        advertising = Advertising.objects.all()
        headers = {
            "Authorization": f"Bearer {env.str('TLY_API_TOKEN')}"
        }
        url = "https://t.ly/api/v1/link/stats"
        for ad in advertising:
            params = {"short_url": ad.url}
            response = requests.get(url,
                                    headers=headers,
                                    params=params)
            response.raise_for_status()
            ad.responses = response.json()["clicks"]
        Advertising.objects.bulk_update(advertising, ['responses'])
        return super().changelist_view(request, extra_context=extra_context)
