import pytest
from main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


def test_process_caption_success(client):
    payload = {"caption": "This is a unit test caption to validate processing."}
    res = client.post('/api/process_caption', json=payload)

    # Should succeed under normal app behavior
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, dict)

    # Expect at least one of the major keys to be present
    keys = set(data.keys())
    assert 'optimized_caption' in keys or 'seo' in keys or 'seo_original' in keys

    # If SEO data provided, check types
    if 'seo_original' in data and data['seo_original'] is not None:
        s = data['seo_original']
        assert isinstance(s.get('score', 0), (int, float))

    # If emotion provided, it should be a dict
    if 'emotion' in data:
        assert isinstance(data['emotion'], dict)


def test_process_caption_empty_caption_handled(client):
    # When caption is empty, endpoint should handle gracefully
    res = client.post('/api/process_caption', json={"caption": ""})

    # Accept either a non-200 status or a 200 with an 'error' key in JSON
    if res.status_code == 200:
        data = res.get_json()
        assert isinstance(data, dict)
        assert 'error' in data
    else:
        assert res.status_code in (400, 422)
