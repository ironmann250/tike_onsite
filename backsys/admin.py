from django.contrib import admin

# Register your models here.
from .models import user,event,category,subcategory,ticket_type,ticket,review

admin.site.register(user)
admin.site.register(event)
admin.site.register(category)  
admin.site.register(subcategory)
admin.site.register(ticket_type)
admin.site.register(ticket)
admin.site.register(review)
