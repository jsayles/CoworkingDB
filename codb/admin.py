from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

from codb.models import Person, Company, EmailAddress, Website


# class UserProfileInline(admin.StackedInline):
#     model = UserProfile
#     can_delete = False
#     max_num = 1
#     exclude = ('websites', )
#
#
# class EmailAddressInline(admin.TabularInline):
#     model = EmailAddress
#     fields=['id', 'is_primary', 'email', 'verified_ts',]
#     readonly_fields=['id', 'is_primary', 'verified_ts', ]
#     extra = 0
#
#
# class UserWithProfileAdmin(UserAdmin):
#     inlines = [EmailAddressInline, UserProfileInline]
#     list_display = ('username', 'email', 'date_joined', 'last_login')
#     ordering = ('-date_joined', 'username')
#     search_fields = ('username', 'first_name', 'last_name', 'emailaddress__email')
#     readonly_fields = ('last_login', 'date_joined')
#     fieldsets = (
#         (None, {'fields': ('username', 'first_name', 'last_name',
#             'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined', 'password')}),
#     )
#
#
# # Hook it all up
# admin.site.unregister(User)
# admin.site.register(User, UserWithProfileAdmin)
# admin.site.unregister(Group)
#

# Register the other models too
admin.site.register(Company)
