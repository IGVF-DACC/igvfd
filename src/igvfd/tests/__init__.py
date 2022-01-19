def pytest_addoption(parser):
    parser.addoption(
        '--wsgi-arg',
        nargs=2,
        dest='wsgi_args',
        action='append',
        type='string'
    )
    parser.addoption(
        '--log',
        action='store',
        default='INFO',
        help='Set logging level'
    )
    parser.addoption(
        '--ini',
        action='store',
        metavar='INI_FILE'
    )
