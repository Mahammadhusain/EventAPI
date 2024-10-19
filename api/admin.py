from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from api.models import User,Event,Ticket

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'role', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser' , 'role')
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('role', )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

admin.site.register(User, UserAdmin)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("available_ticket_stock", "tickets_sold", "total_tickets", "date", "name","id")[::-1]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("purchase_date", "quantity", "event", "user","id")[::-1]
