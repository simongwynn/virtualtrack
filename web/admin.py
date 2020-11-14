from django.contrib import admin
from .models import rider, Event
from import_export.admin import ImportExportModelAdmin

class webAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    readonly_fields = ('created',)

class export1(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ('number', 'name' )
    list_display = ('number', 'name', 'state', 'event',)

class export2(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ('name','id')
    list_display = ('id','name','date','finish','event_option')



admin.site.register(rider, export1)
admin.site.register(Event,export2)
