import pytest

import time


pytestmark = [pytest.mark.indexing]


def wait_for_indexing():
    time.sleep(30)


def test_indexing_simple_igvfd(testapp, workbook):
    response = testapp.post_json('/testing-post-put-patch/', {'required': ''})
    response = testapp.post_json('/testing-post-put-patch/', {'required': ''})
    wait_for_indexing()
    response = testapp.get('/search/?type=TestingPostPutPatch')
    assert len(response.json['@graph']) == 2


def test_indexing_updated_name_invalidates_dependents(testapp, dummy_request, workbook):
    response = testapp.get('/search/?type=User&lab=/labs/j-michael-cherry/')
    assert len(response.json['@graph']) >= 22
    tq = dummy_request.registry['TRANSACTION_QUEUE']
    testapp.patch_json(
        '/labs/j-michael-cherry/',
        {'name': 'some-other-name'}
    )
    print('Wait for queue to drain')
    tq.wait_for_queue_to_drain()
    response = testapp.get('/search/?type=User&lab=/labs/some-other-name/')
    assert len(response.json['@graph']) >= 22
    testapp.get('/search/?type=User&lab=/labs/j-michael-cherry/', status=404)
    testapp.patch_json(
        '/labs/some-other-name/',
        {'name': 'j-michael-cherry'}
    )
    print('Wait for queue to drain')
    tq.wait_for_queue_to_drain()
    print('Wait for indexing')
    wait_for_indexing()
    testapp.get('/search/?type=User&lab=/labs/some-other-lab/', status=404)
    response = testapp.get('/search/?type=User&lab=/labs/j-michael-cherry/')
    assert len(response.json['@graph']) >= 22
