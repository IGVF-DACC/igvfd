from infrastructure.naming import Config


def get_event_source_from_config(config: Config) -> str:
    return f'{config.common.project_name}.{config.name}.{config.branch}'
