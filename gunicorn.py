import os

def syslog_address():
    papertrail_port = os.getenv('SS_SORAYA_RECO_LOGGING_PORT')

    if not papertrail_port:
        return "udp://"

    return "udp://logs4.papertrailapp.com:" + papertrail_port

def workers():
    return int(os.getenv('SS_SORAYA_RECO_GUNICORN_TOTAL_WORKERS', 2))

def timeout():
    return int(os.getenv('SS_SORAYA_RECO_GUNICORN_TIMEOUT', 2400))

workers = workers()
bind = "0.0.0.0:9012"
timeout = timeout()
syslog_addr = syslog_address()
syslog = True
loglevel = 'debug'
accesslog = '-'
