from snovault import upgrade_step


@upgrade_step('cell_line', '1', '2')
@upgrade_step('differentiated_cell', '1', '2')
@upgrade_step('differentiated_tissue', '1', '2')
@upgrade_step('primary_cell', '1', '2')
@upgrade_step('tissue', '1', '2')
@upgrade_step('whole_organism', '1', '2')
def sample_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-207
    return


@upgrade_step('cell_line', '2', '3')
@upgrade_step('differentiated_cell', '2', '3')
@upgrade_step('differentiated_tissue', '2', '3')
@upgrade_step('primary_cell', '2', '3')
@upgrade_step('tissue', '2', '3')
def sample_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-210
    return


@upgrade_step('cell_line', '3', '4')
@upgrade_step('differentiated_cell', '3', '4')
@upgrade_step('differentiated_tissue', '3', '4')
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


@upgrade_step('cell_line', '4', '5')
@upgrade_step('differentiated_cell', '4', '5')
@upgrade_step('differentiated_tissue', '4', '5')
@upgrade_step('primary_cell', '4', '5')
@upgrade_step('tissue', '4', '5')
@upgrade_step('whole_organism', '3', '4')
def sample_4_5(value, system):
    # https://igvf.atlassian.net/browse/IGVF-187
    if 'disease_term' in value:
        value['disease_terms'] = [value['disease_term']]
        value.pop('disease_term')


@upgrade_step('cell_line', '5', '6')
@upgrade_step('differentiated_cell', '5', '6')
@upgrade_step('differentiated_tissue', '5', '6')
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


@upgrade_step('differentiated_cell', '6', '7')
@upgrade_step('differentiated_tissue', '6', '7')
def differentiated_sample_6_7(value, system):
    # https://igvf.atlassian.net/browse/IGVF-239
    if value.get('post_differentiation_time_units') == 'stage':
        old_diff_time = value['post_differentiation_time']
        old_notes_value = ''
        if value.get('notes'):
            old_notes_value = value.get('notes') + '  '
        value['notes'] = old_notes_value + \
            f'post_differentiation_time: {old_diff_time}, post_differentiation_time_units: stage.'
        del value['post_differentiation_time_units']
        del value['post_differentiation_time']


@upgrade_step('technical_sample', '3', '4')
def technical_sample_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-264
    return


@upgrade_step('cell_line', '6', '7')
@upgrade_step('tissue', '6', '7')
@upgrade_step('primary_cell', '6', '7')
@upgrade_step('differentiated_cell', '7', '8')
@upgrade_step('differentiated_tissue', '7', '8')
@upgrade_step('whole_organism', '5', '6')
@upgrade_step('technical_sample', '4', '5')
@upgrade_step('in_vitro_system', '1', '2')
def sample_7_8(value, system):
    # https://igvf.atlassian.net/browse/IGVF-321
    if 'aliases' in value:
        value['alias'] = value['aliases']
        del value['aliases']
    if 'alternate_accessions' in value:
        value['alternate_accession'] = value['alternate_accessions']
        del value['alternate_accessions']
    if 'collections' in value:
        value['collection'] = value['collections']
        del value['collections']
    if 'documents' in value:
        value['document'] = value['documents']
        del value['documents']
    if 'treatments' in value:
        value['treatment'] = value['treatments']
        del value['treatments']
    if 'disease_terms' in value:
        value['disease_term'] = value['disease_terms']
        del value['disease_terms']
    if 'differentiation_treatments' in value:
        value['differentiation_treatment'] = value['differentiation_treatments']
        del value['differentiation_treatment']
    if 'dbxrefs' in value:
        value['dbxref'] = value['dbxrefs']
        del value['dbxrefs']
    if 'references' in value:
        value['reference'] = value['references']
        del value['references']
    if 'introduced_factors' in value:
        value['introduced_factor'] = value['introduced_factors']
        del value['introduced_factors']
    if 'part_of' in value:
        old_part_of_value = value['part_of']
        value['part_of'] = [old_part_of_value]
    if 'originated_from' in value:
        old_originated_from_value = value['originated_from']
        value['originated_from'] = [old_originated_from_value]
