import argparse
import logging

from pathlib import Path
from pyramid.paster import get_app

from webtest import TestApp

logging.basicConfig()
logging.getLogger('igvfd').setLevel(logging.INFO)


def reindex(app):
    environ = {
        'HTTP_ACCEPT': 'application/json',
        'REMOTE_USER': 'INDEXER',
    }
    testapp = TestApp(
        app,
        environ
    )
    testapp.post_json(
        '/_reindex',
        {},
    )


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
        'config_uri',
        help='path to configfile'
    )
    return parser


def get_args():
    return get_parser().parse_args()


def main():
    args = get_args()
    app = get_app(
        args.config_uri,
        args.app_name,
    )
    reindex(app)


if __name__ == '__main__':
    main()
