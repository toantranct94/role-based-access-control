import aws_cdk as core
import aws_cdk.assertions as assertions

from role_based_access_control.role_based_access_control_stack import RoleBasedAccessControlStack

# example tests. To run these tests, uncomment this file along with the example
# resource in role_based_access_control/role_based_access_control_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = RoleBasedAccessControlStack(app, "role-based-access-control")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
