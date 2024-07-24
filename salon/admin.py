from django.contrib import admin

from .models import Salon, Master
    # , Order, Procedure, Feedback

class SaloninLine(admin.TabularInline):
    model = Salon.masters.through
    raw_id_fields = ('master',)

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    inlines = [SaloninLine]

@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
    ]
    list_display = [
        'name',
    ]
