import pytest


def test_construct_library_set_upgrade_1_2(upgrader, construct_library_set_v1):
    value = upgrader.upgrade('construct_library_set', construct_library_set_v1, current_version='1', target_version='2')
    assert value['exon'] == 'exon_ID'
    assert value['schema_version'] == '2'


def test_construct_library_set_upgrade_2_3(upgrader, construct_library_set_v2):
    value = upgrader.upgrade('construct_library_set', construct_library_set_v2, current_version='2', target_version='3')
    assert 'description' not in value
    assert value['schema_version'] == '3'


def test_construct_library_set_upgrade_3_4(upgrader, construct_library_set_v3):
    value = upgrader.upgrade('construct_library_set', construct_library_set_v3, current_version='3', target_version='4')
    assert value['schema_version'] == '4'


def test_construct_library_set_upgrade_4_5(upgrader, construct_library_set_v4):
    genes = construct_library_set_v4['genes']
    value = upgrader.upgrade('construct_library_set', construct_library_set_v4, current_version='4', target_version='5')
    assert 'genes' not in value and value['small_scale_gene_list'] == genes
    assert value['schema_version'] == '5'


def test_construct_library_set_upgrade_5_6(upgrader, construct_library_set_v5):
    value = upgrader.upgrade('construct_library_set', construct_library_set_v5, current_version='5', target_version='6')
    for loci in value['small_scale_loci_list']:
        assert loci['assembly'] == 'GRCh38'
    assert value['schema_version'] == '6'


def test_construct_library_set_upgrade_7_8(upgrader, construct_library_set_v7):
    value = upgrader.upgrade('construct_library_set', construct_library_set_v7, current_version='7', target_version='8')
    assert value['schema_version'] == '8'


def test_construct_library_set_upgrade_8_9(upgrader, construct_library_set_v8):
    value = upgrader.upgrade('construct_library_set', construct_library_set_v8, current_version='8', target_version='9')
    assert value['schema_version'] == '9'
    assert 'publication_identifiers' not in value


def test_construct_library_set_upgrade_9_10(upgrader, construct_library_set_v9, sequence_file, tabular_file, reference_file):
    value = upgrader.upgrade('construct_library_set', construct_library_set_v9,
                             current_version='9', target_version='10')
    assert value['schema_version'] == '10'
    assert sequence_file['@id'] not in value['integrated_content_files']
    assert tabular_file['@id'] in value['integrated_content_files'] and reference_file['@id'] in value['integrated_content_files']
    # print out something to check what's the format of value['integrated_content_files']
