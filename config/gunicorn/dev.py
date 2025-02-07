"""Gunicorn *development* config file"""
# code from : https://realpython.com/django-nginx-gunicorn/#replacing-wsgiserver-with-gunicorn

# Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
wsgi_app = "django_project.wsgi:application"
# The granularity of Error log outputs
loglevel = "debug"
# The number of worker processes for handling requests
workers = 2
# The socket to bind
bind = "0.0.0.0:8000"
# Restart workers when code changes (development only!)
reload = True
# Write access and error log
accesslog = errorlog = "-"
# Redirect stdout/stderr to log file
capture_output = True
# PID file so you can easily fetch process ID
pidfile = "/tmp/gunicorn_dev.pid"