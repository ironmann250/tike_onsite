from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import profile, ticket,Show,tickettype
admin.site.register(profile)
admin.site.register(ticket)
admin.site.register(Show)
admin.site.register(tickettype)
