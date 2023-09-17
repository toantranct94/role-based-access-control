from aws_cdk import aws_cognito as _cognito
from aws_cdk import aws_lambda as _lambda
from constructs import Construct


class Cognito(Construct):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        props: dict = {},
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        env: str = props.get('env', 'dev')
        callback_domain: str = 'https://localhost.com'
        post_confirmation: _lambda.Function = props.get(
            'post_confirmation', None)
        custom_auth: _lambda.Function = props.get('custom_auth', None)

        self.user_pool = _cognito.UserPool(
            self, f'{env}-userpool')

        _cognito.CfnUserPoolGroup(
            self, "admin",
            user_pool_id=self.user_pool.user_pool_id,
            group_name="admin"
        )

        _cognito.CfnUserPoolGroup(
            self, "individual",
            user_pool_id=self.user_pool.user_pool_id,
            group_name="individual"
        )

        _cognito.CfnUserPoolDomain(
            self, f"{env}-cognito-domain",
            domain='rbac-test-1',
            user_pool_id=self.user_pool.user_pool_id,
        )

        self.client = _cognito.UserPoolClient(
            self, f"{env}-cognito-client",
            user_pool=self.user_pool,
            supported_identity_providers=[
                _cognito.UserPoolClientIdentityProvider.COGNITO,
            ],
            o_auth={
                "callback_urls": [callback_domain]
            }
        )

        if post_confirmation:
            self.user_pool.add_trigger(
                _cognito.UserPoolOperation.POST_CONFIRMATION,
                post_confirmation)

        if custom_auth:
            custom_auth.add_environment(
                'COGNITO_APP_CLIENT_ID', self.client.user_pool_client_id)
            custom_auth.add_environment(
                'COGNITO_USER_POOL_ID', self.user_pool.user_pool_id)
