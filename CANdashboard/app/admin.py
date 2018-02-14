from django.contrib import admin
from .models import Charity


class CharityAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Country','Website',)
    list_filter = ('Name', 'Country','Website',)
    search_fields = ('Name',)
    prepopulated_fields = {'slug' : ('Name' ,)}

admin.site.register(Charity, CharityAdmin)

# Register your models here.
