import pytest


def test_ontology_exists_in_registry(registry):
    assert registry.get('ontology') is not None


def test_ontology_get_ontology_gz_json_path():
    from igvfd.ontology import get_ontology_gz_json_path
    path = get_ontology_gz_json_path()
    assert str(path) == '/igvfd/assets/ontology.json.gz'


def test_ontology_file_exists():
    from igvfd.ontology import get_ontology_gz_json_path
    path = get_ontology_gz_json_path()
    assert path.exists(), 'Ontology JSON not found'


def test_ontology_load_ontology_or_empty_dict():
    from pathlib import Path
    from igvfd.ontology import ontology_or_empty_dict
    from igvfd.ontology import get_ontology_gz_json_path
    path = Path('/igvfd/assets/badpath.json.gz')
    assert ontology_or_empty_dict(path) == {}
    path = get_ontology_gz_json_path()
    assert len(ontology_or_empty_dict(path).keys()) > 150000


def test_ontology_load_ontology():
    from igvfd.ontology import load_ontology
    data = load_ontology()
    assert len(data.keys()) > 150000
