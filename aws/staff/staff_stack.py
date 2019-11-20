from aws_cdk import (
    core,
)

from staff.vpc_construct import VPCConstruct
from staff.ecs_construct import ECSConstruct
from staff.ecr_construct import ECRConstruct
from staff.rds_construct import RDSConstruct


class StaffStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, *, app_env: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = VPCConstruct(self, 'Staff-VPC-Construct', app_env=app_env)
        RDSConstruct(self, 'Staff-RDS-Construct', app_env=app_env, vpc=vpc.object)
        ECRConstruct(self, 'Staff-ECR-Construct', app_env=app_env)
        ECSConstruct(self, 'Staff-ECS-Construct', app_env=app_env, vpc=vpc.object)
