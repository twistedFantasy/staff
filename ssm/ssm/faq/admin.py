from django.contrib import admin

from ssm.faq.models import FAQ


class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'active']
    search_fields = ['question', 'description']
    fieldsets = [
        (None, {'fields': ['question', 'description', 'order', 'active']})
    ]


admin.site.register(FAQ, FAQAdmin)
