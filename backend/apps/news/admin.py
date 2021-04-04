from django.contrib import admin
from .models import News

class MediaAdmin(admin.ModelAdmin):
    list_display_links = ['pk']
    ordering = ('pk',)
    list_display = ('pk','title','description','likes')
    
admin.site.register(News,MediaAdmin)
