import pytest


def test_reference_file_upgrade_2_3(upgrader, reference_file_v2):
    source = reference_file_v2['source']
    value = upgrader.upgrade('reference_file', reference_file_v2, current_version='2', target_version='3')
    assert source == value['source_url']
    assert 'source' not in value
    assert 'source_url' in value
    assert value['schema_version'] == '3'


def test_ref_file_upgrade_3_4(upgrader, ref_file_v3):
    ori_ann = ref_file_v3['transcriptome_annotation']
    if ori_ann.startswith('V'):
        ori_ann = ori_ann.split('V')[1]
    match_ann = 'GENCODE ' + ori_ann
    value = upgrader.upgrade('reference_file', ref_file_v3, current_version='3', target_version='4')
    assert match_ann == value['transcriptome_annotation']
    assert 'transcriptome_annotation' in value
    assert value['schema_version'] == '4'


def test_reference_file_upgrade_4_5(upgrader, reference_file_v4):
    value = upgrader.upgrade('reference_file', reference_file_v4, current_version='4', target_version='5')
    assert value['schema_version'] == '5'
    assert 'file_format_type' in value
    assert value['file_format_type'] == 'bed9+'
