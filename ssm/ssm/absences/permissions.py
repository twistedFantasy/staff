from ssm.core.permissions import IsAllowedMethodOrStaff


class CustomIsAllowedMethodOrStaff(IsAllowedMethodOrStaff):
    methods = ['GET', 'HEAD', 'OPTIONS', 'POST', 'PATCH', 'DELETE']
