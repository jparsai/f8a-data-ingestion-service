"""Test module."""

import json
from unittest.mock import patch


payload_data = {

}


def api_route_for(route):
    """Construct an URL to the endpoint for given route."""
    return '/api/v1/' + route


def test_worker_flow(client):
    """Test the /api/v1/worker-flow/<flow_name> endpoint."""
    resp = client.post(api_route_for('worker-flow/bayesianApiFlow'),
                       data=json.dumps(payload_data),
                       content_type='application/json')

    assert resp.status_code == 200
