import pytest


def test_measurement_set_upgrade_1_2(upgrader, measurement_set_v1):
    samples = measurement_set_v1['sample']
    donors = measurement_set_v1['donor']
    value = upgrader.upgrade('measurement_set', measurement_set_v1, current_version='1', target_version='2')
    assert 'sample' not in value
    assert samples == value['samples']
    assert 'donor' not in value
    assert donors == value['donors']
    assert value['schema_version'] == '2'


def test_measurement_set_upgrade_3_4(upgrader, measurement_set_v3):
    value = upgrader.upgrade('measurement_set', measurement_set_v3, current_version='3', target_version='4')
    assert 'protocol' not in value
    assert value['schema_version'] == '4'


def test_measurement_set_upgrade_4_5(upgrader, measurement_set_v4):
    value = upgrader.upgrade('measurement_set', measurement_set_v4, current_version='4', target_version='5')
    assert 'seqspec' not in value
    assert value['schema_version'] == '5'


def test_measurement_set_upgrade_5_6(upgrader, measurement_set_v5):
    value = upgrader.upgrade('measurement_set', measurement_set_v5, current_version='5', target_version='6')
    assert value['schema_version'] == '6'


def test_measurement_set_upgrade_6_7(upgrader, measurement_set_v6):
    value = upgrader.upgrade('measurement_set', measurement_set_v6, current_version='6', target_version='7')
    assert 'construct_libraries' not in value
    assert 'moi' not in value
    assert 'nucleic_acid_delivery' not in value
    assert value['schema_version'] == '7'


def test_measurement_set_upgrade_7_8(upgrader, measurement_set_v7_multiome):
    value = upgrader.upgrade('measurement_set', measurement_set_v7_multiome, current_version='7', target_version='8')
    assert value['schema_version'] == '8'
    assert type(value['multiome_size']) == int
    assert value['multiome_size'] == 2


def test_measurement_set_upgrade_8_9(upgrader, measurement_set_v8):
    sequencing_library_type = measurement_set_v8['sequencing_library_type']
    value = upgrader.upgrade('measurement_set', measurement_set_v8, current_version='8', target_version='9')
    assert 'sequencing_library_type' not in value
    assert 'sequencing_library_types' in value and value['sequencing_library_types'] == sequencing_library_type
    assert value['schema_version'] == '9'


def test_measurement_set_upgrade_9_10(upgrader, measurement_set_v9):
    value = upgrader.upgrade('measurement_set', measurement_set_v9, current_version='9', target_version='10')
    assert value['schema_version'] == '10'
    assert 'description' not in value


def test_measurement_set_upgrade_10_11(upgrader, measurement_set_v10):
    value = upgrader.upgrade('measurement_set', measurement_set_v10, current_version='10', target_version='11')
    assert 'file_set_type' in value
    assert value['file_set_type'] == 'experimental data'
    assert value['schema_version'] == '11'


def test_measurement_set_upgrade_11_12(upgrader, measurement_set_v11):
    value = upgrader.upgrade('measurement_set', measurement_set_v11, current_version='11', target_version='12')
    assert 'protocol' not in value
    assert 'protocols' in value
    assert value['protocols'] == ['https://www.protocols.io/test-protocols-url-12345']
    assert value['schema_version'] == '12'


def test_measurement_set_upgrade_12_13(upgrader, measurement_set_v12):
    value = upgrader.upgrade('measurement_set', measurement_set_v12, current_version='12', target_version='13')
    assert 'preferred_assay_title' in value
    assert value['preferred_assay_title'] == 'Parse SPLiT-seq'
    assert value['schema_version'] == '13'
    assert value['notes'] == 'Preferred_assay_titles enum Parse Split-seq has been renamed to be Parse SPLiT-seq.'


def test_measurement_set_upgrade_14_15(upgrader, measurement_set_v14):
    value = upgrader.upgrade('measurement_set', measurement_set_v14, current_version='14', target_version='15')
    assert 'protocols' not in value
    assert 'control_file_sets' not in value
    assert 'sequencing_library_types' not in value
    assert 'auxiliary_sets' not in value
    assert value['schema_version'] == '15'


