bind = '0.0.0.0:6543'
workers = 4
threads = 1
accesslog = '-'
access_log_format = '{\"host\":"%(h)s", \"user\":"%(u)s", \"time\":"%(t)s", \"statusline\":"%(r)s", \"status\":%(s)s, \"response_length\":%(b)s, \"referer\":"%(f)s", \"user_agent\":"%(a)s", \"x_stats\":"%({X-Stats}o)s"}'
