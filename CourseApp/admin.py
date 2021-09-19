from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Image)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(OfflineCourse)
admin.site.register(OnlineCourse)
