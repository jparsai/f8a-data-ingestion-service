"""Test module."""

import json
from unittest import mock

blank_data = {}
payload_data = {
    "worker-data": "abcd"
}


class Dispatcher:
    """Mocked Dispatcher object class."""

    def __init__(self, id):
        """Create a mock json response."""
        self.id = id


def api_route_for(route):
    """Construct an URL to the endpoint for given route."""
    return 'http://localhost:5000/api/v1/' + route


def get_json_from_response(response):
    """Decode JSON from response."""
    return json.loads(response.data.decode('utf8'))


def test_liveness_endpoint(client):
    """Test the /api/v1/liveness endpoint."""
    response = client.get(api_route_for("liveness"))
    assert response.status_code == 200
    json_data = get_json_from_response(response)
    assert json_data == {}, "Empty JSON response expected"


def test_readiness_endpoint(client):
    """Test the /api/v1/readiness endpoint."""
    response = client.get(api_route_for("readiness"))
    assert response.status_code == 200
    json_data = get_json_from_response(response)
    assert json_data == {}, "Empty JSON response expected"


def test_worker_flow(client):
    """Test the /api/v1/worker_flow/<flow-name> endpoint."""
    rec_resp = client.post(api_route_for("worker-flow/testFlow"),
                           data=json.dumps(blank_data),
                           content_type='application/json')
    assert rec_resp.status_code == 400
    json_data = get_json_from_response(rec_resp)
    assert json_data['message'] == "Incorrect data sent"


@mock.patch('src.rest_api.run_server_flow')
def test_worker_flow1(mocker, client):
    """Test the /api/v1/worker_flow/<flow-name> endpoint."""
    mocker.return_value = Dispatcher(11111)
    rec_resp = client.post(api_route_for("worker-flow/testFlow"),
                           data=json.dumps(payload_data),
                           content_type='application/json')
    assert rec_resp.status_code == 200
    json_data = get_json_from_response(rec_resp)
    assert json_data['id'] == 11111


if __name__ == '__main__':
    test_readiness_endpoint()
    test_liveness_endpoint()
    test_worker_flow()
    test_worker_flow1()
