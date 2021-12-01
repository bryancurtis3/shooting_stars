from django.contrib import admin
from .models import Post, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm

class UserAdmin(BaseUserAdmin):
    model = User
    form = UserCreationForm
    fieldsets = (
        *BaseUserAdmin.fieldsets, ("Location Details", {
            "fields": (
                "location",
            ),
        }),
    )
    add_fieldsets = (
        *BaseUserAdmin.fieldsets, ("Location Details", {
            "fields": (
                "location",
            ),
        }),
    )

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Post)
