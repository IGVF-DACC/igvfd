import pytest
from igvfd.tests.fixtures.audit_docstring import function_with_docstring
from igvfd.commands.make_audit_docstring_json import get_docstring_dict_from_function_name


def test_get_docstring_dict_from_function_name_docstring_is_defined():
    assert get_docstring_dict_from_function_name('igvfd.tests.fixtures.audit_docstring.function_with_docstring') == {
        'igvfd.tests.fixtures.audit_docstring.function_with_docstring': 'foo'}


def test_get_docstring_dict_from_function_name_docstring_not_defined():
    assert get_docstring_dict_from_function_name('igvfd.tests.fixtures.audit_docstring.function_without_docstring') == {
        'igvfd.tests.fixtures.audit_docstring.function_without_docstring': ''}
