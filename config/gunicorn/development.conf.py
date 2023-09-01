bind = '0.0.0.0:6543'
workers = 7
threads = 1
accesslog = '-'
logger_class = 'igvfd.logging.gunicornlogger.MyGunicornLogger'
access_log_format = '{\"host\":"%(h)s", \"user\":"%(u)s", \"time\":"%(t)s", \"statusline\":"%(r)s", \"status\":%(s)s, \"response_length\":%(b)s, \"referer\":"%(f)s", \"user_agent\":"%(a)s", \"db_count\":"%(db_count)i", \"db_time\":"%(db_time)i", \"es_count\":"%(es_count)i", \"es_time\":"%(es_time)i", \"rss_begin\": "%(rss_begin)i", \"rss_end\": "%(rss_end)i", \"rss_change\": "%(rss_change)i", \"wsgi_begin\":"%(wsgi_begin)i",  \"wsgi_end\":"%(wsgi_end)i", \"wsgi_time\":"%(wsgi_time)i"}'
