import pytest


def test_naming_prepend_project_name():
    from infrastructure.naming import prepend_project_name
    assert prepend_project_name(
        'some-other-name'
    ) == 'igvfd-some-other-name'


def test_naming_prepend_branch_name():
    from infrastructure.naming import prepend_branch_name
    assert prepend_branch_name(
        'some-branch',
        'some-name'
    ) == 'some-branch-some-name'
