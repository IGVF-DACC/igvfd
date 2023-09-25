from snosearch.fields import ResponseField
from igvfd.report import get_result_columns


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
