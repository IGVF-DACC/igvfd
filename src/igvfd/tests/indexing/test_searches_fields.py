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
    assert '@id' in r.json['result_columns']
    assert 'uuid' in r.json['result_columns']
    assert 'title' in r.json['result_columns']
    assert 'aliases' in r.json['result_columns']
    assert 'awards' in r.json['result_columns']
    assert 'name' in r.json['result_columns']
    assert 'status' in r.json['result_columns']
    assert 'pi' in r.json['result_columns']
    assert 'institute_label' in r.json['result_columns']


def test_searches_fields_result_columns_response_field_config_field_in_query(workbook, testapp):
    r = testapp.get(
        '/multireport/?type=InVitroSystem&config=Tissue&field=%40id&field=age'
    )
    assert 'result_columns' in r.json
    assert len(r.json['result_columns']) < len(r.json['columns'])
    assert '@id' in r.json['result_columns']
    assert 'age' in r.json['result_columns']
