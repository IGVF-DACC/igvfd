__version__ = '21.1.0'


import igvfd.schema_formats  # needed to import before snovault to add FormatCheckers
import base64
import codecs
import copy
import json
import os
import subprocess

from pathlib import Path
from pyramid.config import Configurator
from pyramid.path import (
    AssetResolver,
    caller_package,
)
from pyramid.session import SignedCookieSessionFactory
from pyramid.settings import (
    aslist,
    asbool,
)
from sqlalchemy import engine_from_config
from webob.cookies import JSONSerializer
from snovault.json_renderer import json_renderer


STATIC_MAX_AGE = 0


def json_asset(spec, **kw):
    utf8 = codecs.getreader('utf-8')
    asset = AssetResolver(caller_package()).resolve(spec)
    return json.load(utf8(asset.stream()), **kw)


def static_resources(config):
    from pkg_resources import resource_filename
    import mimetypes
    mimetypes.init()
    mimetypes.init([resource_filename('igvfd', 'static/mime.types')])
    config.add_static_view('static', 'static', cache_max_age=STATIC_MAX_AGE)
    config.add_static_view('profiles', 'schemas', cache_max_age=STATIC_MAX_AGE)

    favicon_path = '/static/img/favicon.ico'
    if config.route_prefix:
        favicon_path = '/%s%s' % (config.route_prefix, favicon_path)

    config.add_route('favicon.ico', 'favicon.ico')

    def favicon(request):
        subreq = request.copy()
        subreq.path_info = favicon_path
        response = request.invoke_subrequest(subreq)
        return response

    config.add_view(favicon, route_name='favicon.ico')


def changelogs(config):
    config.add_static_view(
        'profiles/changelogs',
        'schemas/changelogs',
        cache_max_age=STATIC_MAX_AGE
    )


def configure_engine(settings):
    settings = copy.deepcopy(settings)
    engine_url = os.environ.get('SQLALCHEMY_URL') or settings['sqlalchemy.url']
    settings['sqlalchemy.url'] = engine_url
    engine_opts = {}
    if engine_url.startswith('postgresql'):
        application_name = 'app'
        engine_opts = dict(
            isolation_level='REPEATABLE READ',
            json_serializer=json_renderer.dumps,
            connect_args={'application_name': application_name}
        )
    engine = engine_from_config(settings, 'sqlalchemy.', **engine_opts)
    if engine.url.drivername == 'postgresql':
        timeout = settings.get('postgresql.statement_timeout')
        if timeout:
            timeout = int(timeout) * 1000
            set_postgresql_statement_timeout(engine, timeout)
    return engine


