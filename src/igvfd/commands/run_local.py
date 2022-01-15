"""\
Examples
For the development.ini you must supply the paster app name:
    %(prog)s development.ini --app-name app --init --clear
"""
from pyramid.paster import get_app, get_appsettings
from multiprocessing import Process, set_start_method
from pathlib import Path

import atexit
import logging
import os.path
import select
import shutil
import sys
import subprocess
import time


EPILOG = __doc__

logger = logging.getLogger(__name__)


def print_to_terminal(stdout):
    while True:
        printed = False
        for line in iter(stdout.readline, b''):
            if line:
                sys.stdout.write(line.decode('utf-8'))
                printed = True
        if not printed:
            time.sleep(0.1)


def nginx_server_process(prefix='', echo=False):
    args = [
        os.path.join(prefix, 'nginx'),
        '-c', f'{Path().absolute()}/config/nginx/local.conf',
        '-g', 'daemon off; pid /dev/null;'
    ]
    process = subprocess.Popen(
        args,
        close_fds=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    if not echo:
        process.stdout.close()

    if echo:
        print('Started: http://localhost:8000')

    return process


def main():
    set_start_method("fork")
    import argparse
    parser = argparse.ArgumentParser(
        description="Run development servers", epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '--app-name',
        default='app',
        help='Pyramid app name in configfile',
    )
    parser.add_argument(
        '--config-uri',
        default=f'{Path().absolute()}/config/pyramid/ini/development.ini',
        help='path to configfile',
    )
    parser.add_argument('--clear', action="store_true", help="Clear existing data")
    parser.add_argument('--init', action="store_true", help="Init database")
    parser.add_argument('--load', action="store_true", help="Load test set")
    parser.add_argument('--datadir', default='/tmp/igvfd', help="path to datadir")
    args = parser.parse_args()

    logging.basicConfig()
    # Loading app will have configured from config file. Reconfigure here:
    logging.getLogger('igvfd').setLevel(logging.INFO)

    from snovault.tests import postgresql_fixture
    datadir = os.path.abspath(args.datadir)
    pgdata = os.path.join(datadir, 'pgdata')

    if args.clear:
        for dirname in [pgdata]:
            if os.path.exists(dirname):
                shutil.rmtree(dirname)
    if args.init:
        postgresql_fixture.initdb(pgdata, echo=True)

    print_processes = []

    postgres = postgresql_fixture.server_process(pgdata, echo=True)
    nginx = nginx_server_process(echo=True)
    processes = [postgres, nginx]

    @atexit.register
    def cleanup_process():
        for process in processes:
            if process.poll() is None:
                process.terminate()
        for process in processes:
            try:
                for line in process.stdout:
                    sys.stdout.write(line.decode('utf-8'))
            except IOError:
                pass
            process.wait()
        for p in print_processes:
            p.terminate()

    if args.init:
        app = get_app(args.config_uri, args.app_name)

    if args.load:
        from igvfd.loadxl import load_test_data
        load_test_data(app)

    print('Started. ^C to exit.')

    stdouts = [p.stdout for p in processes]
    readable, writable, err = select.select(stdouts, [], stdouts, 5)
    for stdout in readable:
        print_processes.append(Process(target=print_to_terminal, args=(stdout,)))
    for stdout in err:
        print_processes.append(Process(target=print_to_terminal, args=(stdout,)))
    for p in print_processes:
        p.start()

if __name__ == '__main__':
    main()
