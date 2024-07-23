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
