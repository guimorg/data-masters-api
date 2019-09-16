"""Testing main score function"""
from api import model


def test_score():
    # Defining a simple dict containing data that is going to be
    # sent to score function
    data = {'text': 'Hello World! I am feeling very well today!'}

    # We are only testing if we can reach a final conclusion
    # regarding our prediction, we don't need to test all
    # particularities about the model!
    prediction = model.score(data)

    assert prediction
    assert all([x in prediction.keys() for x in ['score', 'label']])
    # Makes sense because we are giving a positive message
    assert prediction['score'] >= 0.5
