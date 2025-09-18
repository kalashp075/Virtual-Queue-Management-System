from django.contrib import admin


from .models import Service, QueueEntry, Profile

admin.site.register(Service)
admin.site.register(QueueEntry)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'fullname', 'birthdate')