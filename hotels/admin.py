from django.contrib import admin
from .models import Hotel, Disponibility

# Register your models here.


class DisponibilityInline(admin.TabularInline):
    model = Disponibility
    extra = 0


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'city']
    inlines = [DisponibilityInline]
