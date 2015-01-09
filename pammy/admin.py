'''Pammy admin classes'''
from django.contrib import admin

from .models import Allocation

class AllocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'network', 'parent')

admin.site.register(Allocation, AllocationAdmin)
