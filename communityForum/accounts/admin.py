from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Profile

admin.site.register(Profile)
admin.site.unregister(Group)


#Dashboard Styling

admin.site.site_header = "ATTC Community Forum"
admin.site.site_title = "ATTC Community Forum "
admin.site.index_title = " Forum Database"