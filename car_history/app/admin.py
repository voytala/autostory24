from django.contrib import admin
from .models import Workshop, Vehicle, Repair, ContactRequest

admin.site.register(Vehicle)
admin.site.register(Repair)
admin.site.register(ContactRequest)

class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active')  # Dodaj pole 'is_active' do listy
    list_filter = ('is_active',)  # Umożliw filtrację po 'is_active'
    search_fields = ('username', 'email')  # Dodaj pole 'email' do wyszukiwania
    actions = ['activate_users', 'deactivate_users']

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
    activate_users.short_description = "Aktywuj użytkowników"

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_users.short_description = "Dezaktywuj użytkowników"

admin.site.register(Workshop, WorkshopAdmin)
