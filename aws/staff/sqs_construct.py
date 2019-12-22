from aws_cdk import (
    aws_sqs as sqs,
    core,
)


class SQSConstruct(core.Construct):

    def __init__(self, scope: core.Construct, id: str, *, app_env: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        params = {
            'max_message_size_bytes': 262144,  # 256KiB
            'queue_name': f'staff-sqs-{app_env}.fifo',
            'retention_period': core.Duration.days(5),
            'visibility_timeout': core.Duration.hours(1),
        }
        sqs.Queue(self, 'staff-sqs', **params)
