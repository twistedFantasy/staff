from aws_cdk import (
    aws_ecr as ecr,
    core,
)


class ECRConstruct(core.Construct):

    def __init__(self, scope: core.Construct, id: str, *, app_env: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        repository = ecr.Repository(self, 'staff-repository')
        repository.add_lifecycle_rule(tag_prefix_list=["stg"], max_image_count=5)
        repository.add_lifecycle_rule(tag_prefix_list=["prd"], max_image_count=5)
