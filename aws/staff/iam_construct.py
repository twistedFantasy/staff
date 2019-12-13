from aws_cdk import (
    aws_iam as iam,
    core,
)
from aws_cdk.aws_ssm import StringParameter as Param


class IAMConstruct(core.Construct):

    def __init__(self, scope: core.Construct, id: str, *, app_env: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        password = core.SecretValue.plain_text(Param.value_for_string_parameter(self, f'/{app_env}/ssm/IAM_PASSWORD'))
        user = iam.User(self, "staff-user", password=password)
        user.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))  # FIXME: subset of required permissions