def set_postgresql_statement_timeout(engine, timeout=20 * 1000):
    """ Prevent Postgres waiting indefinitely for a lock.
    """
    from sqlalchemy import event
    import psycopg2

    @event.listens_for(engine, 'connect')
    def connect(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        try:
            cursor.execute('SET statement_timeout TO %d' % timeout)
        except psycopg2.Error:
            dbapi_connection.rollback()
        finally:
            cursor.close()
            dbapi_connection.commit()


def configure_dbsession(config):
    from snovault import DBSESSION
    settings = config.registry.settings
    DBSession = settings.pop(DBSESSION, None)
    if DBSession is None:
        engine = configure_engine(settings)

        if asbool(settings.get('create_tables', False)):
            from snovault.storage import Base
            Base.metadata.create_all(engine)

        import snovault.storage
        import zope.sqlalchemy
        from sqlalchemy import orm

        DBSession = orm.scoped_session(orm.sessionmaker(bind=engine))
        zope.sqlalchemy.register(DBSession)
        snovault.storage.register(DBSession)

    config.registry[DBSESSION] = DBSession


def load_workbook(app, workbook_filename, docsdir, test=False):
    from .loadxl import load_all
    from webtest import TestApp
    environ = {
        'HTTP_ACCEPT': 'application/json',
        'REMOTE_USER': 'IMPORT',
    }
    testapp = TestApp(app, environ)
    load_all(testapp, workbook_filename, docsdir, test=test)


def json_from_path(path, default=None):
    if path is None:
        return default
    return json.load(open(path))


def configure_sqs_client(config):
    from snovault.app import configure_sqs_client
    configure_sqs_client(config)


def configure_transaction_queue(config):
    from snovault.app import configure_transaction_queue
    configure_transaction_queue(config)


def configure_invalidation_queue(config):
    from snovault.app import configure_invalidation_queue
    configure_invalidation_queue(config)


def session(config):
    """ To create a session secret on the server:
    $ cat /dev/urandom | head -c 256 | base64 > session-secret.b64
    """
    from igvfd.cookie import add_session_cookie_name_to_settings
    settings = config.registry.settings
    if 'session.secret' in settings:
        secret = settings['session.secret'].strip()
        if secret.startswith('/'):
            secret = open(secret).read()
            secret = base64.b64decode(secret)
    else:
        secret = os.environ.get('SESSION_SECRET') or os.urandom(256)
    # auth_tkt has no timeout set
    # cookie will still expire at browser close
    if 'session.timeout' in settings:
        timeout = int(settings['session.timeout'])
    else:
        timeout = 60 * 60 * 24
    add_session_cookie_name_to_settings(settings, secret)
    session_factory = SignedCookieSessionFactory(
        cookie_name=settings['session_cookie_name'],
        secret=secret,
        timeout=timeout,
        reissue_time=2**32,  # None does not work
        serializer=JSONSerializer(),
        domain=settings.get('session_cookie_domain', None)
    )
    config.set_session_factory(session_factory)


def app_version(config):
    config.registry.settings['snovault.app_version'] = __version__


def main(global_config, **local_config):
    """ This function returns a Pyramid WSGI application.
    """
    settings = global_config
    settings.update(local_config)

    settings['snovault.jsonld.namespaces'] = json_asset('igvfd:schemas/namespaces.json')
    settings['snovault.jsonld.terms_namespace'] = 'https://api.data.igvf.org/terms/'
    settings['snovault.jsonld.terms_prefix'] = 'igvf'

    # Before settings are passed to Configurator.
    OPENSEARCH_URL = os.environ.get('OPENSEARCH_URL')
    if OPENSEARCH_URL:
        settings['elasticsearch.server'] = OPENSEARCH_URL

    config = Configurator(settings=settings)
    config.include(app_version)

    config.include('pyramid_multiauth')  # must be before calling set_authorization_policy
    from pyramid_localroles import LocalRolesAuthorizationPolicy
    # Override default authz policy set by pyramid_multiauth
    config.set_authorization_policy(LocalRolesAuthorizationPolicy())
    config.include(session)
    # Must go before other route registration.
    config.include('.cors')
    config.include('.auth0')
    config.include('.cookie')

    config.include(configure_dbsession)
    config.include(configure_sqs_client)
    config.include(configure_transaction_queue)
    config.include(configure_invalidation_queue)
    config.include('snovault')
    config.commit()  # commit so search can override listing

    # Render an HTML page to browsers and a JSON document for API clients
    config.include('.renderers')
    config.include('.authentication')
    config.include('.server_defaults')
    config.include('.types')
    config.include('.searches.configs')
    config.include('.root')

    config.include('.ontology')
    config.include('.report')
    config.include('.verify_email')

    if 'elasticsearch.server' in config.registry.settings:
        config.include('snovault.elasticsearch')
        config.include('igvfd.search_views')

    config.include(static_resources)
    config.include(changelogs)

    config.include('.upgrade')
    config.include('.audit')

    if asbool(settings.get('testing', False)):
        config.include('.tests.testing_views')

    config.include('igvfd.mappings.register')
    config.include('igvfd.feature_flags')

    app = config.make_wsgi_app()

    return app
