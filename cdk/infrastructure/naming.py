from infrastructure.config import config


def prepend_project_name(name):
    return f'{config["project_name"]}-{name}'


def prepend_branch_name(branch, name):
    return f'{branch}-{name}'