def test_measurement_set_upgrade_15_16(upgrader, measurement_set_v15):
    other_samples = measurement_set_v15['samples'][1:]
    value = upgrader.upgrade(
        'measurement_set', measurement_set_v15,
        current_version='15', target_version='16')
    assert value['schema_version'] == '16'
    assert len(value['samples']) == 1
    for other_sample in other_samples:
        assert other_sample in value['notes']


def test_measurement_set_upgrade_16_17(upgrader, measurement_set_v16):
    value = upgrader.upgrade(
        'measurement_set', measurement_set_v16,
        current_version='16', target_version='17')
    assert value['schema_version'] == '17'
    assert 'readout' not in value
    assert 'notes' in value
    assert value['notes'].endswith('The readout /assay-terms/OBI_0001271/ was removed from this measurement set.')


def test_measurement_set_upgrade_17_18(upgrader, measurement_set_v17):
    value = upgrader.upgrade('measurement_set', measurement_set_v17, current_version='17', target_version='18')
    assert value['schema_version'] == '18'
    assert 'publication_identifiers' not in value


def test_measurement_set_upgrade_18_19(upgrader, measurement_set_v18):
    value = upgrader.upgrade('measurement_set', measurement_set_v18, current_version='18', target_version='19')
    assert value['schema_version'] == '19'
    assert 'library_construction_platform' not in value


def test_measurement_set_upgrade_19_20(upgrader, measurement_set_v19):
    value = upgrader.upgrade('measurement_set', measurement_set_v19, current_version='19', target_version='20')
    assert value['schema_version'] == '20'
    assert value.get('preferred_assay_title') == 'CRISPR FlowFISH screen'


def test_measurement_set_upgrade_20_21(upgrader, measurement_set_v20):
    value = upgrader.upgrade('measurement_set', measurement_set_v20, current_version='20', target_version='21')
    assert value['schema_version'] == '21'
    assert value.get('preferred_assay_title') == 'SUPERSTARR'


def test_measurement_set_upgrade_21_22(upgrader, measurement_set_v21):
    value = upgrader.upgrade('measurement_set', measurement_set_v21, current_version='21', target_version='22')
    assert value['schema_version'] == '22'
    assert value.get('preferred_assay_title') == 'Variant painting via fluorescence'


def test_measurement_set_upgrade_22_23(upgrader, measurement_set_v22):
    value = upgrader.upgrade('measurement_set', measurement_set_v22, current_version='22', target_version='23')
    assert value['schema_version'] == '23'
    assert value.get('preferred_assay_title') == 'Variant-EFFECTS'


def test_measurement_set_upgrade_23_24(upgrader, measurement_set_v23):
    value = upgrader.upgrade('measurement_set', measurement_set_v23, current_version='23', target_version='24')
    assert value['schema_version'] == '24'
    assert value.get('preferred_assay_title') == '10x multiome with scMito-seq'


def test_measurement_set_upgrade_24_25(upgrader, measurement_set_v24):
    value = upgrader.upgrade('measurement_set', measurement_set_v24, current_version='24', target_version='25')
    assert value['schema_version'] == '25'
    assert value.get('preferred_assay_title') == 'Proliferation CRISPR screen'


def test_measurement_set_upgrade_25_26_5_prime_to_3_prime(upgrader, measurement_set_v25_5_prime_to_3_prime):
    value = upgrader.upgrade('measurement_set', measurement_set_v25_5_prime_to_3_prime,
                             current_version='25', target_version='26')
    assert value['schema_version'] == '26'
    assert value.get('strand_specificity') == '5 prime to 3 prime'


def test_measurement_set_upgrade_25_26_3_prime_to_5_prime(upgrader, measurement_set_v25_3_prime_to_5_prime):
    value = upgrader.upgrade('measurement_set', measurement_set_v25_3_prime_to_5_prime,
                             current_version='25', target_version='26')
    assert value['schema_version'] == '26'
    assert value.get('strand_specificity') == '3 prime to 5 prime'


def test_measurement_set_upgrade_26_27(upgrader, measurement_set_v26):
    value = upgrader.upgrade('measurement_set', measurement_set_v26, current_version='26', target_version='27')
    assert value['schema_version'] == '27'
    assert value.get('control_type') == 'reference transduction'


def test_measurement_set_upgrade_27_28(upgrader, measurement_set_v27):
    value = upgrader.upgrade('measurement_set', measurement_set_v27, current_version='27', target_version='28')
    assert value['schema_version'] == '28'
    assert value.get('preferred_assay_title') == 'STARR-seq'


