# from django.utils.safestring import mark_safe
#
#
# class UserAdminMixin:
#
#     def user_url(self, obj):
#         html = ''
#         if obj.user:
#             html = self.get_href(obj.user.change_url, obj.user.full_name)
#         return mark_safe(html)
#     user_url.short_description = 'User'
