from django.contrib import admin

# Register your models here.
from .models import VagrantBox, SearchBacklog

@admin.register(VagrantBox)
class VagrantBoxAdmin(admin.ModelAdmin):
    list_display = [f.name for f in VagrantBox._meta.fields]


@admin.register(SearchBacklog)
class SearchBacklogAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SearchBacklog._meta.fields]



