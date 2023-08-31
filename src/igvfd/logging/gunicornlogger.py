import logging
import os
import time
logging.Logger.manager.emittedNoHandlerWarning = 1  # noqa

import gunicorn.glogging


class MyGunicornLogger(gunicorn.glogging.Logger):

    def setup(self, cfg):
        super().setup(cfg)

    def atoms(self, resp, req, environ, request_time):
        """ Gets atoms for log formatting.
        """
        status = resp.status
        if isinstance(status, str):
            status = status.split(None, 1)[0]
        atoms = {
            'h': environ.get('REMOTE_ADDR', '-'),
            'l': '-',
            'u': self._get_user(environ) or '-',
            't': self.now(),
            'r': '%s %s %s' % (environ['REQUEST_METHOD'],
                               environ['RAW_URI'],
                               environ['SERVER_PROTOCOL']),
            's': status,
            'm': environ.get('REQUEST_METHOD'),
            'U': environ.get('PATH_INFO'),
            'q': environ.get('QUERY_STRING'),
            'H': environ.get('SERVER_PROTOCOL'),
            'b': getattr(resp, 'sent', None) is not None and str(resp.sent) or '-',
            'B': getattr(resp, 'sent', None),
            'f': environ.get('HTTP_REFERER', '-'),
            'a': environ.get('HTTP_USER_AGENT', '-'),
            'T': request_time.seconds,
            'D': (request_time.seconds * 1000000) + request_time.microseconds,
            'M': (request_time.seconds * 1000) + int(request_time.microseconds / 1000),
            'L': '%d.%06d' % (request_time.seconds, request_time.microseconds),
            'p': '<%s>' % os.getpid(),
        }

        # add request headers
        if hasattr(req, 'headers'):
            req_headers = req.headers
        else:
            req_headers = req

        if hasattr(req_headers, 'items'):
            req_headers = req_headers.items()

        atoms.update({'{%s}i' % k.lower(): v for k, v in req_headers})

        resp_headers = resp.headers
        if hasattr(resp_headers, 'items'):
            resp_headers = resp_headers.items()

        # add response headers
        atoms.update({'{%s}o' % k.lower(): v for k, v in resp_headers})

        # add environ variables
        environ_variables = environ.items()
        atoms.update({'{%s}e' % k.lower(): v for k, v in environ_variables})

        # separate x-stats and add to atoms
        if '{x-stats}o' in atoms:
            try:
                x_stats = atoms['{x-stats}o'].split('&')
                x_stats_tokens = [{x[0]: x[1]} for x in [x.split('=') for x in x_stats]]
                for token in x_stats_tokens:
                    atoms.update(token)
            except IndexError:
                return atoms
        return atoms
