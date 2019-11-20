from aws_cdk import (
    aws_ec2 as ec2,
    core,
)


class VPCConstruct(core.Construct):

    @property
    def object(self):
        return self._vpc

    def __init__(self, scope: core.Construct, id: str, *, app_env: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        params = {
            'cidr': '10.0.0.0/16',
            'enable_dns_hostnames': True,
            'enable_dns_support': True,
            'max_azs': 2,
            'subnet_configuration': [ec2.SubnetConfiguration(
                                        cidr_mask=24,
                                        name=f'{app_env}-staff-public',
                                        subnet_type=ec2.SubnetType.PUBLIC,
            )]
        }
        self._vpc = ec2.Vpc(self, 'staff-vpc', **params)
