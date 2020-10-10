import requests
import json

def test_predict_income():
    with open('tests/sample_input.json') as f:
        test_data = json.load(f)

    r = requests.post('http://127.0.0.1:8000/predict/', data=json.dumps(test_data))

    with open('tests/sample_output.json') as f:
        test_out = json.load(f)

    assert r.json() == test_out