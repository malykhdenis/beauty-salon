from django.contrib import admin

from .models import Salon, Master, Service, Time, Feedback, Order


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
