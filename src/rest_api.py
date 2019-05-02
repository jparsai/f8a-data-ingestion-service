#!/usr/bin/env python3

"""APIs to invoke the worker flow."""

import os
import flask
import logging
from flask import Flask, request, current_app
from flask_cors import CORS
from f8a_worker.setup_celery import init_celery, init_selinon
from selinon import run_flow
import datetime


def setup_logging(flask_app):
    """Perform the setup of logging (file, log level) for this application."""
    if not flask_app.debug:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
        log_level = os.environ.get('FLASK_LOGGING_LEVEL',
                                   logging.getLevelName(logging.WARNING))
        handler.setLevel(log_level)

        flask_app.logger.addHandler(handler)
        flask_app.config['LOGGER_HANDLER_POLICY'] = 'never'
        flask_app.logger.setLevel(logging.DEBUG)


app = Flask(__name__)
setup_logging(app)
CORS(app)


@app.route('/api/v1/readiness')
def readiness():
    """Handle GET requests for /api/v1/readiness REST API."""
    current_app.logger.debug('/readiness called')
    return flask.jsonify({}), 200


@app.route('/api/v1/liveness')
def liveness():
    """Handle GET requests for /api/v1/liveness REST API."""
    current_app.logger.debug('/liveness called')
    return flask.jsonify({}), 200


@app.route('/api/v1/worker-flow/<flow_name>', methods=['POST'])
def worker_flow(flow_name):
    """Handle POST requests for /api/v1/worker-flow/{flow-name} REST API."""
    current_app.logger.info('/worker-flow/{p} called'.format(p=flow_name))
    input_json = request.get_json()
    resp = {
        "id": "",
        "submitted_at": "",
        "status": ""
    }
    if input_json and 'worker-data' in input_json:
        start = datetime.datetime.now()
        flow_args = input_json['worker-data']
        try:
            dispacher_id = run_server_flow(flow_name, flow_args)
            resp['id'] = dispacher_id.id
            resp['submitted_at'] = start.strftime("%d-%m-%Y, "
                                                  "%H:%M:%S")
            resp['status'] = "Flow Initiated"

            # compute the elapsed time
            elapsed_seconds = (datetime.datetime.now() - start).total_seconds()
            current_app.logger.debug(
                "It took {t} seconds to start {f} flow.".format(
                    t=elapsed_seconds, f=flow_name))
        except Exception as e:
            current_app.logger.error(
                "Exception while initiating the worker flow --> {}"
                .format(e))
            return flask.jsonify(
                {'message': 'Failed to initiate worker flow'}), 500
    else:
        current_app.logger.debug('Incorrect data sent for the POST call: {p}'
                                 .format(p=input_json))
        return flask.jsonify({"message": "Incorrect data sent"}), 400

    return flask.jsonify(resp), 200


def run_server_flow(flow_name, flow_args):
    """To run the worker flow via selinon."""
    init_celery(result_backend=False)
    init_selinon()
    return run_flow(flow_name, flow_args)


if __name__ == "__main__":
    app.run()
