from aws_cdk import (
    core,
)

from staff.iam_construct import IAMConstruct
from staff.logs_construct import LogsConstruct
from staff.vpc_construct import VPCConstruct
from staff.ecs_construct import ECSConstruct
from staff.ecr_construct import ECRConstruct
from staff.rds_construct import RDSConstruct


class StaffStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, *, app_env: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        IAMConstruct(self, 'Staff-IAM-Construct', app_env=app_env)
        vpc = VPCConstruct(self, 'Staff-VPC-Construct', app_env=app_env)
        logs = LogsConstruct(self, 'Staff-Logs-Construct', app_env=app_env)
        rds = RDSConstruct(self, 'Staff-RDS-Construct', app_env=app_env, vpc=vpc.object)
        ecr = ECRConstruct(self, 'Staff-ECR-Construct', app_env=app_env)
        params = {
            'app_env': app_env,
            'vpc': vpc.object,
            'rds': rds.object,
            'repository': ecr.object,
            'log_group': logs.object,
        }
        ECSConstruct(self, 'Staff-ECS-Construct', **params)
