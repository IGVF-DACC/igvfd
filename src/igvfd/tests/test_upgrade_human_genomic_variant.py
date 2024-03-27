import pytest


def test_human_genomic_variant_upgrade_1_2(upgrader, human_genomic_variant_v1):
    value = upgrader.upgrade('human_genomic_variant', human_genomic_variant_v1, current_version='1', target_version='2')
    assert value['refseq_id'] == 'NC_999999.00'
    assert value['notes'] == "This human genomic variant's `refseq_id` was originally NC_999999i00, but was changed to NC_999999.00 due to an upgrade in the regex pattern for the property."
    assert value['schema_version'] == '2'


def test_human_genomic_variant_upgrade_2_3(upgrader, human_genomic_variant_v2):
    value = upgrader.upgrade('human_genomic_variant', human_genomic_variant_v2, current_version='2', target_version='3')
    assert value['schema_version'] == '3'
    assert 'description' not in value


def test_human_genomic_variant_upgrade_4_5(upgrader, human_genomic_variant_v4a, human_genomic_variant_v4b):
    value = upgrader.upgrade('human_genomic_variant', human_genomic_variant_v4a,
                             current_version='4', target_version='5')
    assert value['schema_version'] == '5'
    assert 'associated_gwas' not in value
    value = upgrader.upgrade('human_genomic_variant', human_genomic_variant_v4b,
                             current_version='4', target_version='5')
    assert value['schema_version'] == '5'
    assert value['associated_gwas'] == ['GCST000510']
