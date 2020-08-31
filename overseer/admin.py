from django.contrib import admin

# Register your models here.
from .models import VagrantBox, SearchBacklog, VagrantPoolLog


@admin.register(VagrantBox)
class VagrantBoxAdmin(admin.ModelAdmin):
    list_display = [f.name for f in VagrantBox._meta.fields]
    list_filter = ('status_code', 'worker_name')


@admin.register(VagrantPoolLog)
class VagrantPoolLogAdmin(admin.ModelAdmin):
    list_display = [f.name for f in VagrantPoolLog._meta.fields]
    list_filter = ('vagrant_box','status_code')


@admin.register(SearchBacklog)
class SearchBacklogAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SearchBacklog._meta.fields]




