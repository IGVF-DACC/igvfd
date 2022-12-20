import pytest


def test_post_software(award, lab, testapp):
    res = testapp.post_json(
        '/software',
        {
            'lab': lab['@id'],
            'award': award['@id'],
            'name': 'picard'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.post_json(
        '/software',
        {
            'lab': lab['@id'],
            'award': award['@id'],
            'title': 'Picard',
            'name': 'picard',
            'description': 'A set of tools (in Java) for working with next '
                           'generation high-throughput sequencing (HTS) data '
                           'in the BAM format.',
            'source_url': 'https://bowtie-bio.sourceforge.net/bowtie2/index.shtml'
        })
    assert res.status_code == 201
