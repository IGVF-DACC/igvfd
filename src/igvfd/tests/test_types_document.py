def test_document_superseded_by(testapp, experimental_protocol_document, plasmid_map_document):
    original = experimental_protocol_document['@id']
    replacement = plasmid_map_document['@id']
    assert 'superseded_by' not in testapp.get(original).json

    testapp.patch_json(replacement, {'supersedes': [original]})
    assert testapp.get(replacement).json['supersedes'] == [original]
    assert testapp.get(original).json['superseded_by'] == [replacement]

    testapp.patch_json(replacement, {'status': 'deleted'})
    assert 'superseded_by' not in testapp.get(original).json
