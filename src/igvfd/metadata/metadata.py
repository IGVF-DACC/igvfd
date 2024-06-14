from collections import defaultdict
from collections import OrderedDict
from igvfd.metadata.constants import METADATA_ALLOWED_TYPES
from igvfd.metadata.constants import METADATA_COLUMN_TO_FIELDS_MAPPING
from igvfd.metadata.constants import METADATA_AUDIT_TO_AUDIT_COLUMN_MAPPING
from igvfd.metadata.csv import CSVGenerator
from igvfd.metadata.decorators import allowed_types
from igvfd.metadata.inequalities import map_param_values_to_inequalities
from igvfd.metadata.inequalities import try_to_evaluate_inequality
from igvfd.metadata.search import BatchedSearchGenerator
from igvfd.metadata.serializers import make_experiment_cell
from igvfd.metadata.serializers import make_file_cell
from igvfd.metadata.serializers import map_strings_to_booleans_and_ints
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.response import Response
from pyramid.view import view_config
from snosearch.interfaces import EXISTS
from snosearch.interfaces import MUST
from snosearch.interfaces import RANGES
from snosearch.parsers import QueryString
from snovault.util import simple_path_ids


def includeme(config):
    config.add_route('metadata', '/metadata{slash:/?}')
    config.scan(__name__)


def file_matches_file_params(file_, positive_file_param_set):
    # Expects file_param_set where FILES_PREFIX (e.g. 'files.') has been
    # stripped off of key (files.file_type -> file_type)
    # and params with field negation (i.e. file_type!=bigWig)
    # have been filtered out. Param values should be
    # coerced to ints ('2' -> 2) or booleans ('true' -> True)
    # and put into a set for comparison with file values.
    for field, set_of_param_values in positive_file_param_set.items():
        file_value = list(simple_path_ids(file_, field))
        if not file_value:
            return False
        if '*' in set_of_param_values:
            continue
        if not set_of_param_values.intersection(file_value):
            return False
    return True


def some_value_satisfies_inequalities(values, inequalities):
    return all(
        any(
            try_to_evaluate_inequality(inequality, value)
            for value in values
        )
        for inequality in inequalities
    )


def file_satisfies_inequality_constraints(file_, positive_file_inequalities):
    for field, inequalities in positive_file_inequalities.items():
        file_value = list(simple_path_ids(file_, field))
        if not file_value:
            return False
        if not some_value_satisfies_inequalities(file_value, inequalities):
            return False
    return True


def group_audits_by_files_and_type(audits):
    grouped_file_audits = defaultdict(lambda: defaultdict(list))
    grouped_other_audits = defaultdict(list)
    for audit_type, audit_column in METADATA_AUDIT_TO_AUDIT_COLUMN_MAPPING:
        for audit in audits.get(audit_type, []):
            path = audit.get('path')
            if '/files/' in path:
                grouped_file_audits[path][audit_type].append(audit.get('category'))
            else:
                grouped_other_audits[audit_type].append(audit.get('category'))
    return grouped_file_audits, grouped_other_audits


