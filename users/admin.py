from django.contrib import admin
from users.models import User


# 사용자 
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass