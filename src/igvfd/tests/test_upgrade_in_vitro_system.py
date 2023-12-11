import pytest


def test_in_vitro_system_upgrade_1_2(upgrader, in_vitro_system_v1):
    assert 'donor' in in_vitro_system_v1
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v1, current_version='1', target_version='2')
    assert 'donor' not in value
    assert 'donors' in value
    assert value['schema_version'] == '2'


def test_in_vitro_system_upgrade_2_3(upgrader, in_vitro_system_v2):
    biomarkers = in_vitro_system_v2['biomarker']
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v2, current_version='2', target_version='3')
    assert 'biomarker' not in value
    assert biomarkers == value['biomarkers']
    assert value['schema_version'] == '3'


def test_in_vitro_system_upgrade_3_4(upgrader, in_vitro_system_v3):
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v3, current_version='3', target_version='4')
    assert value['accession'] == 'IGVFSM0222IIVA'
    assert value['schema_version'] == '4'


def test_in_vitro_system_upgrade_4_5(upgrader, in_vitro_system_v4):
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v4, current_version='4', target_version='5')
    assert value['schema_version'] == '5'
    assert value.get('classification') == 'organoid'


def test_in_vitro_system_upgrade_5_6(upgrader, in_vitro_system_v5):
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v5, current_version='5', target_version='6')
    assert value['schema_version'] == '6'
    assert value['sorted_fraction_detail'] == 'Default upgrade text: please add more details about sorted_fraction, see sample.json for description.'


def test_in_vitro_system_upgrade_6_7(upgrader, in_vitro_system_v6):
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v6, current_version='6', target_version='7')
    assert value['schema_version'] == '7'
    assert value['taxa'] != 'Saccharomyces'
    assert value['notes'] == 'Previous taxa: Saccharomyces is no longer valid.'


def test_in_vitro_system_upgrade_7_8(upgrader, in_vitro_system_v7):
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v7, current_version='7', target_version='8')
    assert value['schema_version'] == '8'
    assert value['classification'] == 'differentiated cell specimen'


def test_in_vitro_system_upgrade_8_9(upgrader, in_vitro_system_v8):
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v8, current_version='8', target_version='9')
    assert value['schema_version'] == '9'
    assert 'taxa' not in value
    assert value['notes'] == 'Test.  Previous taxa: Homo sapiens will now be calculated.'


def test_in_vitro_system_upgrade_9_10(upgrader, in_vitro_system_v9):
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v9, current_version='9', target_version='10')
    assert value['schema_version'] == '10'


def test_in_vitro_system_upgrade_10_11(upgrader, in_vitro_system_v10):
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v10, current_version='10', target_version='11')
    assert value['schema_version'] == '11'
    assert value['virtual'] == False


def test_in_vitro_system_upgrade_11_12(upgrader, in_vitro_system_v11, treatment_chemical):
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v11, current_version='11', target_version='12')
    assert value['schema_version'] == '12'
    assert 'introduced_factors' not in value
    assert [treatment_chemical['@id']] == value['cell_fate_change_treatments']
    assert 'time_post_factors_introduction' not in value
    assert value['time_post_change'] == 10
    assert 'time_post_factors_introduction_units' not in value
    assert value['time_post_change_units'] == 'minute'


def test_in_vitro_system_upgrade_12_13(upgrader, in_vitro_system_v12):
    sources = [in_vitro_system_v12['source']]
    sample_terms = [in_vitro_system_v12['biosample_term']]
    modifications = [in_vitro_system_v12['modification']]
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v12, current_version='12', target_version='13')
    assert 'source' not in value
    assert sources == value['sources']
    assert type(value['sources']) == list
    assert 'biosample_term' not in value
    assert sample_terms == value['sample_terms']
    assert type(value['sample_terms']) == list
    assert 'modification' not in value
    assert modifications == value['modifications']
    assert type(value['modifications']) == list
    assert value['schema_version'] == '13'


def test_in_vitro_system_upgrade_13_14(upgrader, in_vitro_system_v13_no_units, in_vitro_system_v13_no_amount):
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v13_no_units, current_version='13', target_version='14')
    assert 'starting_amount_units' in value and value['starting_amount_units'] == 'items'
    assert value['schema_version'] == '14'
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v13_no_amount,
                             current_version='13', target_version='14')
    assert 'starting_amount' in value and value['starting_amount'] == 0
    assert value['schema_version'] == '14'


def test_in_vitro_system_upgrade_14_15(upgrader, in_vitro_system_v14):
    sorted_sample = in_vitro_system_v14['sorted_fraction']
    sorted_sample_detail = in_vitro_system_v14['sorted_fraction_detail']
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v14, current_version='14', target_version='15')
    assert 'sorted_from' in value and value['sorted_from'] == sorted_sample
    assert 'sorted_from_detail' in value and value['sorted_from_detail'] == sorted_sample_detail
    assert value['schema_version'] == '15'


def test_in_vitro_system_upgrade_15_16(upgrader, in_vitro_system_v15):
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v15, current_version='15', target_version='16')
    assert value['schema_version'] == '16'
    assert 'description' not in value


def test_in_vitro_system_upgrade_16_17(upgrader, in_vitro_system_v16):
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v16, current_version='16', target_version='17')
    assert value['schema_version'] == '17'


def test_in_vitro_system_upgrade_17_18(
    upgrader,
    in_vitro_system_v17,
    treatment_protein,
    sample_term_endothelial_cell
):
    value = upgrader.upgrade('in_vitro_system', in_vitro_system_v17, current_version='17', target_version='18')
    assert 'cell_fate_change_treatments' not in value
    assert 'time_post_change' not in value
    assert 'time_post_change_units' not in value
    assert 'targeted_sample_term' not in value
    assert value['schema_version'] == '18'
    assert 'notes' in value
    assert value['notes'] == (
        f'The following properties were removed in an upgrade because '
        f'they are invalid for a "cell line" in vitro system: '
        f'cell_fate_change_treatments: [\'{treatment_protein["@id"]}\']; '
        f'targeted_sample_term: {sample_term_endothelial_cell["@id"]}; '
        f'time_post_change: 10; time_post_change_units: day.'
    )