class MetadataReport:

    SEARCH_PATH = '/search/'
    EXCLUDED_COLUMNS = (
    )
    DEFAULT_PARAMS = [
        ('field', 'audit'),
        ('field', 'files.@id'),
        ('field', 'files.file_format'),
        ('field', 'files.file_format_type'),
        ('field', 'files.status'),
        ('limit', 'all'),
    ]
    CONTENT_TYPE = 'text/tsv'
    CONTENT_DISPOSITION = 'attachment; filename="metadata.tsv"'
    FILES_PREFIX = 'files.'

    def __init__(self, request):
        self.request = request
        self.query_string = QueryString(request)
        self.param_list = self.query_string.group_values_by_key()
        self.split_file_filters = {}
        self.positive_file_param_set = {}
        self.positive_file_inequalities = {}
        self.header = []
        self.experiment_column_to_fields_mapping = OrderedDict()
        self.file_column_to_fields_mapping = OrderedDict()
        self.raw_only = self.query_string.is_param('option', 'raw')
        self.csv = CSVGenerator()

    def _get_column_to_fields_mapping(self):
        return METADATA_COLUMN_TO_FIELDS_MAPPING

    def _build_header(self):
        for column in self._get_column_to_fields_mapping():
            if column not in self.EXCLUDED_COLUMNS:
                self.header.append(column)
        for audit, column in METADATA_AUDIT_TO_AUDIT_COLUMN_MAPPING:
            self.header.append(column)

    def _split_column_and_fields_by_experiment_and_file(self):
        for column, fields in self._get_column_to_fields_mapping().items():
            if fields[0].startswith(self.FILES_PREFIX):
                self.file_column_to_fields_mapping[column] = [
                    field.replace(self.FILES_PREFIX, '')
                    for field in fields
                ]
            else:
                self.experiment_column_to_fields_mapping[column] = fields

    def _set_split_file_filters(self):
        file_params = self.query_string.get_filters_by_condition(
            key_and_value_condition=lambda k, _: k.startswith(self.FILES_PREFIX)
        )
        self.split_file_filters = self.query_string.split_filters(
            params=file_params
        )

    def _set_positive_file_param_set(self):
        grouped_positive_file_params = self.query_string.group_values_by_key(
            params=self.split_file_filters[MUST] + self.split_file_filters[EXISTS]
        )
        self.positive_file_param_set = {
            k.replace(self.FILES_PREFIX, ''): set(map_strings_to_booleans_and_ints(v))
            for k, v in grouped_positive_file_params.items()
        }

    def _set_positive_file_inequalities(self):
        grouped_positive_file_inequalities = self.query_string.group_values_by_key(
            params=self.split_file_filters[RANGES]
        )
        self.positive_file_inequalities = {
            k.replace(self.FILES_PREFIX, ''): map_param_values_to_inequalities(v)
            for k, v in grouped_positive_file_inequalities.items()
        }

    def _add_positive_file_filters_as_fields_to_param_list(self):
        self.param_list['field'] = self.param_list.get('field', [])
        self.param_list['field'].extend(
            (
                k
                for k, v in self.query_string._get_original_params()
                if k.startswith(self.FILES_PREFIX) and '!' not in k
            )
        )

    def _add_fields_to_param_list(self):
        self.param_list['field'] = self.param_list.get('field', [])
        for column, fields in self._get_column_to_fields_mapping().items():
            self.param_list['field'].extend(fields)
        self._add_positive_file_filters_as_fields_to_param_list()

    def _initialize_at_id_param(self):
        self.param_list['@id'] = self.param_list.get('@id', [])

    def _get_json_elements_or_empty_list(self):
        try:
            return self.request.json.get('elements', [])
        except ValueError:
            return []

    def _maybe_add_json_elements_to_param_list(self):
        self.param_list['@id'].extend(
            self._get_json_elements_or_empty_list()
        )

    def _get_field_params(self):
        return [
            ('field', p)
            for p in self.param_list.get('field', [])
        ]

    def _get_at_id_params(self):
        return [
            ('@id', p)
            for p in self.param_list.get('@id', [])
        ]

    def _get_default_params(self):
        return self.DEFAULT_PARAMS

    def _build_query_string(self):
        self.query_string.drop('limit')
        self.query_string.drop('option')
        self.query_string.extend(
            self._get_default_params()
            + self._get_field_params()
            + self._get_at_id_params()
        )

    def _get_search_path(self):
        return self.SEARCH_PATH

    def _build_new_request(self):
        self._build_query_string()
        request = self.query_string.get_request_with_new_query_string()
        request.path_info = self._get_search_path()
        return request

    def _get_search_results_generator(self):
        return BatchedSearchGenerator(
            self._build_new_request()
        ).results()

    def _should_not_report_file(self, file_):
        conditions = [
            not file_matches_file_params(file_, self.positive_file_param_set),
            not file_satisfies_inequality_constraints(file_, self.positive_file_inequalities),
        ]
        return any(conditions)

    def _get_experiment_data(self, experiment):
        return {
            column: make_experiment_cell(fields, experiment)
            for column, fields in self.experiment_column_to_fields_mapping.items()
        }

    def _get_file_data(self, file_):
        file_['href'] = self.request.host_url + file_['href']
        return {
            column: make_file_cell(fields, file_)
            for column, fields in self.file_column_to_fields_mapping.items()
        }

    def _get_audit_data(self, grouped_audits_for_file, grouped_other_audits):
        return {
            audit_column: ', '.join(
                set(
                    grouped_audits_for_file.get(audit_type, [])
                    + grouped_other_audits.get(audit_type, [])
                )
            ) for audit_type, audit_column in METADATA_AUDIT_TO_AUDIT_COLUMN_MAPPING
        }

    def _output_sorted_row(self, experiment_data, file_data):
        row = []
        for column in self.header:
            row.append(
                file_data.get(
                    column,
                    experiment_data.get(column)
                )
            )
        return row

    def _generate_rows(self):
        yield self.csv.writerow(self.header)
        for experiment in self._get_search_results_generator():
            if not experiment.get('files', []):
                continue
            grouped_file_audits, grouped_other_audits = group_audits_by_files_and_type(
                experiment.get('audit', {})
            )
            experiment_data = self._get_experiment_data(experiment)
            for file_ in experiment.get('files', []):
                if self._should_not_report_file(file_):
                    continue
                file_data = self._get_file_data(file_)
                audit_data = self._get_audit_data(
                    grouped_file_audits.get(file_.get('@id'), {}),
                    grouped_other_audits
                )
                file_data.update(audit_data)
                yield self.csv.writerow(
                    self._output_sorted_row(experiment_data, file_data)
                )

    def _validate_request(self):
        type_params = self.param_list.get('type', [])
        if len(type_params) != 1:
            raise HTTPBadRequest(explanation='URL requires one "type" parameter.')
        return True

    def _initialize_report(self):
        self._build_header()
        self._split_column_and_fields_by_experiment_and_file()
        self._set_split_file_filters()
        self._set_positive_file_param_set()
        self._set_positive_file_inequalities()

    def _build_params(self):
        self._add_fields_to_param_list()
        self._initialize_at_id_param()
        self._maybe_add_json_elements_to_param_list()

    def generate(self):
        self._validate_request()
        self._initialize_report()
        self._build_params()
        return Response(
            content_type=self.CONTENT_TYPE,
            app_iter=self._generate_rows(),
            content_disposition=self.CONTENT_DISPOSITION,
        )


def _get_metadata(context, request):
    metadata_report = MetadataReport(request)
    return metadata_report.generate()


def metadata_report_factory(context, request):
    return _get_metadata(context, request)


@view_config(route_name='metadata', request_method=['GET', 'POST'])
@allowed_types(METADATA_ALLOWED_TYPES)
def metadata_tsv(context, request):
    return metadata_report_factory(context, request)
