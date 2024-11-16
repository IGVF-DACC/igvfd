import pytest


def test_genome_browser_annotation_file_upgrade_1_2(upgrader, genome_browser_annotation_file_v1):
    value = upgrader.upgrade('genome_browser_annotation_file', genome_browser_annotation_file_v1,
                             current_version='1', target_version='2')
    assert 'dbxrefs' not in value
    assert value['schema_version'] == '2'


def test_genome_browser_annotation_file_upgrade_2_3(upgrader, genome_browser_annotation_file_v2):
    value = upgrader.upgrade('genome_browser_annotation_file', genome_browser_annotation_file_v2,
                             current_version='2', target_version='3')
    assert 'description' not in value
    assert value['schema_version'] == '3'


def test_genome_browser_annotation_file_upgrade_3_4(upgrader, genome_browser_annotation_file_v3):
    value = upgrader.upgrade('genome_browser_annotation_file', genome_browser_annotation_file_v3,
                             current_version='3', target_version='4')
    assert value['upload_status'] == 'invalidated'
    assert value['schema_version'] == '4'


def test_genome_browser_annotation_file_upgrade_4_5(upgrader, genome_browser_annotation_file_v4):
    value = upgrader.upgrade('genome_browser_annotation_file', genome_browser_annotation_file_v4,
                             current_version='4', target_version='5')
    assert 'assembly' in value
    assert value['assembly'] == 'GRCh38'
    assert value['schema_version'] == '5'


def test_genome_browser_annotation_file_upgrade_5_6(upgrader, genome_browser_annotation_file_v5):
    value = upgrader.upgrade('genome_browser_annotation_file', genome_browser_annotation_file_v5,
                             current_version='5', target_version='6')
    assert value['assembly'] == 'GRCh38'
    assert value['schema_version'] == '6'


def test_genome_browser_annotation_file_upgrade_7_8(upgrader, genome_browser_annotation_file_v7):
    value = upgrader.upgrade('genome_browser_annotation_file', genome_browser_annotation_file_v7,
                             current_version='7', target_version='8')
    assert 'derived_from' not in value
    assert 'file_format_specifications' not in value
    assert value['schema_version'] == '8'


def test_genome_browser_annotation_file_upgrade_8_9(upgrader, genome_browser_annotation_file_v8):
    value = upgrader.upgrade('genome_browser_annotation_file', genome_browser_annotation_file_v8,
                             current_version='8', target_version='9')
    assert genome_browser_annotation_file_v8['file_format'] == 'bigBed'
    assert genome_browser_annotation_file_v8['notes'].endswith('but has been upgraded to .bigBed')
    assert genome_browser_annotation_file_v8['version'] == '9'
