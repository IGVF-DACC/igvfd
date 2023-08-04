import json

import os

from pyramid.path import AssetResolver
from pyramid.path import caller_package

from pathlib import Path

from snovault.interfaces import COLLECTIONS


LATE = 10


def includeme(config):
    config.scan(__name__, categories=None)

    def configure_opensearch_index_names_later():
        configure_opensearch_index_names(config)

    config.action(
        'configure_opensearch_index_names',
        configure_opensearch_index_names_later,
        order=LATE
    )


def resolve_mapping_path(filename):
    return AssetResolver(
        caller_package()
    ).resolve(
        filename
    ).abspath()


def configure_opensearch_index_names(config):
    item_type_to_index_name = {}
    for collection in sorted(config.registry[COLLECTIONS].by_item_type.keys()):
        mapping_path = resolve_mapping_path(f'{collection}.json')
        with open(mapping_path, 'r') as f:
            mapping = json.load(f)
        item_type_to_index_name[mapping['item_type']] = mapping['index_name']
    config.registry['OPENSEARCH_ITEM_TYPE_TO_INDEX_NAME'] = dict(sorted(item_type_to_index_name.items()))
