from aws_cdk import (
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_ecr as ecr,
    aws_rds as rds,
    aws_ecs_patterns as ecs_patterns,
    core,
)
from aws_cdk.aws_ssm import StringParameter as _


class ECSConstruct(core.Construct):

    def __init__(self, scope: core.Construct, id: str, *, app_env: str, vpc: ec2.Vpc, rds: rds.CfnDBInstance,
                 repository: ecr.Repository, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        cluster = ecs.Cluster(self, 'staff-cluster', cluster_name=f'staff-cluster-{app_env}', vpc=vpc)

        admin_url = _.from_string_parameter_name(self, "admin_url", f'/{app_env}/ssm/ADMIN_URL')
        db_name = _.from_string_parameter_name(self, "database_name", f'/{app_env}/ssm/DATABASE_NAME')
        test_db_name = _.from_string_parameter_name(self, "test_database_name", f'/{app_env}/ssm/TEST_DATABASE_NAME')
        db_user = _.from_string_parameter_name(self, "database_user", f'/{app_env}/ssm/DATABASE_USER')
        db_pass = _.from_string_parameter_name(self, "database_pass", f'/{app_env}/ssm/DATABASE_PASSWORD')
        db_port = _.from_string_parameter_name(self, "database_port", f'/{app_env}/ssm/DATABASE_PORT')
        email_host_user = _.from_string_parameter_name(self, "email_host_user", f'/{app_env}/ssm/EMAIL_HOST_USER')
        email_host_pass = _.from_string_parameter_name(self, "email_host_pass", f'/{app_env}/ssm/EMAIL_HOST_PASSWORD')
        broker_url = _.from_string_parameter_name(self, "celery_broker_url", f'/{app_env}/ssm/CELERY_BROKER_URL')
        backend = _.from_string_parameter_name(self, "celery_result_backend", f'/{app_env}/ssm/CELERY_RESULT_BACKEND')
        log_level = _.from_string_parameter_name(self, "celery_log_level", f'/{app_env}/ssm/CELERY_LOG_LEVEL')
        gen_queue = _.from_string_parameter_name(self, "celery_general_queue", f'/{app_env}/ssm/CELERY_GENERAL_QUEUE')
        report_queue = _.from_string_parameter_name(self, "celery_report_queue", f'/{app_env}/ssm/CELERY_REPORT_QUEUE')
        system_email = _.from_string_parameter_name(self, "system_email", f'/{app_env}/ssm/SYSTEM_EMAIL')
        system_password = _.from_string_parameter_name(self, "system_password", f'/{app_env}/ssm/SYSTEM_PASSWORD')
        params = {
            'assign_public_ip': True,
            'cpu': 512,
            'memory_limit_mib': 1024,
            'cluster': cluster,
            'desired_count': 1,
            'listener_port': 80,
            'public_load_balancer': True,
            'task_image_options': {
                'image': ecs.ContainerImage.from_ecr_repository(repository, tag=app_env),
                'environment': {
                    'ENV': f'{app_env}',
                    'PROJECT': 'ssm',
                    'PYTHONPATH': '/var/staff/ssm/',
                    'CORS_ORIGIN_ALLOW_ALL': 'True',
                    'DJANGO_SETTINGS_MODULE': 'ssm.settings',
                    'DATABASE_HOST': rds.attr_endpoint_address,
                },
                'secrets': {
                    'ADMIN_URL': ecs.Secret.from_ssm_parameter(admin_url),
                    'DATABASE_NAME': ecs.Secret.from_ssm_parameter(db_name),
                    'TEST_DATABASE_NAME': ecs.Secret.from_ssm_parameter(test_db_name),
                    'DATABASE_USER': ecs.Secret.from_ssm_parameter(db_user),
                    'DATABASE_PASSWORD': ecs.Secret.from_ssm_parameter(db_pass),
                    'DATABASE_PORT': ecs.Secret.from_ssm_parameter(db_port),
                    'EMAIL_HOST_USER': ecs.Secret.from_ssm_parameter(email_host_user),
                    'EMAIL_HOST_PASSWORD': ecs.Secret.from_ssm_parameter(email_host_pass),
                    'CELERY_BROKER_URL': ecs.Secret.from_ssm_parameter(broker_url),
                    'CELERY_RESULT_BACKEND': ecs.Secret.from_ssm_parameter(backend),
                    'CELERY_LOG_LEVEL': ecs.Secret.from_ssm_parameter(log_level),
                    'CELERY_GENERAL_QUEUE': ecs.Secret.from_ssm_parameter(gen_queue),
                    'CELERY_REPORT_QUEUE': ecs.Secret.from_ssm_parameter(report_queue),
                    'SYSTEM_EMAIL': ecs.Secret.from_ssm_parameter(system_email),
                    'SYSTEM_PASSWORD': ecs.Secret.from_ssm_parameter(system_password),
                }
            },
        }
        ecs_patterns.ApplicationLoadBalancedFargateService(self, "staff-fargate-service", **params)
