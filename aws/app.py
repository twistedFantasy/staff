#!/usr/bin/env python3

import os

from aws_cdk import core

from staff.staff_stack import StaffStack


if os.environ.get("ENV") and os.environ["ENV"] in ['stg', 'prod']:
    app = core.App()
    StaffStack(app, f'staff-cdk-{os.environ["ENV"]}', app_env=os.environ["ENV"], env={'region': 'us-east-2'})
    app.synth()
else:
    raise Exception("No ENV value was specified, supported options: stg, prod")


