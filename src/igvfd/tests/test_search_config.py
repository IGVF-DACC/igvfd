import pytest
from snovault.elasticsearch.searches.interfaces import SEARCH_CONFIG
from snovault import TYPES


def test_search_config_file_set_columns(registry):
    item_registry = registry[TYPES]
    search_registry = registry[SEARCH_CONFIG]
    subtypes = item_registry.abstract['FileSet'].subtypes
    file_set_columns = search_registry.get('FileSet').columns
    subtypes_configs = search_registry.get_configs_by_names(subtypes)
    for config in subtypes_configs:
        for column in config.columns:
            assert column in file_set_columns


def test_search_config_biosample_columns(registry):
    item_registry = registry[TYPES]
    search_registry = registry[SEARCH_CONFIG]
    subtypes = item_registry.abstract['Biosample'].subtypes
    biosample_columns = search_registry.get('Biosample').columns
    subtypes_configs = search_registry.get_configs_by_names(subtypes)
    for config in subtypes_configs:
        for column in config.columns:
            assert column in biosample_columns


def test_search_config_items_columns(registry):
    item_registry = registry[TYPES]
    search_registry = registry[SEARCH_CONFIG]
    subtypes = item_registry.abstract['Item'].subtypes
    item_columns = search_registry.get('Item').columns
    subtypes_configs = search_registry.get_configs_by_names(subtypes)
    for config in subtypes_configs:
        for column in config.columns:
            assert column in item_columns


def test_search_config_sample_columns(registry):
    item_registry = registry[TYPES]
    search_registry = registry[SEARCH_CONFIG]
    subtypes = item_registry.abstract['Sample'].subtypes
    sample_columns = search_registry.get('Sample').columns
    subtypes_configs = search_registry.get_configs_by_names(subtypes)
    for config in subtypes_configs:
        for column in config.columns:
            assert column in sample_columns


def test_search_config_file_columns(registry):
    item_registry = registry[TYPES]
    search_registry = registry[SEARCH_CONFIG]
    subtypes = item_registry.abstract['File'].subtypes
    file_columns = search_registry.get('File').columns
    subtypes_configs = search_registry.get_configs_by_names(subtypes)
    for config in subtypes_configs:
        for column in config.columns:
            assert column in file_columns
