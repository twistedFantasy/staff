from aws_cdk import (
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_ecr as ecr,
    aws_rds as rds,
    aws_logs as logs,
    aws_elasticloadbalancingv2 as elbv2,
    core,
)
from aws_cdk.aws_ssm import StringParameter as _


class ECSConstruct(core.Construct):

    def __init__(self, scope: core.Construct, id: str, *, app_env: str, vpc: ec2.Vpc, rds: rds.CfnDBInstance,
                 repository: ecr.Repository, log_group: logs.LogGroup, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        cluster = ecs.Cluster(self, 'staff-cluster', cluster_name=f'staff-cluster-{app_env}', vpc=vpc)

        # task definition
        task_definition = ecs.FargateTaskDefinition(self, f'staff-task-def-{app_env}', cpu=512, memory_limit_mib=1024)
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

        task_definition_params = {
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
             },
            'logging': ecs.LogDriver(stream_prefix='ecs-', log_group=log_group)
        }
        container = task_definition.add_container("web", **task_definition_params)
        container.add_port_mappings(container_port=80)

        # fargate service
        service_sg_params = {
            'security_group_name': f'staff-fargate-service-security-group-{app_env}',
            'description': f'staff balancer security group for {app_env}',
            'vpc': vpc,
        }
        service_sc = ec2.SecurityGroup(self, f'staff-balancer-security-group', **service_sg_params)
        service_sc.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), 'allow 80 port access from the world')
        service_sc.add_egress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), '')
        service_params = {
            'service_name': 'staff-fargate-service',
            'cluster': cluster,
            'task_definition': task_definition,
            'desired_count': 1,
            'assign_public_ip': True,
            'security_group': service_sc,
            'vpc_subnets': vpc.public_subnets,
        }
        service = ecs.FargateService(self, 'staff-fargate-service', **service_params)

        # application load balancer
        balancer_sg_params = {
            'security_group_name': f'staff-balancer-security-group-{app_env}',
            'description': f'staff balancer security group for {app_env}',
            'vpc': vpc,
        }
        balancer_sc = ec2.SecurityGroup(self, f'staff-balancer-security-group', **balancer_sg_params)
        balancer_sc.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), 'allow 80 port access from the world')
        balancer_sc.add_egress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), '')

        balancer_params = {
            'http2_enabled': True,
            'ip_address_type': elbv2.IpAddressType.IPV4,
            'security_group': balancer_sc,
            'vpc': vpc,
            'deletion_protection': False,
            'internet_facing': True,
            'load_balancer_name': f'staff-application-balancer-{app_env}',
            'vpc_subnets': vpc.public_subnets,
        }
        balancer = elbv2.ApplicationLoadBalancer(self, 'staff-application-balancer', **balancer_params)
        listener = balancer.add_listener('staff-listener', open=True, port=80)
        listener.add_target_groups('staff-target-group', target_groups=[service.load_balancer_target(
            container_name='web', container_port=80,
        )])
