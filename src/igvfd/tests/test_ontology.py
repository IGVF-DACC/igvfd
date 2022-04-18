import pytest


def test_ontology_exists_in_registry(registry):
    assert registry.get('ontology') is not None
