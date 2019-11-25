from django.utils.safestring import mark_safe

from ssm.core.helpers import pluralize, delimit


class BaseAdminMixin:

    def get_href(self, link, *args, **kw):
        label = delimit(args, sep=' ')
        kw = kw or {'style': 'white-space: nowrap;'}
        attr = delimit([f'{k}="{v}"' for k, v in kw.items()], sep=' ')
        return f'<a href="{link}" {attr}>{label}</a>'

    def get_change_url(self, obj, label=None):
        html = self.get_href(obj.change_url, label or obj.__class__.__name__)
        return mark_safe(html)

    def get_action_url(self, obj, label=None):
        html = self.get_href(obj.action_url, label or obj.__class__.__name__)
        return mark_safe(html)

    def get_url(self, cls, singular=None, plural=None, **kw):
        link = cls.get_admin_url(**kw)
        count = cls.objects.filter(**kw).count()
        label = pluralize(count, singular or cls.__name__.lower(), plural=plural)
        html = self.get_href(link, count, label)
        return mark_safe(html)
