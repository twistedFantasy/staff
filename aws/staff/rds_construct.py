from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds,
    core,
)
from aws_cdk.aws_ssm import StringParameter


class RDSConstruct(core.Construct):

    def __init__(self, scope: core.Construct, id: str, *, app_env: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        security_group_params = {
            'security_group_name': f'staff-rds-{app_env}-ssm-security-group',
            'description': f'staff: security group for rds ssm({app_env})',
            'vpc': vpc,
        }
        security_group = ec2.SecurityGroup(self, 'staff-security-group', **security_group_params)
        security_group.add_ingress_rule(peer=ec2.Peer.ipv4("80.249.81.179"),
                                        connection=ec2.Port(
                                            string_representation='codex-soft office',
                                            protocol=ec2.Protocol.TCP,
                                            from_port=5432,
                                            to_port=5432,
                                        ))

        rds_params = {
            'engine': rds.DatabaseInstanceEngine.POSTGRES,
            'license_model': rds.LicenseModel.GENERAL_PUBLIC_LICENSE,
            'database_name': StringParameter.value_for_string_parameter(f'/{app_env}/ssm/DATABASE_NAME'),
            'master_username': StringParameter.value_for_string_parameter(f'/{app_env}/ssm/DATABASE_USER'),
            'master_user_password': StringParameter.value_for_string_parameter(f'/{app_env}/ssm/DATABASE_PASSWORD'),
            'instance_class': ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3_AMD, ec2.InstanceSize.MICRO),
            'instance_identifier': f'staff-{app_env}-ssm',
            'backup_retention': core.Duration.days(7),
            'delete_automated_backups': True,
            'security_groups': [security_group],
            'allocated_storage': 20,
            'engine_version': '11.5-R1',
            'vpc': vpc,

        }
        rds.DatabaseInstance(self, 'staff-rds', **rds_params)
