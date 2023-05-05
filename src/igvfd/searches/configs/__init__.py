from pyramid.interfaces import PHASE3_CONFIG

from snovault.interfaces import TYPES

from snovault.elasticsearch.searches.interfaces import SEARCH_CONFIG

from snosearch.interfaces import COLUMNS


def register_subtype_columns_in_abstract_search_configs(config):
    item_registry = config.registry[TYPES]
    search_config_registry = config.registry[SEARCH_CONFIG]
    for name, item in item_registry.abstract.items():
        subtypes = item.subtypes
        if len(subtypes) == 1:  # No children.
            continue
        search_config = search_config_registry.get(name)
        if search_config is None:
            raise ValueError(f'Must define search config for {name}')
        if search_config.columns:  # Manually set, skip.
            continue
        columns = {}
        for subtype in subtypes:
            subtype_search_config = search_config_registry.get(subtype)
            columns.update(subtype_search_config.columns)
        search_config.update(**{COLUMNS: columns})


def includeme(config):
    config.scan()
    config.action(
        ('register-subtype-columns-in-abstract-search-configs',),
        callable=register_subtype_columns_in_abstract_search_configs,
        args=(config,),
        order=PHASE3_CONFIG,
    )
