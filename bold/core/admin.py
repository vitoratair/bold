from django.contrib import admin

from core.models import Subscriber

#### All adapters and resources must be import here ####
from core.movies import admin as movies_admin


class SubscriberAdmin(admin.ModelAdmin):
    list_filter = ('resource',)
    list_display = ('name', 'resource')
    search_fields = ('name','client', 'resource')

admin.site.register(Subscriber, SubscriberAdmin)
