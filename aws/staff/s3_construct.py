from aws_cdk import (
    aws_s3 as s3,
    core,
)


class S3Construct(core.Construct):

    def __init__(self, scope: core.Construct, id: str, *, app_env: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        params = {
            'access_control': s3.BucketAccessControl.PRIVATE,
            'block_public_access': s3.BlockPublicAccess.BLOCK_ALL,
            'bucket_name': f'staff-s3-{app_env}',
            'removal_policy': core.RemovalPolicy.DESTROY,
            'versioned': False,
        }
        s3.Bucket(self, 'staff-s3', **params)
