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
    if value['sample_terms'] != ['/sample-terms/UBERON_0000468/']:
        old_term = str(value['sample_terms'][0])
        notes += f' Biosample_term (formerly: {old_term}) was automatically upgraded.'
        value['sample_terms'] = ['/sample-terms/UBERON_0000468/']
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
def in_vitro_system_9_10(value, system):
    # https://igvf.atlassian.net/browse/IGVF-627
    # This upgrade was done manually, see the ticket above.
    return


@upgrade_step('primary_cell', '12', '13')
@upgrade_step('in_vitro_system', '10', '11')
@upgrade_step('tissue', '12', '13')
@upgrade_step('technical_sample', '6', '7')
@upgrade_step('whole_organism', '13', '14')
def sample_12_13(value, system):
    # https://igvf.atlassian.net/browse/IGVF-726
    # This upgrade is to update previous data with
    # default value for 'virtual' property.
    # The default value will be automatically populated.
    return


@upgrade_step('in_vitro_system', '11', '12')
def in_vitro_system_11_12(value, system):
    # https://igvf.atlassian.net/browse/IGVF-844
    if 'introduced_factors' in value:
        value['cell_fate_change_treatments'] = value['introduced_factors']
        del value['introduced_factors']
    if 'time_post_factors_introduction' in value:
        value['time_post_change'] = value['time_post_factors_introduction']
        del value['time_post_factors_introduction']
    if 'time_post_factors_introduction_units' in value:
        value['time_post_change_units'] = value['time_post_factors_introduction_units']
        del value['time_post_factors_introduction_units']


@upgrade_step('whole_organism', '14', '15')
def whole_organism_14_15(value, system):
    # https://igvf.atlassian.net/browse/IGVF-753
    if 'part_of' in value:
        del value['part_of']
    if 'pooled_from' in value:
        del value['pooled_from']


@upgrade_step('whole_organism', '15', '16')
def whole_organism_15_16(value, system):
    # https://igvf.atlassian.net/browse/IGVF-802
    if 'references' in value:
        value['publication_identifiers'] = value['references']
        del value['references']


@upgrade_step('multiplexed_sample', '1', '2')
def multiplexed_sample_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-872
    notes = value.get('notes', '')
    if 'source' in value:
        notes += f" Source {value['source']} was removed via upgrade."
        value.pop('source')
    if 'product_id' in value:
        notes += f" Product ID {value['product_id']} was removed via upgrade."
        value.pop('product_id')
    if 'lot_id' in value:
        notes += f" Lot ID {value['lot_id']} was removed via upgrade."
        value.pop('lot_id')
    value['notes'] = notes.strip()


@upgrade_step('primary_cell', '13', '14')
@upgrade_step('in_vitro_system', '12', '13')
@upgrade_step('tissue', '13', '14')
@upgrade_step('technical_sample', '7', '8')
@upgrade_step('whole_organism', '16', '17')
def sample_13_14(value, system):
    # https://igvf.atlassian.net/browse/IGVF-895
    # Three properties are renamed and pluralized in this upgrade
    if 'source' in value:
        value['sources'] = [value['source']]
        del value['source']
    if 'modification' in value:
        value['modifications'] = [value['modification']]
        del value['modification']
    if 'biosample_term' in value:
        value['sample_terms'] = [value['biosample_term']]
        del value['biosample_term']
    if 'technical_sample_term' in value:
        value['sample_terms'] = [value['technical_sample_term']]
        del value['technical_sample_term']


@upgrade_step('multiplexed_sample', '2', '3')
def multiplexed_sample_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-895
    # Biosample_terms is renamed to sample_terms
    # The property is calculated so the upgrade is solely to flag the change
    return


@upgrade_step('primary_cell', '14', '15')
@upgrade_step('in_vitro_system', '13', '14')
@upgrade_step('tissue', '14', '15')
@upgrade_step('technical_sample', '8', '9')
@upgrade_step('whole_organism', '17', '18')
@upgrade_step('multiplexed_sample', '3', '4')
def sample_14_15(value, system):
    # https://igvf.atlassian.net/browse/IGVF-949
    notes = value.get('notes', '')
    if 'starting_amount' in value and 'starting_amount_units' not in value:
        value['starting_amount_units'] = 'items'
        notes += f' This sample has been upgraded to have starting_amount_units as "items" since there was no entry. Please update with the appropriate value for starting_amount_units.'
    elif 'starting_amount_units' in value and 'starting_amount' not in value:
        value['starting_amount'] = 0
        notes += f' This sample has been upgraded to have a starting_amount of 0 since there was no entry. Please update with the appropriate value for starting_amount.'
    if 'pmi' in value and 'pmi_units' not in value:
        value['pmi_units'] = 'second'
        notes += f' This sample has been upgraded to have pmi_units as "second" since there was no entry. Please update with the appropriate value for pmi_units.'
    elif 'pmi_units' in value and 'pmi' not in value:
        value['pmi'] = 1
        notes += f' This sample has been upgraded to have a pmi of 1 since there was no entry. Please update with the appropriate value for pmi.'
    value['notes'] = notes.strip()
