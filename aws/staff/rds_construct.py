from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds,
    core,
)
from aws_cdk.aws_ssm import StringParameter as Param


class RDSConstruct(core.Construct):

    @property
    def object(self):
        return self._rds

    def __init__(self, scope: core.Construct, id: str, *, app_env: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        rds_params = {
            'engine': "postgres",
            'db_name': Param.value_for_string_parameter(self, f'/{app_env}/ssm/DATABASE_NAME'),
            'master_username': Param.value_for_string_parameter(self, f'/{app_env}/ssm/DATABASE_USER'),
            'master_user_password': Param.value_for_string_parameter(self, f'/{app_env}/ssm/DATABASE_PASSWORD'),
            'db_instance_class': 'db.t3.micro',
            'db_instance_identifier': f'staff-{app_env}-ssm',
            'backup_retention_period': 7,
            'delete_automated_backups': True,
            'storage_type': 'gp2',
            'allocated_storage': '20',
            'engine_version': '11.5',
            'deletion_protection': False,
            'auto_minor_version_upgrade': True,
            'publicly_accessible': True,
            'storage_encrypted': False,
            'copy_tags_to_snapshot': False,
            'multi_az': False,
        }
        self._rds = rds.CfnDBInstance(self, 'staff-rds', **rds_params)
