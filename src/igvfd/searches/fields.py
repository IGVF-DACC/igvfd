from snosearch.fields import ResponseField
from snosearch.fields import BasicSearchResponseField

from igvfd.report import get_result_columns

from igvfd.searches.queries import BasicSearchQueryFactoryWithSort


class ResultColumnsResponseField(ResponseField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self, *args, **kwargs):
        self.parent = kwargs.get('parent')
        request = self.get_request()
        facets = self.parent.response.get('facets', [])
        columns = self.parent.response.get('columns', [])
        return {
            'result_columns': get_result_columns(request, facets, columns)
        }


class BasicSearchResponseFieldWithSort(BasicSearchResponseField):

    def _build_query(self):
        self.query_builder = BasicSearchQueryFactoryWithSort(
            params_parser=self.get_params_parser(),
            **self.kwargs
        )
        self.query = self.query_builder.build_query()
