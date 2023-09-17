#!/usr/bin/env python3

import aws_cdk as cdk

from role_based_access_control.role_based_access_control_stack import \
    RoleBasedAccessControlStack

app = cdk.App()
RoleBasedAccessControlStack(
    app, "RoleBasedAccessControlStack",
    props={
        'env': 'dev',
    }
)

app.synth()
