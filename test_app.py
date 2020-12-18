from app import app

import pytest
import json

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_app1_valid_input(client):
    payload = dict(
        job_name = "Tapan",
        job_id = 4,
        num_jobs = 11,
        job_duration = 3,
        )
    payload = json.dumps(payload)
    result = client.post('/job_done', data=payload, content_type='application/json')
    assert b"OK" in result.data

def test_app2_invalid_jobname_1(client):
    payload = dict(
        job_name = None,
        job_id = 1,
        num_jobs = 2,
        job_duration = 2,
        )
    payload = json.dumps(payload)
    result = client.post('/job_done', data=payload, content_type='application/json')
    assert b"Invalid Input" in result.data

def test_app3_invalid_jobname_2(client):
    payload = dict(
        job_name = "",
        job_id = 1,
        num_jobs = 2,
        job_duration = 2,
        )
    payload = json.dumps(payload)
    result = client.post('/job_done', data=payload, content_type='application/json')
    assert b"Invalid Input" in result.data

def test_app4_invalid_jobid_1(client):
    payload = dict(
        job_name = "Tapan",
        job_id = 3,
        num_jobs = 2,
        job_duration = 15,
        )
    payload = json.dumps(payload)
    result = client.post('/job_done', data=payload, content_type='application/json')
    assert b"Invalid Input" in result.data

def test_app5_invalid_jobname_3(client):
    payload = dict(
        job_name = "j-1234858585858585858588585948359348594385983",
        job_id = 1,
        num_jobs = 50,
        job_duration = 2,
        )
    payload = json.dumps(payload)
    result = client.post('/job_done', data=payload, content_type='application/json')
    assert b"Invalid Input" in result.data

def test_app6_invalid_numjobs_1(client):
    payload = dict(
        job_name = "Tapan",
        job_id = 1,
        num_jobs = 101,
        job_duration = 29,
        )
    payload = json.dumps(payload)
    result = client.post('/job_done', data=payload, content_type='application/json')
    assert b"Invalid Input" in result.data

def test_app7_invalid_jobduration_1(client):
    payload = dict(
        job_name = "Tapan",
        job_id = 1,
        num_jobs = 99,
        job_duration = 0,
        )
    payload = json.dumps(payload)
    result = client.post('/job_done', data=payload, content_type='application/json')
    assert b"Invalid Input" in result.data

def test_app8_invalid_jobduration_2(client):
    payload = dict(
        job_name = "Tapan",
        job_id = 1,
        num_jobs = 100,
        job_duration = 31,
        )
    payload = json.dumps(payload)
    result = client.post('/job_done', data=payload, content_type='application/json')
    assert b"Invalid Input" in result.data

def test_app9_invalid_jobid_2(client):
    payload = dict(
        job_name = "Tapan",
        job_id = -1,
        num_jobs = 100,
        job_duration = 31,
        )
    payload = json.dumps(payload)
    result = client.post('/job_done', data=payload, content_type='application/json')
    assert b"Invalid Input" in result.data

def test_app10_invalid_jobid_3(client):
    payload = dict(
        job_name = "Tapan",
        job_id = 102,
        num_jobs = 100,
        job_duration = 20,
        )
    payload = json.dumps(payload)
    result = client.post('/job_done', data=payload, content_type='application/json')
    assert b"Invalid Input" in result.data

def test_app11_all_invalid(client):
    payload = dict(
        job_name = "",
        job_id = -1,
        num_jobs = 0,
        job_duration = 0,
        )

    result = client.post('/job_done', json=payload)
    assert b"Invalid Input" in result.data

def test_app12_job_status_1(client):
    
    result = client.get('/job_status')
    assert b'{"Tapan":{"completed":1,"total":11}' in result.data

def test_app13_too_many_jobs_1(client):
    """
    This test case is for when the monitoring system gets more than num_jobs number of jobs under a given job_name
    Since num_jobs here is 11, I'm giving 12 jobs under name 'Tapan'.
    """
    payload = dict(
        job_name = "Tapan",
        job_id = 4,
        num_jobs = 11,
        job_duration = 3,
        )
    payload = json.dumps(payload)
    result = client.post('/job_done', data=payload, content_type='application/json')
    result = client.post('/job_done', data=payload, content_type='application/json')
    result = client.post('/job_done', data=payload, content_type='application/json')
    result = client.post('/job_done', data=payload, content_type='application/json')
    result = client.post('/job_done', data=payload, content_type='application/json')
    result = client.post('/job_done', data=payload, content_type='application/json')
    result = client.post('/job_done', data=payload, content_type='application/json')
    result = client.post('/job_done', data=payload, content_type='application/json')
    result = client.post('/job_done', data=payload, content_type='application/json')
    result = client.post('/job_done', data=payload, content_type='application/json')
    result = client.post('/job_done', data=payload, content_type='application/json')
    assert b"Don't send more jobs." in result.data

def test_app14_job_status_2(client):
    result = client.get('/job_status')
    assert b'{"Tapan":{"completed":11,"total":11}' in result.data
    

