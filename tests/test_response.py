import pytest

from servant.client import Response

@pytest.fixture
def response():
    return Response.fromDict({
        'actions': [
            {'action_name': 'charge_credit_card',
                'errors': None,
                'field_errors': None,
                'results': {'approved_amount': 94.49,
                            'transaction_id': 2004015948,
                            'transaction_status': 'Approved'}}],
        'response': {'correlation_id': 'f4a1a0ca-24e6-4682-8f8f-b89f25267cdb',
                   'errors': None,
                   'name': 'cc_payment_service',
                   'response_time': '0.54586',
                   'version': 1}
    })

@pytest.fixture
def double_response():
    return Response.fromDict({
        'actions': [
            {
                'action_name': 'charge_credit_card',
                'errors': None,
                'field_errors': None,
                'results': {'approved_amount': 94.49,
                         'transaction_id': 2004015948,
                         'transaction_status': 'Approved'},
            },
            {
                'action_name': 'create_payment_account',
                'errors': None,
                'field_errors': None,
                'results': {'payment_account_id': '6D2F592B-3761-40EC-AC18-B140304B3542'},
             },
        ],
        'response': {'correlation_id': 'f8b56731-3203-4645-a6b3-8c3ddb5559b9',
                    'errors': None,
                    'name': 'cc_payment_service',
                    'response_time': '0.65126',
                    'version': 1}
    })


def test_not_error():
    d = {
        'actions': [ {'errors': None, 'field_errors': None} ],
        'response': {'errors': None},
    }
    resp = Response.fromDict(d)
    assert not resp.is_error()
    assert resp.errors is None

def test_error_from_2nd_action():
    d = {
        'actions': [
            {'errors': None, 'field_errors': None},
            {'errors': 'Client error', 'field_errors': None},
        ],
        'response': {'errors': None},
    }
    resp = Response.fromDict(d)
    assert resp.is_error()
    assert resp.errors is None

def test_error_from_2nd_action_field():
    d = {
        'actions': [
            {'errors': None, 'field_errors': None},
            {'errors': '', 'field_errors': {'input': 'error'}},
        ],
        'response': {'errors': None},
    }
    resp = Response.fromDict(d)
    assert resp.is_error()
    assert resp.errors is None

def test_error_from_response():
    d = {
        'actions': [ {'errors': None, 'field_errors': None} ],
        'response': {'errors': 'There was an error'},
    }
    resp = Response.fromDict(d)
    assert resp.is_error()
    assert resp.errors == 'There was an error'

def test_response_text(response):
    assert  isinstance(response, Response)
    assert isinstance(response.text, basestring)

def test_response_to_native(response):
    assert isinstance(response.to_native(), dict)

def test_single_response(response):
    assert response
    assert response.errors is None
    assert response.action_errors is None
    assert response.field_errors is None

    assert response.meta.response_time == '0.54586'
    assert response.meta.correlation_id == 'f4a1a0ca-24e6-4682-8f8f-b89f25267cdb'
    assert response.meta.version == 1

    assert response.approved_amount == 94.49
    assert response.transaction_id == 2004015948
    assert response.transaction_status == 'Approved'


#def test_double_response(double_response):
#    batch = client.Batch()
#    ref1 = batch.create_charge()
#    ref2 = batch.do_something()
#    resp = batch.execute()
#
#    resp1 = resp.get_action_result(ref1)
#    resp2 = resp.get_action_result(ref2)
#
#    assert double_response.results
#



