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


@upgrade_step('in_vitro_system', '4', '5')
def in_vitro_system_4_5(value, system):
    # https://igvf.atlassian.net/browse/IGVF-471
    if value['classification'] == 'differentiated tissue':
        value['classification'] = 'organoid'


@upgrade_step('primary_cell', '9', '10')
@upgrade_step('tissue', '9', '10')
@upgrade_step('whole_organism', '8', '9')
@upgrade_step('in_vitro_system', '5', '6')
@upgrade_step('technical_sample', '5', '6')
def sample_10_11(value, system):
    # https://igvf.atlassian.net/browse/IGVF-486
    if 'sorted_fraction' in value:
        value['sorted_fraction_detail'] = 'Default upgrade text: please add more details about sorted_fraction, see sample.json for description.'


@upgrade_step('primary_cell', '10', '11')
@upgrade_step('tissue', '10', '11')
@upgrade_step('whole_organism', '9', '10')
@upgrade_step('in_vitro_system', '6', '7')
def biosample_6_7(value, system):
    # https://igvf.atlassian.net/browse/IGVF-511
    if 'notes' in value:
        new_notes_value = value.get('notes')
        if len(new_notes_value) > 0:
            new_notes_value += '  '
    if 'taxa' in value:
        if value['taxa'] == 'Saccharomyces':
            value['notes'] = new_notes_value + 'Previous taxa: ' + value['taxa'] + ' is no longer valid.'
            value['taxa'] = 'Mus musculus'


@upgrade_step('in_vitro_system', '7', '8')
def in_vitro_system_7_8(value, system):
    if value['classification'] == 'differentiated cell':
        value['classification'] = 'differentiated cell specimen'
    if value['classification'] == 'reprogrammed cell':
        value['classification'] = 'reprogrammed cell specimen'


@upgrade_step('whole_organism', '10', '11')
def whole_organism_10_11(value, system):
    # https://igvf.atlassian.net/browse/IGVF-575
    notes = value.get('notes', '')
    if 'part_of' in value:
        part_id = value['part_of']
        notes += f' Part_of property (previous content: {part_id}) is no longer valid.'
        del value['part_of']
    if 'pooled_from' in value:
        pool_ids = []
        for sample in value['pooled_from']:
            pool_ids.append(sample)
        pool_list = ', '.join(pool_ids)
        notes += f' Pooled_from property (previous content: {pool_list}) is no longer valid.'
        del value['pooled_from']
    new_notes = notes.strip()
    value['notes'] = new_notes


@upgrade_step('whole_organism', '11', '12')
def whole_organism_11_12(value, system):
    # https://igvf.atlassian.net/browse/IGVF-577
    notes = value.get('notes', '')
    if value['biosample_term'] != '/sample-terms/UBERON_0000468/':
        old_term = value['biosample_term']
        notes += f' Biosample_term (formerly: {old_term}) was automatically upgraded.'
        value['biosample_term'] = '/sample-terms/UBERON_0000468/'
        value['notes'] = notes.strip()


@upgrade_step('primary_cell', '11', '12')
@upgrade_step('tissue', '11', '12')
@upgrade_step('whole_organism', '12', '13')
@upgrade_step('in_vitro_system', '8', '9')
def biosample_7_8(value, system):
    # https://igvf.atlassian.net/browse/IGVF-586
    if 'taxa' in value:
        if 'notes' in value:
            notes_value = value['notes']
            if notes_value:
                notes_value += '  '
            value['notes'] = notes_value + 'Previous taxa: ' + value['taxa'] + ' will now be calculated.'
        else:
            value['notes'] = 'Previous taxa: ' + value['taxa'] + ' will now be calculated.'
        del value['taxa']


@upgrade_step('in_vitro_system', '9', '10')
def in_vitro_system_8_9(value, system):
    # https://igvf.atlassian.net/browse/IGVF-627
    notes = value.get('notes', '')
    # if value['classification'] in ['organoid', 'differentiated cell specimen', 'reprogrammed cell specimen']:
    #
    # else:
    if 'time_post_factors_introduction' in value and 'time_post_factors_introduction_units' in value and 'introduced_factors' not in value:
        time_post_factors_introduction = value['time_post_factors_introduction']
        time_post_factors_introduction_units = value['time_post_factors_introduction_units']
        del value['time_post_factors_introduction']
        del value['time_post_factors_introduction_units']
        notes += f' This sample originally had time_post_factors_introduction of {time_post_factors_introduction} and time_post_factors_introduction_units of {time_post_factors_introduction_units}, but no associated introduced_factors. All three properties are now mutually required for in_vitro_system samples and should be submitted together.'
    if 'introduced_factors' in value and 'time_post_factors_introduction' not in value and 'time_post_factors_introduction_units' not in value:
        introduced_factors = value['introduced_factors']
        del value['introduced_factors']
        notes += f' This sample originally had introduced_factors of {introduced_factors}, but no associated time_post_factors_introduction or time_post_factors_introduction_units. All three properties are now mutually required for in_vitro_system samples and should be submitted together.'
    new_notes = notes.strip()
    value['notes'] = new_notes
