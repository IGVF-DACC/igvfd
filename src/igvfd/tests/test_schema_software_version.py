import pytest


def test_post_software_version(testapp, software, lab, award):
    res = testapp.post_json(
        '/software_version',
        {
            'version': 'v2',
            'award': award['@id'],
            'lab': lab['@id'],
            'software': software['@id']
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.post_json(
        '/software_version',
        {
            'version': 'v2.4.4',
            'award': award['@id'],
            'lab': lab['@id'],
            'software': software['@id'],
            'source_url': 'https://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.4.4/'
        })
    assert res.status_code == 201
    # Test if can post various version formats
    res = testapp.post_json(
        '/software_version',
        {
            'version': 'v2.4.4b',
            'award': award['@id'],
            'lab': lab['@id'],
            'software': software['@id'],
            'source_url': 'https://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.4.4b/'
        })
    assert res.status_code == 201
    res = testapp.post_json(
        '/software_version',
        {
            'version': 'v2.4.4.1b',
            'award': award['@id'],
            'lab': lab['@id'],
            'software': software['@id'],
            'source_url': 'https://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.4.4.1b/'
        })
    assert res.status_code == 201
    res = testapp.post_json(
        '/software_version',
        {
            'version': 'v2.4a.4.1b',
            'award': award['@id'],
            'lab': lab['@id'],
            'software': software['@id'],
            'source_url': 'https://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.4a.4.1b/'
        })
    assert res.status_code == 201
    res = testapp.post_json(
        '/software_version',
        {
            'version': 'vb2.4a.4.1b',
            'award': award['@id'],
            'lab': lab['@id'],
            'software': software['@id'],
            'source_url': 'https://sourceforge.net/projects/bowtie-bio/files/bowtie2/b2.4a.4.1b/'
        }, expect_errors=True)
    assert res.status_code == 422
