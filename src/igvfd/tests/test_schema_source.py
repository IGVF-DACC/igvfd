def test_sample_1(source, testapp):
    res = testapp.get(source['@id'])
    assert(res.json['name'] == 'sigma')


def test_lab_as_source(lab, award, testapp):
    res = testapp.post_json('/cell_line',
                            {
                                'award': award['@id'],
                                'lab': lab['@id'],
                                'source': lab['@id']
                            })
    assert(res.status_code == 201)
