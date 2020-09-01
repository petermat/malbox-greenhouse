from django.contrib import admin

# Register your models here.
from .models import VagrantBox, SearchBacklog, VagrantPoolLog


def clean_and_wait(modeladmin, request, queryset):
    queryset.update(processed_at=None, status_code="W", status_message="", worker_name="")
clean_and_wait.short_description = "Clean selected Boxes and set them to WAIT"

@admin.register(VagrantBox)
class VagrantBoxAdmin(admin.ModelAdmin):
    list_display = [f.name for f in VagrantBox._meta.fields]
    list_filter = ('status_code', 'worker_name')
    search_fields = ('status_message', 'description')
    actions = [clean_and_wait]


@admin.register(VagrantPoolLog)
class VagrantPoolLogAdmin(admin.ModelAdmin):
    list_display = [f.name for f in VagrantPoolLog._meta.fields]
    list_filter = ('vagrant_box','status_code')


@admin.register(SearchBacklog)
class SearchBacklogAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SearchBacklog._meta.fields]




