"""Testing Application"""
import unittest


async def test_health_check(api):
    """
    Testing Healtcheck endpoint
    """
    res = await api.get('/v1/healthcheck')
    assert res.status == 200
    data = await res.json()
    headers = res.headers
    assert data['status'] == 'running'
    assert headers['Content-Type'] == 'application/json'


async def test_prediction(api):
    """
    Testing Prediction.
    We test for various scenarios involving failure.
    Unfortunately, because MagicMock is not Pickable it would be hard
    """
    # FIXME Improve testing for actual prediction
    # Input Contract Failure
    with unittest.mock.patch('api.routes.model.score') as _:
        data = {'emoji': 'smiley-face'}
        res = await api.post('/v1/predict', json=data)
        assert res.status == 400

        # Output contract failuer
        # Here we are actually testing for an inside Exception
        # But it would be the same behaviour
        data = {'text': 'I hate Javascript'}
        res = await api.post('/v1/predict', json=data)
        assert res.status == 500
