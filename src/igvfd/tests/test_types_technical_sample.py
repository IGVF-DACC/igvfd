import pytest


def test_technical_sample_summary(testapp, technical_sample, construct_library_set_reporter, construct_library_set_genome_wide):
    res = testapp.get(technical_sample['@id'])
    assert res.json.get('summary') == 'synthetic technical sample'
    testapp.patch_json(
        technical_sample['@id'],
        {
            'virtual': True
        }
    )
    res = testapp.get(technical_sample['@id'])
    assert res.json.get('summary') == 'virtual synthetic technical sample'
    testapp.patch_json(
        technical_sample['@id'],
        {
            'construct_library_sets': [construct_library_set_reporter['@id']]
        }
    )
    res = testapp.get(technical_sample['@id'])
    assert res.json.get('summary') == 'virtual synthetic technical sample modified with a reporter library'
    testapp.patch_json(
        technical_sample['@id'],
        {
            'construct_library_sets': [construct_library_set_reporter['@id'],
                                       construct_library_set_genome_wide['@id']]
        }
    )
    res = testapp.get(technical_sample['@id'])
    assert res.json.get('summary') == 'virtual synthetic technical sample modified with multiple libraries'
    testapp.patch_json(
        technical_sample['@id'],
        {
            'moi': 6,
            'nucleic_acid_delivery': 'lentiviral transduction',
        }
    )
    res = testapp.get(technical_sample['@id'])
    assert res.json.get(
        'summary') == 'virtual synthetic technical sample transduced (lentivirus) with multiple libraries (MOI of 6)'
