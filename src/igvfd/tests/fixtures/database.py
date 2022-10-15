import pytest


@pytest.fixture(scope='session')
def engine_url(request, ini_file):
    print('Use Docker Postgres')
    yield ini_file.get('sqlalchemy.url')


# http://docs.sqlalchemy.org/en/rel_0_8/orm/session.html#joining-a-session-into-an-external-transaction
# By binding the SQLAlchemy Session to an external transaction multiple testapp
# requests can be rolled back at the end of the test.
@pytest.fixture(scope='session')
def conn(engine_url):
    from snovault.app import configure_engine
    from snovault.storage import Base
    engine_settings = {
        'sqlalchemy.url': engine_url,
    }
    engine = configure_engine(engine_settings)
    conn = engine.connect()
    tx = conn.begin()
    try:
        Base.metadata.create_all(bind=conn)
        yield conn
    finally:
        tx.rollback()
        conn.close()
        engine.dispose()


@pytest.fixture(scope='session')
def _DBSession(conn):
    import snovault.storage
    import zope.sqlalchemy
    from sqlalchemy import orm
    # ``server`` thread must be in same scope
    DBSession = orm.scoped_session(orm.sessionmaker(bind=conn), scopefunc=lambda: 0)
    zope.sqlalchemy.register(DBSession)
    snovault.storage.register(DBSession)
    return DBSession


@pytest.fixture(scope='session')
def DBSession(_DBSession, zsa_savepoints, check_constraints):
    return _DBSession


@pytest.fixture
def external_tx(request, conn):
    tx = conn.begin_nested()
    yield tx
    tx.rollback()


@pytest.fixture
def transaction(request, external_tx, zsa_savepoints, check_constraints):
    import transaction
    transaction.begin()
    request.addfinalizer(transaction.abort)
    return transaction


@pytest.fixture(scope='session')
def zsa_savepoints(conn):
    """ Place a savepoint at the start of the zope transaction
    This means failed requests rollback to the db state when they began rather
    than that at the start of the test.
    """
    from transaction.interfaces import ISynchronizer
    from zope.interface import implementer

    @implementer(ISynchronizer)
    class Savepoints(object):
        def __init__(self, conn):
            self.conn = conn
            self.sp = None
            self.state = None

        def beforeCompletion(self, transaction):
            pass

        def afterCompletion(self, transaction):
            # txn be aborted a second time in manager.begin()
            if self.sp is None:
                return
            if self.state == 'commit':
                self.state = 'completion'
                self.sp.commit()
            else:
                self.state = 'abort'
                self.sp.rollback()
            self.sp = None
            self.state = 'done'

        def newTransaction(self, transaction):
            self.state = 'new'
            self.sp = self.conn.begin_nested()
            self.state = 'begun'
            transaction.addBeforeCommitHook(self._registerCommit)

        def _registerCommit(self):
            self.state = 'commit'

    zsa_savepoints = Savepoints(conn)

    import transaction
    transaction.manager.registerSynch(zsa_savepoints)

    yield zsa_savepoints
    transaction.manager.unregisterSynch(zsa_savepoints)


@pytest.fixture
def session(transaction, DBSession):
    """ Returns a setup session
    Depends on transaction as storage relies on some interaction there.
    """
    return DBSession()


@pytest.fixture(scope='session')
def check_constraints(conn, _DBSession):
    '''Check deffered constraints on zope transaction commit.
    Deferred foreign key constraints are only checked at the outer transaction
    boundary, not at a savepoint. With the Pyramid transaction bound to a
    subtransaction check them manually.
    '''
    from transaction.interfaces import ISynchronizer
    from zope.interface import implementer

    @implementer(ISynchronizer)
    class CheckConstraints(object):
        def __init__(self, conn):
            self.conn = conn
            self.state = None

        def beforeCompletion(self, transaction):
            pass

        def afterCompletion(self, transaction):
            pass

        def newTransaction(self, transaction):

            @transaction.addBeforeCommitHook
            def set_constraints():
                self.state = 'checking'
                session = _DBSession()
                session.flush()
                sp = self.conn.begin_nested()
                try:
                    self.conn.execute('SET CONSTRAINTS ALL IMMEDIATE')
                except:
                    sp.rollback()
                    raise
                else:
                    self.conn.execute('SET CONSTRAINTS ALL DEFERRED')
                finally:
                    sp.commit()
                    self.state = None

    check_constraints = CheckConstraints(conn)

    import transaction
    transaction.manager.registerSynch(check_constraints)

    yield check_constraints

    transaction.manager.unregisterSynch(check_constraints)


@pytest.fixture
def execute_counter(conn, zsa_savepoints, check_constraints):
    """ Count calls to execute
    """
    from contextlib import contextmanager
    from sqlalchemy import event

    class Counter(object):
        def __init__(self):
            self.reset()
            self.conn = conn

        def reset(self):
            self.count = 0

        @contextmanager
        def expect(self, count):
            start = self.count
            yield
            difference = self.count - start
            assert difference == count

    counter = Counter()

    @event.listens_for(conn, 'after_cursor_execute')
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        # Ignore the testing savepoints
        if zsa_savepoints.state != 'begun' or check_constraints.state == 'checking':
            return
        counter.count += 1

    yield counter

    event.remove(conn, 'after_cursor_execute', after_cursor_execute)


@pytest.fixture
def no_deps(conn, DBSession):
    from sqlalchemy import event

    session = DBSession()

    @event.listens_for(session, 'after_flush')
    def check_dependencies(session, flush_context):
        assert not flush_context.cycles

    @event.listens_for(conn, 'before_execute', retval=True)
    def before_execute(conn, clauseelement, multiparams, params):
        return clauseelement, multiparams, params

    yield

    event.remove(session, 'before_flush', check_dependencies)


@pytest.fixture(scope='session')
def wsgi_server_host_port(request):
    wsgi_args = dict(request.config.option.wsgi_args or ())
    if ('port_range.min' in wsgi_args and 'port_range.max' in wsgi_args):
        import socket
        import os
        # return available port in specified range if min and max are defined
        port_temp, port_max = int(wsgi_args['port_range.min']), int(wsgi_args['port_range.max'])
        port_assigned = False
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while not port_assigned and port_temp <= port_max:
            try:
                s.bind(('', port_temp))
                port_assigned = True
            except OSError:
                port_temp += 1
        if not port_assigned:
            # port failed to be assigned, so raise an error
            raise
        ip, port = s.getsockname()
        s.close()
        ip = os.environ.get('WEBTEST_SERVER_BIND', '127.0.0.1')
        return ip, port
    else:
        # otherwise get any free port
        from webtest.http import get_free_port
        return get_free_port()


@pytest.fixture(scope='session')
def wsgi_server_app(app):
    return app


@pytest.fixture(scope='session')
def wsgi_server(request, wsgi_server_app, wsgi_server_host_port):
    from webtest.http import StopableWSGIServer
    host, port = wsgi_server_host_port

    server = StopableWSGIServer.create(
        wsgi_server_app,
        host=host,
        port=port,
        threads=1,
        channel_timeout=60,
        cleanup_interval=10,
        expose_tracebacks=True,
        clear_untrusted_proxy_headers=False,
    )
    assert server.wait()

    yield 'http://%s:%s' % wsgi_server_host_port

    server.shutdown()
