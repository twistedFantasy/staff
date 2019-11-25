from aws_cdk import (
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_ecr as ecr,
    aws_ecs_patterns as ecs_patterns,
    core,
)
from aws_cdk.aws_ssm import StringParameter as Param


class ECSConstruct(core.Construct):

    def __init__(self, scope: core.Construct, id: str, *, app_env: str, vpc: ec2.Vpc, repository: ecr.Repository,
                 **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        cluster = ecs.Cluster(self, 'staff-cluster', cluster_name='staff-cluster', vpc=vpc)

        params = {
            'assign_public_ip': True,
            'cpu': 512,
            'memory_limit_mib': 1024,
            'cluster': cluster,
            'desired_count': 1,
            'listener_port': 80,
            'public_load_balancer': True,
            'public_load_balancer': True,
            'task_image_options': {
                'image': ecs.ContainerImage.from_ecr_repository(repository, tag=app_env),
                'environment': {
                    'ENV': f'{app_env}',
                    'PROJECT': 'ssm',
                    'PYTHONPATH': '/var/staff/ssm/',
                    'CORS_ORIGIN_ALLOW_ALL': True,
                    'DJANGO_SETTINGS_MODULE': 'ssm.settings',
                },
                'secrets': {
                    'ADMIN_URL': '',
                    'DATABASE_NAME': Param.value_for_string_parameter(f'/{app_env}/ssm/DATABASE_NAME'),
                    'TEST_DATABASE_NAME': Param.value_for_string_parameter(f'/{app_env}/ssm/TEST_DATABASE_NAME'),
                    'DATABASE_USER': Param.value_for_string_parameter(f'/{app_env}/ssm/DATABASE_USER'),
                    'DATABASE_PASSWORD': Param.value_for_string_parameter(f'/{app_env}/ssm/DATABASE_PASSWORD'),
                    'DATABASE_HOST': Param.value_for_string_parameter(f'/{app_env}/ssm/DATABASE_HOST'),
                    'DATABASE_PORT': Param.value_for_string_parameter(f'/{app_env}/ssm/DATABASE_PORT'),
                    'EMAIL_HOST_USER': '',
                    'EMAIL_HOST_PASSWORD': '',
                    'CELERY_BROKER_URL': '',
                    'CELERY_RESULT_BACKEND': '',
                    'CELERY_LOG_LEVEL': '',
                    'CELERY_GENERAL_QUEUE': '',
                    'CELERY_REPORT_QUEUE': '',
                    'SYSTEM_EMAIL': Param.value_for_string_parameter(f'/{app_env}/ssm/SYSTEM_EMAIL'),
                    'SYSTEM_PASSWORD': Param.value_for_string_parameter(f'/{app_env}/ssm/SYSTEM_PASSWORD'),
                }
            },
        }
        ecs_patterns.ApplicationLoadBalancedFargateService(self, "staff-fargate-service", **params)
