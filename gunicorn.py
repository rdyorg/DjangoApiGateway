import multiprocessing

bind = '127.0.0.1:10001'
workers = multiprocessing.cpu_count() * 2 + 1

reload = True
backlog = 2048
worker_class = "gevent"
worker_connections = 1000
daemon = True
debug = True
proc_name = 'django_api_gateway'
pidfile = '/root/logs/api_gateway_gunicorn.pid'
accesslog = '/root/logs/api_gateway_access.log'
errorlog = '/root/logs/api_gateway_error.log'
