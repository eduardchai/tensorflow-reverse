from flask import Flask, request, jsonify
from soraya_train import SorayaRecommenderEngine
import app_logging

import os
import tensorflow as tf
import bugsnag
from bugsnag.flask import handle_exceptions

app = Flask(__name__)

batch_size = 1  # We decode one sentence at a time.
ct_vocab_path = os.path.join("./data_dir", "vocab%d.ct" % 10000)
op_vocab_path = os.path.join("./data_dir", "vocab%d.op" % 10000)
engine = SorayaRecommenderEngine(batch_size, ct_vocab_path, op_vocab_path)

@app.errorhandler(404)
def route_not_found(e):
        response = jsonify(message='Route not found', status=404)
        response.status_code = 404
        return response

@app.route('/reply')
def index():
    query = request.args.get('q')
    return engine.getReply(query)

from flask import got_request_exception

def setup_app(app):
    #setup syslog
    app.logger.addFilter(app_logging.ContextFilter())
    syslog_handler = app_logging.get_syslog_handler()
    if syslog_handler:
        app.logger.addHandler(syslog_handler)
        #send application error exception message to log
        def log_exception(sender, exception, **extra):
            sender.logger.error(exception)
        got_request_exception.connect(log_exception, app)
        #setup bugsnag
        bugsnag_api_key =  os.getenv('SS_SORAYA_RECO_BUGSNAG_API_KEY')
        if bugsnag_api_key:
            bugsnag.configure(
                api_key= bugsnag_api_key,
                project_root=os.path.abspath(os.path.dirname(__file__)),
                release_stage=os.getenv('SS_SORAYA_RECO_RELEASE_STAGE'))
            handle_exceptions(app)

setup_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9012, debug=True, use_reloader=False)
