def test_sample_1(source, testapp):
    res = testapp.get(source['@id'])
    assert res.json['name'] == 'sigma'


def test_lab_as_source(lab, award, testapp, human_donor, sample_term_K562):
    res = testapp.post_json('/in_vitro_system',
                            {
                                'award': award['@id'],
                                'lab': lab['@id'],
                                'sources': [lab['@id']],
                                'donors': [human_donor['@id']],
                                'sample_terms': [sample_term_K562['@id']],
                                'classifications': ['cell line']
                            })
    assert res.status_code == 201
