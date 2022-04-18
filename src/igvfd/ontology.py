def includeme(config):
    config.scan(__name__)
    config.registry['ontology'] = {}
