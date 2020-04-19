import requests
def test_index():
    r = requests.get("http://0.0.0.0:5000")
    print(r.status_code)
    assert r.status_code == 200

def test_login():
    r = requests.get("http://0.0.0.0:5000/login")
    print(r.status_code)
    assert r.status_code == 200

def test_democonstula():
    r = requests.get("http://0.0.0.0:5000/democonstula")
    print(r.status_code)
    assert r.status_code == 200

def test_repuestateleconsulta():
    r = requests.get("http://0.0.0.0:5000/repuestateleconsulta")
    print(r.status_code)
    assert r.status_code == 200