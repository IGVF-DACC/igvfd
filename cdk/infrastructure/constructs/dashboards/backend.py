import aws_cdk as cdk

from constructs import Construct

from aws_cdk.aws_cloudwatch import Dashboard
from aws_cdk.aws_cloudwatch import GraphWidget
from aws_cdk.aws_cloudwatch import IMetric
from aws_cdk.aws_cloudwatch import IWidget
from aws_cdk.aws_cloudwatch import Stats
from aws_cdk.aws_cloudwatch import Unit
from aws_cdk.aws_cloudwatch import YAxisProps

from aws_cdk.aws_logs import LogGroup
from aws_cdk.aws_logs import MetricFilter
from aws_cdk.aws_logs import FilterPattern

from dataclasses import dataclass

from typing import Any
from typing import List

from infrastructure.config import Config

ITEM_TYPES = [
    'access_key',
    'alignment_file',
    'analysis_set',
    'analysis_step',
    'analysis_step_version',
    'assay_term',
    'auxiliary_set',
    'award',
    'biomarker',
    'configuration_file',
    'construct_library_set',
    'crispr_modification',
    'curated_set',
    'degron_modification',
    'document',
    'gene',
    'genome_browser_annotation_file',
    'human_donor',
    'image',
    'image_file',
    'in_vitro_system',
    'index_file',
    'institutional_certificate',
    'lab',
    'matrix_file',
    'measurement_set',
    'model_file',
    'model_set',
    'mpra_quality_metric',
    'multiplexed_sample',
    'open_reading_frame',
    'page',
    'perturb_seq_quality_metric',
    'phenotype_term',
    'phenotypic_feature',
    'platform_term',
    'prediction_set',
    'primary_cell',
    'publication',
    'reference_file',
    'rodent_donor',
    'sample_term',
    'sequence_file',
    'signal_file',
    'single_cell_atac_seq_quality_metric',
    'single_cell_rna_seq_quality_metric',
    'software',
    'software_version',
    'source',
    'starr_seq_quality_metric',
    'tabular_file',
    'technical_sample',
    'tissue',
    'treatment',
    'user',
    'whole_organism',
    'workflow',
]


@dataclass
class BackendDashboardProps:
    config: Config
    log_group: LogGroup


class BackendDashboard(Construct):

    props: BackendDashboardProps
    _widgets: List[IWidget]
    _item_type_indexing_metrics: List[IMetric]

    ITEM_TYPES: List[str] = [
        'access_key',
        'alignment_file',
        'analysis_set',
        'analysis_step',
        'analysis_step_version',
        'assay_term',
        'auxiliary_set',
        'award',
        'biomarker',
        'configuration_file',
        'construct_library_set',
        'crispr_modification',
        'curated_set',
        'degron_modification',
        'document',
        'gene',
        'genome_browser_annotation_file',
        'human_donor',
        'image',
        'image_file',
        'in_vitro_system',
        'index_file',
        'institutional_certificate',
        'lab',
        'matrix_file',
        'measurement_set',
        'model_file',
        'model_set',
        'mpra_quality_metric',
        'multiplexed_sample',
        'open_reading_frame',
        'page',
        'perturb_seq_quality_metric',
        'phenotype_term',
        'phenotypic_feature',
        'platform_term',
        'prediction_set',
        'primary_cell',
        'publication',
        'reference_file',
        'rodent_donor',
        'sample_term',
        'sequence_file',
        'signal_file',
        'single_cell_atac_seq_quality_metric',
        'single_cell_rna_seq_quality_metric',
        'software',
        'software_version',
        'source',
        'starr_seq_quality_metric',
        'tabular_file',
        'technical_sample',
        'tissue',
        'treatment',
        'user',
        'whole_organism',
        'workflow',
    ]

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
        self._item_type_indexing_metrics = []
        self._define_wsgi_time_widget()
        self._define_es_time_widget()
        self._define_db_time_widget()
        self._define_response_length_widget()
        self._define_response_2xx_count_widget()
        self._define_response_4xx_count_widget()
        self._define_response_5xx_count_widget()
        self._define_item_type_indexing_metrics()
        self._define_item_type_indexing_widget()
        self._define_dashboard()

    def _define_item_type_indexing_metric(self, item_type: str) -> IMetric:
        item_type_camel_case = ''.join(word.capitalize() for word in item_type.split('_'))
        item_type_indexing_metric_filter = MetricFilter(
            self,
            f'{item_type}IndexingMetricFilter',
            log_group=self.props.log_group,
            metric_namespace=self.props.config.branch,
            metric_name=f'{item_type_camel_case}Indexing',
            filter_pattern=FilterPattern.all(
                FilterPattern.string_value(json_field='$.statusline', comparison='=', value='*@@index-data-external*'),
                FilterPattern.string_value(json_field='$.item_type', comparison='=', value=item_type)
            ),
            metric_value='$.wsgi_time'
        )
        item_type_indexing_metric = item_type_indexing_metric_filter.metric(
            label=f'{item_type_camel_case} Indexing Time Microseconds',
            unit=Unit.MICROSECONDS
        )
        return item_type_indexing_metric

    def _define_item_type_indexing_metrics(self) -> None:
        for item_type in self.ITEM_TYPES:
            self._item_type_indexing_metrics.append(self._define_item_type_indexing_metric(item_type))

    def _define_item_type_indexing_widget(self) -> None:
        item_type_indexing_widget = GraphWidget(
            left=self._item_type_indexing_metrics,
            left_y_axis=YAxisProps(show_units=False),
            period=cdk.Duration.seconds(60),
            title='Per Item Type Indexing Time Microseconds',
        )
        self._widgets.append(item_type_indexing_widget)

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
