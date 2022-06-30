import argparse
import logging

from pathlib import Path
from pkg_resources import resource_filename
from pyramid.paster import get_app

from igvfd.loadxl import load_all


logging.basicConfig()
logging.getLogger('igvfd').setLevel(logging.INFO)


def get_parser():
    parser = argparse.ArgumentParser(
        description='Load data',
    )
    parser.add_argument(
        '--app-name',
        default='app',
        help='Pyramid app name in config file',
    )
    parser.add_argument(
        '--config_uri',
        default=f'{Path().absolute()}/config/pyramid/ini/loader.ini',
        help='Path to config file',
    )
    parser.add_argument(
        '--load',
        action='store_true',
        help='Load test set'
    )
    return parser


def get_args():
    return get_parser().parse_args()


def load_alpha(app):
    from webtest import TestApp
    environ = {
        'HTTP_ACCEPT': 'application/json',
        'REMOTE_USER': 'IMPORT',
    }
    testapp = TestApp(app, environ)
    inserts = resource_filename('igvfd', 'commands/assets/alpha/inserts/')
    docsdir = [resource_filename('igvfd', 'commands/assets/alpha/documents/')]
    load_all(testapp, inserts, docsdir)


def main():
    args = get_args()
    app = get_app(
        args.config_uri,
        args.app_name,
    )
    load_alpha(app)


if __name__ == '__main__':
    main()
