from snovault.feature_flags import register_feature_flags


# These are only for testing on local demos.
# Change feature flags in infrastructure config
# for deployed demos.
LOCAL_FEATURE_FLAGS = {
    'block_database_writes': {
        'enabled': False
    },
    'is_igvfd': {
        'enabled': True
    }
}


def includeme(config):
    register_feature_flags(config, LOCAL_FEATURE_FLAGS)
    config.scan(__name__, categories=None)
