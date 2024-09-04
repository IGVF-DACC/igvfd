import pytest
from igvfd.tests.fixtures.audit_docstring import function_with_docstring
from igvfd.commands.make_audit_docstring_json import get_docstring_dict_from_function_name


def test_get_docstring_dict_from_function_name_docstring_is_defined():
    assert get_docstring_dict_from_function_name('igvfd.tests.fixtures.audit_docstring.function_with_docstring') == {'igvfd.tests.fixtures.audit_docstring.function_with_docstring': [
        {
            'audit_description': 'audit description',
            'audit_category': 'audit category',
            'audit_level': 'ERROR'
        },
        {
            'audit_description': 'audit description 2',
            'audit_category': 'audit category 2',
            'audit_level': 'WARNING'
        }
    ]}


def test_get_docstring_dict_from_function_name_docstring_improper_keys():
    assert get_docstring_dict_from_function_name('igvfd.tests.fixtures.audit_docstring.function_with_docstring_improper_keys') == {
        'igvfd.tests.fixtures.audit_docstring.function_with_docstring_improper_keys': [
            {
                'audit_detail': 'audit description',
                'audit_category': 'audit category',
                'audit_levels': 'WARNING'
            }
        ]}


def test_get_docstring_dict_from_function_name_docstring_is_out_of_order():
    assert (get_docstring_dict_from_function_name('igvfd.tests.fixtures.audit_docstring.function_with_docstring_out_of_order')) == {
        'igvfd.tests.fixtures.audit_docstring.function_with_docstring_out_of_order': [
            {
                'audit_level': 'WARNING',
                'audit_category': 'audit category',
                'audit_description': 'audit description'
            }
        ]}


def test_get_docstring_dict_from_function_name_docstring_not_defined():
    assert get_docstring_dict_from_function_name('igvfd.tests.fixtures.audit_docstring.function_without_docstring') == {
        'igvfd.tests.fixtures.audit_docstring.function_without_docstring': {}}


def test_get_docstring_dict_from_function_name_docstring_is_not_json():
    with pytest.raises(ValueError):
        get_docstring_dict_from_function_name('igvfd.tests.fixtures.audit_docstring.function_with_non_json_docstring')
