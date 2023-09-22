import pytest
pytestmark = [pytest.mark.indexing]


def test_searches_fields_result_columns_response_field_init():
    from igvfd.searches.fields import ResultColumnsResponseField
    rrf = ResultColumnsResponseField()
    assert isinstance(rrf, ResultColumnsResponseField)


def test_searches_fields_result_columns_response_field_query(workbook, testapp):
    r = testapp.get(
        '/multireport/?institute_label=Stanford'
    )
    assert 'result_columns' in r.json
    assert len(r.json['result_columns']) < len(r.json['columns'])