def test_measurement_set_upgrade_28_29(upgrader, measurement_set_v28):
    value = upgrader.upgrade('measurement_set', measurement_set_v28, current_version='28', target_version='29')
    assert value['schema_version'] == '29'
    assert value.get('preferred_assay_title') == 'mtscMultiome'


def test_measurement_set_upgrade_29_30(upgrader, measurement_set_v29):
    value = upgrader.upgrade('measurement_set', measurement_set_v29, current_version='29', target_version='30')
    assert value['schema_version'] == '30'
    assert value.get('preferred_assay_title') == 'Perturb-seq'


def test_measurement_set_upgrade_30_31(upgrader, measurement_set_v30):
    value = upgrader.upgrade('measurement_set', measurement_set_v30, current_version='30', target_version='31')
    assert 'preferred_assay_title' in value
    assert value['preferred_assay_title'] == 'Arrayed semi-qY2H v1'
    assert value['schema_version'] == '31'
    assert value['notes'] == 'Preferred_assay_title enum semi-qY2H has been renamed to be Arrayed semi-qY2H v1.'


def test_measurement_set_upgrade_31_32(upgrader, measurement_set_v31):
    value = upgrader.upgrade('measurement_set', measurement_set_v31, current_version='31', target_version='32')
    assert 'control_type' not in value
    assert value['schema_version'] == '32'
    assert value['notes'] == 'Control_type enum pre-selection was removed via upgrade.'


def test_measurement_set_upgrade_32_33(upgrader, measurement_set_v32):
    value = upgrader.upgrade('measurement_set', measurement_set_v32, current_version='32', target_version='33')
    assert 'control_type' not in value
    assert 'control_types' in value and value['control_types'] == ['pre-selection']
    assert value['schema_version'] == '33'


def test_measurement_set_upgrade_33_34(upgrader, measurement_set_v33):
    value = upgrader.upgrade('measurement_set', measurement_set_v33, current_version='33', target_version='34')
    assert 'preferred_assay_title' in value
    assert value['preferred_assay_title'] == '10x with Scale pre-indexing'
    assert value['schema_version'] == '34'
    assert value['notes'] == 'This measurement set previously used 10X ATAC with Scale pre-indexing as a preferred_assay_title, but the preferred_assay_title has been updated to 10x with Scale pre-indexing via an upgrade.'


def test_measurement_set_upgrade_35_36(upgrader, measurement_set_v35):
    preferred_assay_title = measurement_set_v35['preferred_assay_title']
    value = upgrader.upgrade('measurement_set', measurement_set_v35, current_version='35', target_version='36')
    assert 'preferred_assay_title' not in value
    assert 'preferred_assay_titles' in value and value['preferred_assay_titles'] == [(preferred_assay_title)]
    assert value['schema_version'] == '36'


def test_measurement_set_upgrade_36_37(upgrader, measurement_set_v36):
    value = upgrader.upgrade('measurement_set', measurement_set_v36, current_version='36', target_version='37')
    assert value['schema_version'] == '37'
    assert value.get('preferred_assay_titles') == ['CC-Perturb-seq']


def test_measurement_set_upgrade_37_38(upgrader, measurement_set_v37):
    value = upgrader.upgrade('measurement_set', measurement_set_v37, current_version='37', target_version='38')
    assert 'external_image_url' not in value
    assert 'external_image_urls' in value and value['external_image_urls'] == [
        'https://cellpainting-gallery.s3.amazonaws.com/index.html#cpg0011-lipocyteprofiler/broad/images/Batch5/images/BR00101116/']
    assert value['schema_version'] == '38'


def test_measurement_set_upgrade_38_39(upgrader, measurement_set_v38):
    value = upgrader.upgrade('measurement_set', measurement_set_v38, current_version='38', target_version='39')
    assert value['schema_version'] == '39'
    assert value.get('preferred_assay_titles') == ['10x snATAC-seq with Scale pre-indexing']
    assert value.get('notes') == 'This measurement set previously used 10x with Scale pre-indexing as a preferred_assay_titles, but it has been updated to 10x snATAC-seq with Scale pre-indexing via an upgrade.'
