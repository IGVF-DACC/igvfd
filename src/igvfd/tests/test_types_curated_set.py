import pytest


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
    assert {'GRCh38', 'hg19'} == set(curated_set_result.get('assemblies', []))


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
    assert {'GENCODE 40', 'GENCODE 41'} == set(curated_set_result.get('transcriptome_annotations', []))


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
    assert curated_set_result.get('summary', '') == 'Homo sapiens GRCh38 hg19 GENCODE 40 GENCODE 41 genome'
