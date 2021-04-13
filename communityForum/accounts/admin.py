from django.contrib import admin
from .models import Profile,Question,Answer,Category


#Dashboard Styling
admin.site.site_header = "ATTC Community Forum"
admin.site.site_title = "Developers Console"
admin.site.index_title = "Community Forum Database"


admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Category)