import pytest


def test_post_workflow_version(testapp, lab, award):
    # stanford workflow version testing
    res = testapp.post_json(
        '/workflow',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'name': 'test workflow',
            'workflow_version': 'v1.0.0'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.post_json(
        '/workflow',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'name': 'test workflow',
            'workflow_version': 'v2.4.4',
            'source_url': 'https://github.com/projects/bowtie-bio/files/bowtie2/'
        })
    assert res.status_code == 201
    res = testapp.post_json(
        '/workflow',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'name': 'test workflow',
            'workflow_version': 'v2.4.4.1',
            'source_url': 'https://github.com/projects/bowtie-bio/files/bowtie2/'
        })
    assert res.status_code == 201
    # Test if can post various version formats with letters
    res = testapp.post_json(
        '/workflow',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'name': 'test workflow',
            'workflow_version': 'v2.4.4b',
            'source_url': 'https://github.com/projects/bowtie-bio/files/bowtie2/'
        })
    res = testapp.post_json(
        '/workflow',
        {
            'workflow_version': 'v2.4b.4b',
            'award': award['@id'],
            'lab': lab['@id'],
            'name': 'test workflow',
            'source_url': 'https://github.com/projects/bowtie-bio/files/bowtie2/'
        })
    res = testapp.post_json(
        '/workflow',
        {
            'workflow_version': 'v2b.4c.4b',
            'award': award['@id'],
            'lab': lab['@id'],
            'name': 'test workflow',
            'source_url': 'https://github.com/projects/bowtie-bio/files/bowtie2/'
        })
