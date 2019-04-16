#!/usr/bin/env python3

"""APIs to invoke the worker flow."""

import os
import flask
import logging
from flask import Flask, request, current_app
from flask_cors import CORS


def setup_logging(flask_app):
    """Perform the setup of logging (file, log level) for this application."""
    if not flask_app.debug:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
        log_level = os.environ.get('FLASK_LOGGING_LEVEL', logging.getLevelName(logging.WARNING))
        handler.setLevel(log_level)

        flask_app.logger.addHandler(handler)
        flask_app.config['LOGGER_HANDLER_POLICY'] = 'never'
        flask_app.logger.setLevel(logging.DEBUG)


app = Flask(__name__)
setup_logging(app)
CORS(app)


@app.route('/api/v1/readiness')
def readiness():
    """Handle GET requests that are sent to /api/v1/readiness REST API endpoint."""
    current_app.logger.debug('/readiness called')
    return flask.jsonify({}), 200


@app.route('/api/v1/liveness')
def liveness():
    """Handle GET requests that are sent to /api/v1/liveness REST API endpoint."""
    current_app.logger.debug('/liveness called')
    return flask.jsonify({}), 200


if __name__ == "__main__":
    app.run()
