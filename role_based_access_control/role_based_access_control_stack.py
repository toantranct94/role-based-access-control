from aws_cdk import Stack
from constructs import Construct

from role_based_access_control.resources.api_gateway.api_gateway_construct import \
    APIGateway
from role_based_access_control.resources.cognito.congito_construct import \
    Cognito
from role_based_access_control.resources.dynamodb.dynamodb_construct import \
    DynamoDB
from role_based_access_control.resources.lambdas.lambda_construct import Lambda


class RoleBasedAccessControlStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        props: dict = {},
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.props = props

        self._lambda = Lambda(
            self, 'lambda',
            props={
                **self.props
            }
        )

        self.cognito = Cognito(
            self, 'cognito',
            props={
                **self.props,
                'post_confirmation': self._lambda.post_confirmation,
                'custom_auth': self._lambda.custom_auth,
            }
        )

        self.dynamodb = DynamoDB(
            self, 'dynamodb-cvc',
            props={
                **self.props,
                'custom_auth': self._lambda.custom_auth,
            }
        )

        self.apigw = APIGateway(
            self, 'apigw',
            props={
                **self.props,
                'custom_auth': self._lambda.custom_auth,
                'backend_handler': self._lambda.backend_handler
            }
        )
