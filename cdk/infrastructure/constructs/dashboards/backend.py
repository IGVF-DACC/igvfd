import aws_cdk as cdk

from constructs import Construct

from aws_cdk.aws_cloudwatch import Dashboard
from aws_cdk.aws_cloudwatch import GraphWidget
from aws_cdk.aws_cloudwatch import LogQueryWidget
from aws_cdk.aws_cloudwatch import YAxisProps

from aws_cdk.aws_logs import LogGroup
from aws_cdk.aws_logs import MetricFilter
from aws_cdk.aws_logs import FilterPattern

from dataclasses import dataclass

from typing import Any

from infrastructure.config import Config


@dataclass
class BackendDashboardProps:
    config: Config
    log_group: LogGroup


class BackendDashboard(Construct):

    props: BackendAlarmsProps

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            props: BackendDashboardProps,
            **kwargs: Any
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.props = props
        self._define_pyramid_wsgi_time_widget()
        self._define_pyramid_es_time_widget()
        self._define_pyramid_response_length_widget()
        self._define_dashboard()

    def _define_pyramid_wsgi_time_widget(self) -> None:
        wsgi_time_metric_filter = MetricFilter(
            self,
            'WsgiTimeMetricFilter',
            log_group=self.props.log_group,
            metric_namespace=self.props.config.branch,
            metric_name='WSGI Time',
            filter_pattern=FilterPattern.exists('$.wsgi_time'),
            metric_value='$.wsgi_time',
        )
        wsgi_time_metric = wsgi_time_metric_filter.metric(
            label='WSGI Time microseconds',
        )
        self._wsgi_time_widget = GraphWidget(
            left=[wsgi_time_metric],
            left_y_axis=YAxisProps(show_units=False),
            period=cdk.Duration.seconds(60),
        )

    def _define_pyramid_es_time_widget(self) -> None:
        es_time_metric_filter = MetricFilter(
            self,
            'ESTimeMetricFilter',
            log_group=self.props.log_group,
            metric_namespace=self.props.config.branch,
            metric_name='ES Time',
            filter_pattern=FilterPattern.all(
                FilterPattern.exists('$.es_time'),
                FilterPattern.number_value('$.es_time', '>', 0)
            ),
            metric_value='$.es_time',
        )
        es_time_metric = es_time_metric_filter.metric(
            label='ES Time microseconds',
        )
        self._es_time_widget = GraphWidget(
            left=[es_time_metric],
            left_y_axis=YAxisProps(show_units=False),
            period=cdk.Duration.seconds(60),
        )

    def _define_pyramid_response_length_widget(self) -> None:
        response_length_metric_filter = MetricFilter(
            self,
            'ResponseLengthMetricFilter',
            log_group=self.props.log_group,
            metric_namespace=self.props.config.branch,
            metric_name='Response Length',
            filter_pattern=FilterPattern.exists('$.response_length'),
            metric_value='$.response_length',
        )
        response_length_metric = response_length_metric_filter.metric(
            label='Response Length bytes',
        )
        self._response_length_widget = GraphWidget(
            left=[response_length_metric],
            left_y_axis=YAxisProps(show_units=False),
            period=cdk.Duration.seconds(60),
        )

    def _define_dashboard(self) -> None:
        self.dashboard = Dashboard(
            self,
            'BackendDashBoard'
        )
        self.dashboard.add_widgets(
            self._wsgi_time_widget,
            self._es_time_widget,
            self._response_length_widget,
        )
