from django.contrib import admin
from DryIce.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'uuid')
    
admin.site.register(UserProfile, UserProfileAdmin)