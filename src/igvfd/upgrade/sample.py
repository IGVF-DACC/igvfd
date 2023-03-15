from snovault import upgrade_step


@upgrade_step('primary_cell', '1', '2')
@upgrade_step('tissue', '1', '2')
@upgrade_step('whole_organism', '1', '2')
def sample_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-207
    return


@upgrade_step('primary_cell', '2', '3')
@upgrade_step('tissue', '2', '3')
def sample_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-210
    return


@upgrade_step('primary_cell', '3', '4')
@upgrade_step('tissue', '3', '4')
@upgrade_step('whole_organism', '2', '3')
@upgrade_step('technical_sample', '1', '2')
def sample_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-221
    if 'treatments' in value:
        if len(value['treatments']) == 0:
            del value['treatments']
    if 'donors' in value:
        if len(value['donors']) == 0:
            del value['donors']
    if 'dbxrefs' in value:
        if len(value['dbxrefs']) == 0:
            del value['dbxrefs']
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']
    if 'collections' in value:
        if len(value['collections']) == 0:
            del value['collections']
    if 'alternate_accessions' in value:
        if len(value['alternate_accessions']) == 0:
            del value['alternate_accessions']
    if 'differentiation_treatments' in value:
        if len(value['differentiation_treatments']) == 0:
            del value['differentiation_treatments']


@upgrade_step('technical_sample', '2', '3')
def technical_sample_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-238
    if 'additional_description' in value:
        value['description'] = value['additional_description']
        del value['additional_description']


@upgrade_step('primary_cell', '4', '5')
@upgrade_step('tissue', '4', '5')
@upgrade_step('whole_organism', '3', '4')
def sample_4_5(value, system):
    # https://igvf.atlassian.net/browse/IGVF-187
    if 'disease_term' in value:
        value['disease_terms'] = [value['disease_term']]
        value.pop('disease_term')


@upgrade_step('primary_cell', '5', '6')
@upgrade_step('tissue', '5', '6')
@upgrade_step('whole_organism', '4', '5')
def sample_5_6(value, system):
    # https://igvf.atlassian.net/browse/IGVF-249
    # https://igvf.atlassian.net/browse/IGVF-243
    if 'age' in value:
        age = value['age']
        del value['age']
        if age != 'unknown':
            if age == '90 or above':
                value['lower_bound_age'] = 90
                value['upper_bound_age'] = 90
            else:
                value['lower_bound_age'] = int(age)
                value['upper_bound_age'] = int(age)
    if 'life_stage' in value:
        if value['life_stage'] == 'embryonic':
            value['embryonic'] = True
        del value['life_stage']
    return


@upgrade_step('technical_sample', '3', '4')
def technical_sample_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-264
    return


@upgrade_step('primary_cell', '6', '7')
@upgrade_step('tissue', '6', '7')
@upgrade_step('whole_organism', '5', '6')
@upgrade_step('in_vitro_system', '1', '2')
def sample_7_8(value, system):
    # https://igvf.atlassian.net/browse/IGVF-387
    if 'donor' in value:
        value['donors'] = value['donor']
        value.pop('donor')


@upgrade_step('primary_cell', '7', '8')
@upgrade_step('tissue', '7', '8')
@upgrade_step('whole_organism', '6', '7')
@upgrade_step('in_vitro_system', '2', '3')
def sample_8_9(value, system):
    # https://igvf.atlassian.net/browse/IGVF-321
    if 'biomarker' in value:
        value['biomarkers'] = value['biomarker']
        del value['biomarker']


@upgrade_step('primary_cell', '8', '9')
@upgrade_step('tissue', '8', '9')
@upgrade_step('whole_organism', '7', '8')
@upgrade_step('in_vitro_system', '3', '4')
@upgrade_step('technical_sample', '4', '5')
def sample_9_10(value, system):
    # https://igvf.atlassian.net/browse/IGVF-398
    if 'accession' in value:
        accession_prefix = value['accession'][0:6]
        accession_suffix = value['accession'][6:]
        value['accession'] = f'{accession_prefix}0{accession_suffix}A'


@upgrade_step('primary_cell', '9', '10')
@upgrade_step('tissue', '9', '10')
@upgrade_step('whole_organism', '8', '9')
@upgrade_step('in_vitro_system', '5', '6')
@upgrade_step('technical_sample', '5', '6')
def sample_10_11(value, system):
    # https://igvf.atlassian.net/browse/IGVF-486
    if value['sorted_fraction']:
        value['sorted_fraction_detail'] = 'Default upgrade text: please add more details about sorted_fraction, see sample.json for description.'
