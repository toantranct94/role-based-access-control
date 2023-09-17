import aws_cdk as cdk
from aws_cdk import aws_apigatewayv2_alpha as _apigwv2
from aws_cdk import aws_apigatewayv2_authorizers_alpha as _authorizers
from aws_cdk import aws_apigatewayv2_integrations_alpha as _integration
from aws_cdk import aws_lambda as _lambda
from constructs import Construct


class APIGateway(Construct):
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
        backend_handler: _lambda.Function = props.get('backend_handler', None)

        cors_preflight = _apigwv2.CorsPreflightOptions(
            allow_origins=['*'],
            allow_methods=[_apigwv2.CorsHttpMethod.ANY],
            allow_headers=[
                'Content-Type', 'X-Amz-Date', 'X-Amz-Security-Token',
                'Authorization', 'X-Api-Key', 'X-Requested-With', 'Accept',
                'Access-Control-Allow-Methods', 'Access-Control-Allow-Origin',
                'Access-Control-Allow-Headers'
            ]
        )

        self.http_api = _apigwv2.HttpApi(
            self, f"{env}-api",
            cors_preflight=cors_preflight,
        )

        authorizer = _authorizers.HttpLambdaAuthorizer(
            'custom-authorizer-cvc', custom_auth,
            response_types=[
                _authorizers.HttpLambdaResponseType.IAM
            ],
            results_cache_ttl=cdk.Duration.hours(1)
        )

        self.integration = _integration.HttpLambdaIntegration(
            "LambdaHandler", backend_handler
        )

        self.http_api.add_routes(
            path='/admin',
            authorizer=authorizer,
            integration=self.integration,
            methods=[
                _apigwv2.HttpMethod.GET,
                _apigwv2.HttpMethod.POST,
                _apigwv2.HttpMethod.PUT,
                _apigwv2.HttpMethod.DELETE,
            ]
        )

        self.http_api.add_routes(
            path='/individual',
            authorizer=authorizer,
            integration=self.integration,
            methods=[
                _apigwv2.HttpMethod.GET,
                _apigwv2.HttpMethod.POST,
                _apigwv2.HttpMethod.PUT,
                _apigwv2.HttpMethod.DELETE,
            ]
        )
