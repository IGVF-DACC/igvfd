from snovault.interfaces import COLLECTIONS


LATE = 10


def includeme(config):
    config.scan(__name__)

    def configure_opensearch_mapping_hashes_later():
        configure_opensearch_mapping_hashes(config)

    config.action(
        'configure_opensearch_mapping_hashes_later',
        configure_opensearch_mapping_hashes_later,
        order=LATE
    )


DEFAULT_HASHES = {
    'default': 'aaav1',
}


def configure_opensearch_mapping_hashes(config):
    hashes = DEFAULT_HASHES.copy()
    for collection in config.registry[COLLECTIONS].by_item_type.keys():
        hashes[collection] = hashes.get(collection, hashes.get('default'))
    del hashes['default']
    config.registry['MAPPING_HASHES'] = hashes
