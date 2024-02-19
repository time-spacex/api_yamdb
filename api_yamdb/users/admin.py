from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import MyUser


class myUserAdmin(UserAdmin):
    """Custom fields for display in the admin's page."""

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email')
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'role',
                'groups',
                'user_permissions'
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_superuser',
        'role'
    )


admin.site.register(MyUser, myUserAdmin)
