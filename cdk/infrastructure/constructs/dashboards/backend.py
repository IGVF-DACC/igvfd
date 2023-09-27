import aws_cdk as cdk

from constructs import Construct

from aws_cdk.aws_cloudwatch import Dashboard
from aws_cdk.aws_cloudwatch import GraphWidget
from aws_cdk.aws_cloudwatch import IWidget
from aws_cdk.aws_cloudwatch import LogQueryWidget
from aws_cdk.aws_cloudwatch import Stats
from aws_cdk.aws_cloudwatch import YAxisProps

from aws_cdk.aws_logs import LogGroup
from aws_cdk.aws_logs import ILogGroup
from aws_cdk.aws_logs import MetricFilter
from aws_cdk.aws_logs import FilterPattern

from dataclasses import dataclass

from typing import Any
from typing import List
from typing import Optional

from infrastructure.config import Config


@dataclass
class BackendDashboardProps:
    config: Config
    log_group: LogGroup


class BackendDashboard(Construct):

    props: BackendDashboardProps
    _widgets: List[IWidget]

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
        self._widgets = []
        self._define_wsgi_time_widget()
        self._define_es_time_widget()
        self._define_db_time_widget()
        self._define_response_length_widget()
        self._define_response_2xx_count_widget()
        self._define_response_4xx_count_widget()
        self._define_response_5xx_count_widget()
        self._define_dashboard()

    def _define_wsgi_time_widget(self) -> None:
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
        wsgi_time_widget = GraphWidget(
            left=[wsgi_time_metric],
            left_y_axis=YAxisProps(show_units=False),
            period=cdk.Duration.seconds(60),
        )
        self._widgets.append(wsgi_time_widget)

    def _define_es_time_widget(self) -> None:
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
        es_time_widget = GraphWidget(
            left=[es_time_metric],
            left_y_axis=YAxisProps(show_units=False),
            period=cdk.Duration.seconds(60),
        )
        self._widgets.append(es_time_widget)

    def _define_db_time_widget(self) -> None:
        db_time_metric_filter = MetricFilter(
            self,
            'DBTimeMetricFilter',
            log_group=self.props.log_group,
            metric_namespace=self.props.config.branch,
            metric_name='DB Time',
            filter_pattern=FilterPattern.all(
                FilterPattern.exists('$.db_time'),
                FilterPattern.number_value('$.db_time', '>', 0)
            ),
            metric_value='$.db_time',
        )
        db_time_metric = db_time_metric_filter.metric(
            label='DB Time microseconds',
        )
        db_time_widget = GraphWidget(
            left=[db_time_metric],
            left_y_axis=YAxisProps(show_units=False),
            period=cdk.Duration.seconds(60),
        )
        self._widgets.append(db_time_widget)

    def _define_response_length_widget(self) -> None:
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
        response_length_widget = GraphWidget(
            left=[response_length_metric],
            left_y_axis=YAxisProps(show_units=False),
            period=cdk.Duration.seconds(60),
        )
        self._widgets.append(response_length_widget)

    def _define_response_2xx_count_widget(self) -> None:
        response_2xx_count_metric_filter = MetricFilter(
            self,
            '2xxResponseCountFilter',
            log_group=self.props.log_group,
            metric_namespace=self.props.config.branch,
            metric_name='2xx Response Count',
            filter_pattern=FilterPattern.string_value('$.status', '=', '2**'),
            metric_value='1',
        )
        response_2xx_metric = response_2xx_count_metric_filter.metric(
            label='2xx Response Count',
            statistic=Stats.SUM,
        )
        response_2xx_widget = GraphWidget(
            left=[response_2xx_metric],
            left_y_axis=YAxisProps(show_units=False),
            period=cdk.Duration.seconds(60),
        )
        self._widgets.append(response_2xx_widget)

    def _define_response_4xx_count_widget(self) -> None:
        response_4xx_count_metric_filter = MetricFilter(
            self,
            '4xxResponseCountFilter',
            log_group=self.props.log_group,
            metric_namespace=self.props.config.branch,
            metric_name='4xx Response Count',
            filter_pattern=FilterPattern.string_value('$.status', '=', '4**'),
            metric_value='1',
        )
        response_4xx_metric = response_4xx_count_metric_filter.metric(
            label='4xx Response Count',
            statistic=Stats.SUM,
        )
        response_4xx_widget = GraphWidget(
            left=[response_4xx_metric],
            left_y_axis=YAxisProps(show_units=False),
            period=cdk.Duration.seconds(60),
        )
        self._widgets.append(response_4xx_widget)

    def _define_response_5xx_count_widget(self) -> None:
        response_5xx_count_metric_filter = MetricFilter(
            self,
            '5xxResponseCountFilter',
            log_group=self.props.log_group,
            metric_namespace=self.props.config.branch,
            metric_name='5xx Response Count',
            filter_pattern=FilterPattern.string_value('$.status', '=', '5**'),
            metric_value='1',
        )
        response_5xx_metric = response_5xx_count_metric_filter.metric(
            label='5xx Response Count',
            statistic=Stats.SUM,
        )
        response_5xx_widget = GraphWidget(
            left=[response_5xx_metric],
            left_y_axis=YAxisProps(show_units=False),
            period=cdk.Duration.seconds(60),
        )
        self._widgets.append(response_5xx_widget)

    def _define_dashboard(self) -> None:
        self.dashboard = Dashboard(
            self,
            'Dashboard',
            dashboard_name=f'{self.props.config.common.project_name}-{self.props.config.name}-{self.props.config.branch}-backend',
        )
        self.dashboard.add_widgets(*self._widgets)
