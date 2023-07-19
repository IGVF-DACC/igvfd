import pytest
from igvfd.tests.fixtures.audit_docstring import function_with_docstring
from igvfd.commands.make_audit_docstring_json import get_docstring_dict_from_function_name


def test_get_docstring_dict_from_function_name_docstring_is_defined():
    assert get_docstring_dict_from_function_name('igvfd.tests.fixtures.audit_docstring.function_with_docstring') == {'igvfd.tests.fixtures.audit_docstring.function_with_docstring': {
        'audit_detail': 'This detail: has colons: and : multiple lines', 'audit_category': 'audit category', 'audit_levels': ['ERROR', 'WARNING']}}


def test_get_docstring_dict_from_function_name_docstring_improper_keys():
    assert get_docstring_dict_from_function_name('igvfd.tests.fixtures.audit_docstring.function_with_docstring_improper_keys') == {
        'igvfd.tests.fixtures.audit_docstring.function_with_docstring_improper_keys': {'audit_detail': '', 'audit_category': '', 'audit_levels': []}}


def test_get_docstring_dict_from_function_name_docstring_not_defined():
    assert get_docstring_dict_from_function_name('igvfd.tests.fixtures.audit_docstring.function_without_docstring') == {
        'igvfd.tests.fixtures.audit_docstring.function_without_docstring': {}}
