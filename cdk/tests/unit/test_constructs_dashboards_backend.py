
import json
import pytest
from aws_cdk.assertions import Template


def test_constructs_dashboards_backend_initialize_backend_dashboard(stack, config, snapshot):
    from aws_cdk.aws_logs import LogGroup
    from infrastructure.constructs.dashboards.backend import BackendDashboard
    from infrastructure.constructs.dashboards.backend import BackendDashboardProps

    log_group = LogGroup(stack, 'TestLogGroup')
    dashboard = BackendDashboard(
        stack,
        'TestDashboard',
        props=BackendDashboardProps(
            config=config,
            log_group=log_group
        )
    )
    template = Template.from_stack(stack)
    template_json = template.to_json()
    snapshot.assert_match(
        json.dumps(
            template_json,
            indent=4,
            sort_keys=True
        ),
        'backend_dashboard_template.json'
    )
