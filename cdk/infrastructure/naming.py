from infrastructure.config import config


def prepend_project_name(name: str) -> str:
    return f'{config["project_name"]}-{name}'


def prepend_branch_name(branch: str, name: str) -> str:
    return f'{branch}-{name}'
