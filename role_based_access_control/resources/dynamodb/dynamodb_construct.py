from aws_cdk import aws_dynamodb as _dynamodb
from aws_cdk import aws_lambda as _lambda
from constructs import Construct


class DynamoDB(Construct):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        props: dict = {},
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        env = props.get('env', 'dev')

        custom_auth: _lambda.Function = props.get('custom_auth', None)

        self.auth_table = _dynamodb.Table(
            self, f'{env}-auth-policy-store',
            partition_key=_dynamodb.Attribute(
                name="group",
                type=_dynamodb.AttributeType.STRING
            )
        )

        if custom_auth:
            custom_auth.add_environment(
                'TABLE_NAME', self.auth_table.table_name)
            self.auth_table.grant_read_write_data(custom_auth)
