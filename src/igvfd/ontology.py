import gzip
import json

from pathlib import Path


def includeme(config):
    config.scan(__name__)
    config.registry['ontology'] = load_ontology()


def load_local_gz_json(path):
    with gzip.open(path, 'rt', encoding='utf-8') as local_file:
        data = json.load(local_file)
    return data


def get_ontology_gz_json_path():
    return Path(__file__).resolve().parents[2] / 'assets' / 'ontology.json.gz'


def ontology_or_empty_dict(path):
    if path.exists():
        return load_local_gz_json(path)
    return {}


def load_ontology():
    path = get_ontology_gz_json_path()
    return ontology_or_empty_dict(path)
