from django.contrib import admin
from .models import rider

class webAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(rider)
