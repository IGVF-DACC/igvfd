import aws_cdk as cdk


config = {
    'org_name': 'IGVF',
    'project_name': 'igvfd',
    'default_branch': 'main',
    'region': 'us-west-2',
}


IGVF_DEV_US_WEST_2 = cdk.Environment(
    account='109189702753',
    region='us-west-2',
)
