import pytest
from app import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_instances(client):
    ""Test getting all instances"""
    response = client.get('/instances')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'data' in data
    assert isinstance(data['data'], list)
    assert len(data['data']) > 0

def test_stop_instance_success(client):
    ""Test stopping a running instance"""
    # First get all instances to find a running one
    response = client.get('/instances')
    instances = json.loads(response.data)['data']
    running_instance = next((i for i in instances if i['state'] == 'running'), None)
    
    if running_instance:
        instance_id = running_instance['id']
        response = client.post(f'/instances/{instance_id}/stop')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'stopped successfully' in data['message']

def test_stop_nonexistent_instance(client):
    ""Test stopping a non-existent instance"""
    response = client.post('/instances/i-nonexistent/stop')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'not found' in data['message'].lower()
