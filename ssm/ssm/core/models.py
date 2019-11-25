from urllib.parse import urlencode

from django.db import models
from django.conf import settings

from ssm.core.helpers import delimit


class BaseModel(models.Model):
    """
    Add created and modified indexed fields
    """
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True

    @classmethod
    def get_admin_url(cls, *args, **kw):
        url = f'{settings.ADMIN_URL}{cls._meta.app_label}/{cls._meta.model_name}/'
        url += (delimit(list(args), sep='/') + '/') if args else ''
        if kw:
            query = [(k, kw[k]) for k in sorted(kw)]
            sep = '&' if '?' in url else '?'
            url += f'{sep}{urlencode(query)}'
        return url

    @property
    def change_url(self):
        return self.get_admin_url(self.id, 'change')

    @property
    def action_url(self):
        return self.get_admin_url(id=self.id)


    @property
    def admin_url(self):
        return self.get_admin_url()

    def modify(self, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)
            self.save(update_fields=list(kwargs.keys()))
