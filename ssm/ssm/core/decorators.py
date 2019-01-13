from django.contrib import messages


def message_user(msg=None):
    def decorator(func):
        def inner(self, request, queryset, *args, **kw):
            try:
                result = func(self, request, queryset, *args, **kw)
                if msg:
                    self.message_user(request, msg)
                return result
            except Exception as e:
                self.message_user(request, e, level=messages.ERROR)
        return inner
    return decorator
