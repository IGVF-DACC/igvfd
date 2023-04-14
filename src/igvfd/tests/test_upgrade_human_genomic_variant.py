import pytest


def test_human_genomic_variant_upgrade_1_2(upgrader, human_genomic_variant_v1):
    value = upgrader.upgrade('human_genomic_variant', human_genomic_variant_v1, current_version='1', target_version='2')
    assert value['refseq_id'] == 'NC_999999.00'
    assert value['notes'] == "This human genomic variant's `refseq_id` was originally NC_999999i00, but was changed to NC_999999.00 due to an upgrade in the regex pattern for the property."
    assert value['schema_version'] == '2'
