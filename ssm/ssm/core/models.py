from django.db import models


class BaseModel(models.Model):
    """
    Add created and modified indexed fields
    """
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True

    def modify(self, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)
            self.save(update_fields=list(kwargs.keys()))
