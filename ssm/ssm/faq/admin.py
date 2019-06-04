from django.contrib import admin

from ssm.faq.models import FAQ


class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'active']
    search_fields = ['question', 'answer']
    fieldsets = [
        (None, {'fields': ['question', 'answer', 'order', 'active']})
    ]


admin.site.register(FAQ, FAQAdmin)
