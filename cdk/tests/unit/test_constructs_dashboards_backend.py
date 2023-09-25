import pytest

from aws_cdk.assertions import Template


def test_constructs_dashboards_backend_initialize_backend_dashboard(stack, config):
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
    template.has_resource_properties(
        'AWS::Logs::MetricFilter',
        {
            'FilterPattern': "{ $.status = \"2**\" }",
            'LogGroupName': {
                'Ref': 'TestLogGroup4EEF7AD4'
            },
            'MetricTransformations': [
                {
                    'MetricName': '2xx Response Count',
                    'MetricNamespace': 'some-branch',
                    'MetricValue': '1'
                }
            ]
        }
    )
    template.has_resource_properties(
        'AWS::Logs::MetricFilter',
        {
            'FilterPattern': "{ $.status = \"4**\" }",
            'LogGroupName': {
                'Ref': 'TestLogGroup4EEF7AD4'
            },
            'MetricTransformations': [
                {
                    'MetricName': '4xx Response Count',
                    'MetricNamespace': 'some-branch',
                    'MetricValue': '1'
                }
            ]
        }
    )
    """
    template.has_resource_properties(
            'AWS::Logs::MetricFilter',
            {
                'FilterPattern': "{ $.status = \"5**\" }",
                'LogGroupName': {
                    'Ref': 'TestLogGroup4EEF7AD4'
                },
                'MetricTransformations': [
                    {
                        'MetricName': '5xx Response Count',
                        'MetricNamespace': 'some-branch',
                        'MetricValue': '1'
                    }
                ]
            }
        )

        template.has_resource_properties(
            'AWS::CloudWatch::Dashboard',
            {
                'DashboardBody':
                {
                    'Fn::Join': [
                        '',
                        [
                            "{\"widgets\":[{\"type\":\"metric\",\"width\":6,\"height\":6,\"x\":0,\"y\":0,\"properties\":{\"view\":\"timeSeries\",\"region\":\"",
                            {
                                'Ref': 'AWS::Region'
                            },
                            "\",\"metrics\":[[\"some-branch\",\"WSGI Time\",{\"label\":\"WSGI Time microseconds\"}]],\"yAxis\":{\"left\":{\"showUnits\":false}},\"period\":60}},{\"type\":\"metric\",\"width\":6,\"height\":6,\"x\":6,\"y\":0,\"properties\":{\"view\":\"timeSeries\",\"region\":\"",
                            {
                                'Ref': 'AWS::Region'
                            },
                            "\",\"metrics\":[[\"some-branch\",\"ES Time\",{\"label\":\"ES Time microseconds\"}]],\"yAxis\":{\"left\":{\"showUnits\":false}},\"period\":60}},{\"type\":\"metric\",\"width\":6,\"height\":6,\"x\":12,\"y\":0,\"properties\":{\"view\":\"timeSeries\",\"region\":\"",
                            {
                                'Ref': 'AWS::Region'
                            },
                            "\",\"metrics\":[[\"some-branch\",\"DB Time\",{\"label\":\"DB Time microseconds\"}]],\"yAxis\":{\"left\":{\"showUnits\":false}},\"period\":60}},{\"type\":\"metric\",\"width\":6,\"height\":6,\"x\":18,\"y\":0,\"properties\":{\"view\":\"timeSeries\",\"region\":\"",
                            {
                                'Ref': 'AWS::Region'
                            },
                            "\",\"metrics\":[[\"some-branch\",\"Response Length\",{\"label\":\"Response Length bytes\"}]],\"yAxis\":{\"left\":{\"showUnits\":false}},\"period\":60}},{\"type\":\"metric\",\"width\":6,\"height\":6,\"x\":0,\"y\":6,\"properties\":{\"view\":\"timeSeries\",\"region\":\"",
                            {
                                'Ref': 'AWS::Region'
                            },
                            "\",\"metrics\":[[\"some-branch\",\"2xx Response Count\",{\"label\":\"2xx Response Count\",\"stat\":\"Sum\"}]],\"yAxis\":{\"left\":{\"showUnits\":false}},\"period\":60}},{\"type\":\"metric\",\"width\":6,\"height\":6,\"x\":6,\"y\":6,\"properties\":{\"view\":\"timeSeries\",\"region\":\"",
                            {
                                'Ref': 'AWS::Region'
                            },
                            "\",\"metrics\":[[\"some-branch\",\"4xx Response Count\",{\"label\":\"4xx Response Count\",\"stat\":\"Sum\"}]],\"yAxis\":{\"left\":{\"showUnits\":false}},\"period\":60}},{\"type\":\"metric\",\"width\":6,\"height\":6,\"x\":12,\"y\":6,\"properties\":{\"view\":\"timeSeries\",\"region\":\"",
                            {
                                'Ref': 'AWS::Region'
                            },
                            "\",\"metrics\":[[\"some-branch\",\"5xx Response Count\",{\"label\":\"5xx Response Count\",\"stat\":\"Sum\"}]],\"yAxis\":{\"left\":{\"showUnits\":false}},\"period\":60}}]}"
                        ]
                    ]
                }
            }
        )
    """
    template.has_resource_properties(
        'AWS::Logs::MetricFilter',
        {
            'FilterPattern': "{ ($.es_time = \"*\") && ($.es_time > 0) }",
            'LogGroupName': {
                'Ref': 'TestLogGroup4EEF7AD4'
            },
            'MetricTransformations': [
                {
                    'MetricName': 'ES Time',
                    'MetricNamespace': 'some-branch',
                    'MetricValue': '$.es_time'
                }
            ]
        }
    )
    template.has_resource_properties(
        'AWS::Logs::MetricFilter',
        {
            'FilterPattern': "{ $.response_length = \"*\" }",
            'LogGroupName': {
                'Ref': 'TestLogGroup4EEF7AD4'
            },
            'MetricTransformations': [
                {
                    'MetricName': 'Response Length',
                    'MetricNamespace': 'some-branch',
                    'MetricValue': '$.response_length'
                }
            ]
        }
    )
    template.has_resource_properties(
        'AWS::Logs::MetricFilter',
        {
            'FilterPattern': "{ $.wsgi_time = \"*\" }",
            'LogGroupName': {
                'Ref': 'TestLogGroup4EEF7AD4'
            },
            'MetricTransformations': [
                {
                    'MetricName': 'WSGI Time',
                    'MetricNamespace': 'some-branch',
                    'MetricValue': '$.wsgi_time'
                }
            ]
        }
    )
    template.has_resource_properties(
        'AWS::Logs::MetricFilter',
        {
            'FilterPattern': "{ ($.db_time = \"*\") && ($.db_time > 0) }",
            'LogGroupName': {
                'Ref': 'TestLogGroup4EEF7AD4'
            },
            'MetricTransformations': [
                {
                    'MetricName': 'DB Time',
                    'MetricNamespace': 'some-branch',
                    'MetricValue': '$.db_time'
                }
            ]
        }
    )
    template.has_resource_properties(
        'AWS::Logs::LogGroup',
        {
            'RetentionInDays': 731
        }
    )
    """
        template.resource_count_is(
            'AWS::Logs::MetricFilter',
            7
        )
    """
