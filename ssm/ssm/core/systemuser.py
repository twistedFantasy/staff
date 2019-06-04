import os
import importlib

import django; django.setup()
from django.db import transaction
models = importlib.import_module(f"{os.environ['PROJECT']}.users.models")

if os.environ['SYSTEM_EMAIL'] and os.environ['SYSTEM_PASSWORD']:
    if not models.User.objects.filter(email=os.environ['SYSTEM_EMAIL']).exists():
        with transaction.atomic():
            models.User.objects.filter(email=os.environ['SYSTEM_EMAIL']).delete()
            models.User.objects.create_superuser(os.environ['SYSTEM_EMAIL'], os.environ['SYSTEM_PASSWORD'])
