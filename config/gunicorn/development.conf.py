bind = '0.0.0.0:6543'
workers = 7
threads = 1
accesslog = '-'
logger_class = 'igvfd.logging.gunicornlogger.MyGunicornLogger'
access_log_format = '{\"host\":"%(h)s", \"user\":"%(u)s", \"time\":"%(t)s", \"statusline\":"%(r)s", \"status\":%(s)s, \"response_length\":%(b)s, \"referer\":"%(f)s", \"user_agent\":"%(a)s", \"db_count\":"%(db_count)s", \"db_time\":"%(db_time)s", \"es_count\":"%(es_count)s", \"es_time\":"%(es_time)s", \"rss_begin\": "%(rss_begin)s", \"rss_end\": "%(rss_end)s", \"rss_change\": "%(rss_change)s", \"wsgi_begin\":"%(wsgi_begin)s",  \"wsgi_end\":"%(wsgi_end)s", \"wsgi_time\":"%(wsgi_time)s"}'
