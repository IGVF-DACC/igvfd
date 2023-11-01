import pytest


def test_genome_browser_annotation_file_upgrade_1_2(upgrader, genome_browser_annotation_file_v1):
    value = upgrader.upgrade('genome_browser_annotation_file', genome_browser_annotation_file_v1,
                             current_version='1', target_version='2')
    assert 'dbxrefs' not in value
    assert value['schema_version'] == '2'
