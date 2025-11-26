import pytest
from main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


def test_trends_graph_shape(client):
    res = client.get('/api/trends_graph')
    assert res.status_code == 200
    data = res.get_json()

    assert isinstance(data, dict)
    assert 'labels' in data and 'points' in data

    assert isinstance(data['labels'], list)
    assert len(data['labels']) > 0

    assert isinstance(data['points'], list)
    assert len(data['points']) > 0

    # spot-check fields/types on first few points
    for p in data['points'][:3]:
        assert isinstance(p, dict)
        assert 'topic' in p and isinstance(p['topic'], str) and p['topic']
        assert 'viral_score' in p and isinstance(p['viral_score'], (int, float))
        assert 'momentum' in p and isinstance(p['momentum'], str)
        assert 'hashtags' in p and isinstance(p['hashtags'], list)


def test_trends_graph_disallows_post(client):
    # Ensure POST isn't accepted for this read-only endpoint (should not be 200)
    res = client.post('/api/trends_graph')
    assert res.status_code != 200
