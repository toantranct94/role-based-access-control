from aws_cdk import aws_lambda as _lambda
from constructs import Construct


class Lambda(Construct):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        props: dict = {},
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        run_time: _lambda.Runtime = _lambda.Runtime.PYTHON_3_9

        self.post_confirmation = _lambda.Function(
            self, 'PostConfirmation',
            runtime=run_time,
            handler='lambda_function.lambda_handler',
            code=_lambda.Code.from_asset(
                './role_based_access_control/resources/lambdas/post_confirmation/src')
        )

        self.custom_auth = _lambda.Function(
            self, 'CustomAuth',
            runtime=run_time,
            handler='lambda_function.lambda_handler',
            code=_lambda.Code.from_asset(
                './role_based_access_control/resources/lambdas/custom_auth/src')
        )

        self.backend_handler = _lambda.Function(
            self, 'BackendHandler',
            runtime=run_time,
            handler='lambda_function.lambda_handler',
            code=_lambda.Code.from_asset(
                './role_based_access_control/resources/lambdas/backend_handler/src')
        )
