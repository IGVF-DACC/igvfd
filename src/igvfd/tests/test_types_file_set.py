import pytest


def test_files_link(testapp, sequence_file, reference_file, measurement_set):
    testapp.patch_json(
        sequence_file['@id'],
        {
            'file_set': measurement_set['@id']
        }
    )
    testapp.patch_json(
        reference_file['@id'],
        {
            'file_set': measurement_set['@id']
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert set([file_id['@id'] for file_id in res.json.get('files')]) == {sequence_file['@id'], reference_file['@id']}
    testapp.patch_json(
        sequence_file['@id'],
        {
            'status': 'deleted'
        }
    )
    res = testapp.get(measurement_set['@id'])
    assert set([file_id['@id'] for file_id in res.json.get('files')]) == {reference_file['@id']}


def test_control_link(testapp, measurement_set, curated_set_genome):
    testapp.patch_json(
        measurement_set['@id'],
        {
            'control_file_sets': [curated_set_genome['@id']]
        }
    )
    res = testapp.get(curated_set_genome['@id'])
    assert set([file_set_id['@id'] for file_set_id in res.json.get('control_for')]) == {measurement_set['@id']}


def test_curated_set_assembly(testapp, reference_file, reference_file_two, curated_set_genome):
    testapp.patch_json(
        reference_file['@id'],
        {
            'file_set': curated_set_genome['@id'],
            'assembly': 'GRCh38'
        }
    )
    testapp.patch_json(
        reference_file_two['@id'],
        {
            'file_set': curated_set_genome['@id'],
            'assembly': 'hg19'
        }
    )
    curated_set_result = testapp.get(curated_set_genome['@id']).json
    assert {'GRCh38', 'hg19'} == set(curated_set_result.get('assembly', []))


def test_curated_set_transcriptome_annotation(testapp, reference_file, reference_file_two, curated_set_genome):
    testapp.patch_json(
        reference_file['@id'],
        {
            'file_set': curated_set_genome['@id'],
            'transcriptome_annotation': 'GENCODE 40'
        }
    )
    testapp.patch_json(
        reference_file_two['@id'],
        {
            'file_set': curated_set_genome['@id'],
            'transcriptome_annotation': 'GENCODE 41'
        }
    )
    curated_set_result = testapp.get(curated_set_genome['@id']).json
    assert {'GENCODE 40', 'GENCODE 41'} == set(curated_set_result.get('transcriptome_annotation', []))


def test_curated_set_summary(testapp, reference_file, reference_file_two, curated_set_genome):
    testapp.patch_json(
        reference_file['@id'],
        {
            'file_set': curated_set_genome['@id'],
            'transcriptome_annotation': 'GENCODE 40',
            'assembly': 'GRCh38'
        }
    )
    testapp.patch_json(
        reference_file_two['@id'],
        {
            'file_set': curated_set_genome['@id'],
            'transcriptome_annotation': 'GENCODE 41',
            'assembly': 'hg19'
        }
    )
    testapp.patch_json(
        curated_set_genome['@id'],
        {
            'taxa': 'Homo sapiens'
        }
    )
    curated_set_result = testapp.get(curated_set_genome['@id']).json
    assert curated_set_result.get('summary', '') == 'genome Homo sapiens GRCh38 hg19 GENCODE 40 GENCODE 41'
