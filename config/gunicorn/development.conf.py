bind = '0.0.0.0:6543'
workers = 7
threads = 1
accesslog = '-'
logger_class = 'igvfd.logging.gunicornlogger.MyGunicornLogger'
access_log_format = '{\"host\":"%(h)s", \"user\":"%(u)s", \"time\":"%(t)s", \"statusline\":"%(r)s", \"status\":%(s)s, \"response_length\":%(b)s, \"referer\":"%(f)s", \"user_agent\":"%(a)s", \"db_count\":%(db_count)d, \"db_time\":%(db_time)d, \"es_count\":%(es_count)d, \"es_time\":%(es_time)d, \"rss_begin\": %(rss_begin)d, \"rss_end\": %(rss_end)d, \"rss_change\": %(rss_change)d, \"wsgi_begin\":%(wsgi_begin)d,  \"wsgi_end\":%(wsgi_end)d, \"wsgi_time\":%(wsgi_time)d}'
