import csv

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.http import HttpResponse

from accounts.models import UserProfile


# Register your models here.

class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_bio', 'get_location', 'get_website')
    list_select_related = ('user_info', )
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names + ['bio', 'website', 'location'])
        for obj in queryset:
            row = [getattr(obj, field) for field in field_names]
            if getattr(obj, 'user_info', False):
                row.append(obj.user_info.bio)
                row.append(obj.user_info.website)
                row.append(obj.user_info.location)
            writer.writerow(row)

        return response

    export_as_csv.short_description = "Export Selected"

    def get_bio(self, instance):
        return instance.user_info.bio

    def get_location(self, instance):
        return instance.user_info.location

    def get_website(self, instance):
        return instance.user_info.website

    get_bio.short_description = 'Bio'
    get_location.short_description = 'Location'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)