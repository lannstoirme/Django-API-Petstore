from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models
from .models import StoreStatus
from .models import Category
from .models import Order
from .models import PetManager
from .models import PetName
from .models import Price
from .models import Customer


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Order)
admin.site.register(models.PetManager)
admin.site.register(models.StoreStatus)
admin.site.register(models.PetName)
admin.site.register(models.Category)
admin.site.register(models.Price)
admin.site.register(models.Customer)
