def test_sample_1(source, testapp):
    res = testapp.get(source['@id'])
    assert(res.json['name'] == 'sigma')


def test_lab_as_source(lab, award, testapp):

<<<<<<< HEAD
    res = testapp.post_json('/biosample',
=======
    res = testapp.post_json('/cell_line',
>>>>>>> b5fb316 (added tissue)
                            {
                                'award': award['@id'],
                                'lab': lab['@id'],
                                'source': lab['@id']
                            })
    assert(res.status_code == 201)
