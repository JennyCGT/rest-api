from django.contrib import admin
from .models import Media

class MediaAdmin(admin.ModelAdmin):
    list_display_links = ['pk']
    ordering = ('pk',)
    list_display = ('pk','title','description','image')
    
admin.site.register(Media,MediaAdmin)
