import pytest


def test_technical_sample_summary(testapp, technical_sample, construct_library_set_reporter, construct_library_set_genome_wide, treatment_chemical):
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
    assert res.json.get(
        'summary') == 'virtual synthetic technical sample transfected with a reporter library targeting accessible genome regions genome-wide'
    testapp.patch_json(
        technical_sample['@id'],
        {
            'construct_library_sets': [construct_library_set_reporter['@id'],
                                       construct_library_set_genome_wide['@id']]
        }
    )
    res = testapp.get(technical_sample['@id'])
    assert res.json.get('summary') == 'virtual synthetic technical sample transfected with multiple libraries'
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
    testapp.patch_json(
        technical_sample['@id'],
        {
            'treatments': [treatment_chemical['@id']]
        }
    )
    res = testapp.get(technical_sample['@id'])
    assert res.json.get(
        'summary') == 'virtual synthetic technical sample activated with 10 mM lactate for 1 hour, transduced (lentivirus) with multiple libraries (MOI of 6)'


def test_technical_sample_parts(testapp, technical_sample, technical_sample_organic, technical_sample_inorganic):
    testapp.patch_json(
        technical_sample_organic['@id'],
        {
            'part_of': technical_sample['@id']
        }
    )
    testapp.patch_json(
        technical_sample_inorganic['@id'],
        {
            'part_of': technical_sample['@id']
        }
    )
    res = testapp.get(technical_sample['@id'])
    assert set(res.json.get('parts')) == {technical_sample_organic['@id'], technical_sample_inorganic['@id']}
