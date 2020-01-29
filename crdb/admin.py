from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

from crdb.models import Person, Project, Relationship, EmailAddress, Website


class EmailAddressInline(admin.TabularInline):
    model = EmailAddress
    fields=['id', 'is_primary', 'email', 'verified_ts',]
    readonly_fields=['id', 'is_primary', 'verified_ts', ]
    extra = 0


class PersonAdmin(UserAdmin):
    inlines = [EmailAddressInline, ]
    list_display = ('username', 'email', 'date_joined', 'last_login')
    ordering = ('-date_joined', 'username')
    search_fields = ('username', 'first_name', 'last_name', 'emailaddress__email')
    readonly_fields = ('last_login', 'date_joined')
    fieldsets = (
        ("Primary Fields", {'fields': ('username', 'first_name', 'last_name',
            'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined', 'password')}),
        ("Profile Fields", {'fields': ('websites', 'gender', 'pronouns', 'location', 'phone')}),
    )


# Register the other models too
admin.site.register(Person, PersonAdmin)
admin.site.register(Project)
admin.site.register(Relationship)
