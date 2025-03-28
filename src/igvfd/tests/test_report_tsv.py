import pytest
from igvfd.report import lookup_column_value
from igvfd.report import format_row
from igvfd.report import _convert_camel_to_snake
from igvfd.report import get_host_type


def test_format_row():
    columns = ['col1', 'col2', 'col3']
    expected = b'col1\tcol2\tcol3\r\n'
    target = format_row(columns)
    assert expected == target


def test_convert_camel_to_snake_with_two_words():
    expected = 'camel_case'
    target = _convert_camel_to_snake('CamelCase')
    assert expected == target


def test_convert_camel_to_snake_with_one_words():
    expected = 'camel'
    target = _convert_camel_to_snake('Camel')
    assert expected == target


def test_batch_download_lookup_column_value(lookup_column_value_item, lookup_column_value_validate):
    for path in lookup_column_value_validate.keys():
        assert lookup_column_value_validate[path] == lookup_column_value(lookup_column_value_item, path)


def test_get_host_type():
    assert 'localhost' == get_host_type('localhost:8000')
    assert 'data' == get_host_type('api.data.igvf.org')
    assert 'sandbox' == get_host_type('api.sandbox.igvf.org')
    assert 'staging' == get_host_type('api.staging.igvf.org')
    assert 'igvfd-dev' == get_host_type('igvfd-dev.demo.igvf.org')
    assert 'igvfd-igvf-2320-improve-sample-summary' == get_host_type(
        'igvfd-igvf-2320-improve-sample-summary.demo.igvf.org')
