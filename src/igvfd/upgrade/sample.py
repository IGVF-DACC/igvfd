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
    if notes.strip():
        value['notes'] = notes.strip()


@upgrade_step('primary_cell', '15', '16')
@upgrade_step('in_vitro_system', '14', '15')
@upgrade_step('tissue', '15', '16')
@upgrade_step('technical_sample', '9', '10')
@upgrade_step('whole_organism', '18', '19')
@upgrade_step('multiplexed_sample', '4', '5')
def sample_15_16(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1199
    if 'sorted_fraction' in value:
        value['sorted_from'] = value['sorted_fraction']
        del value['sorted_fraction']
    if 'sorted_fraction_detail' in value:
        value['sorted_from_detail'] = value['sorted_fraction_detail']
        del value['sorted_fraction_detail']


@upgrade_step('primary_cell', '16', '17')
@upgrade_step('in_vitro_system', '15', '16')
@upgrade_step('tissue', '16', '17')
@upgrade_step('technical_sample', '10', '11')
@upgrade_step('whole_organism', '19', '20')
@upgrade_step('multiplexed_sample', '5', '6')
def sample_16_17(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1170
    if 'description' in value:
        if value['description'] == '':
            del value['description']


@upgrade_step('in_vitro_system', '16', '17')
def in_vitro_system_16_17(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1291
    # Restrict cell_fate_change_treatments to admin only.
    return


@upgrade_step('in_vitro_system', '17', '18')
def in_vitro_system_17_18(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1323
    # Prevent "cell line" in vitro systems from specifying
    # cell fate change related properties.
    cell_fate_change_properties = [
        'cell_fate_change_protocol',
        'cell_fate_change_treatments',
        'targeted_sample_term',
        'time_post_change',
        'time_post_change_units'
    ]
    removed_metadata = {}
    if value['classification'] == 'cell line' and \
            any(p in value for p in cell_fate_change_properties):
        for p in cell_fate_change_properties:
            if p in value:
                removed_metadata[p] = value[p]
                del value[p]
    if removed_metadata:
        key_val_to_str = []
        for k in sorted(removed_metadata.keys()):
            key_val_to_str.append(f'{k}: {removed_metadata[k]}')
        notes = value.get('notes', '')
        notes += (
            f' The following properties were removed in an upgrade '
            f'because they are invalid for a "cell line" in vitro '
            f'system: {"; ".join(key_val_to_str)}.'
        )
        value['notes'] = notes.strip()


@upgrade_step('in_vitro_system', '18', '19')
def in_vitro_system_18_19(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1394
    value['classifications'] = [value['classification']]
    del value['classification']
    notes = value.get('notes', '')
    notes += (
        f' The "classification" of this in vitro system was '
        f'moved into the array property "classifications." '
    )
    value['notes'] = notes.strip()


@upgrade_step('primary_cell', '17', '18')
@upgrade_step('in_vitro_system', '19', '20')
@upgrade_step('tissue', '17', '18')
@upgrade_step('technical_sample', '11', '12')
@upgrade_step('whole_organism', '20', '21')
@upgrade_step('multiplexed_sample', '6', '7')
def sample_17_18(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1494
    if value['status'] in ['released', 'archived', 'revoked'] and 'release_timestamp' not in value:
        value['release_timestamp'] = '2024-03-06T12:34:56Z'
        notes = value.get('notes', '')
        notes += f'This object\'s release_timestamp has been set to 2024-03-06T12:34:56Z'
        value['notes'] = notes.strip()


@upgrade_step('primary_cell', '18', '19')
@upgrade_step('in_vitro_system', '20', '21')
@upgrade_step('tissue', '18', '19')
@upgrade_step('whole_organism', '21', '22')
def sample_18_19(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1684
    if 'nih_institutional_certification' in value:
        old_nic = value.get('nih_institutional_certification')
        notes = f'This biosample previously specified {old_nic} as its NIC, but this property has been moved to the institutional certification object. Please submit there instead to specify certification.'
        old_notes = value.get('notes', '')
        if old_notes:
            notes = f'{old_notes} {notes}'
        value['notes'] = notes
        del value['nih_institutional_certification']


@upgrade_step('primary_cell', '19', '20')
@upgrade_step('in_vitro_system', '21', '22')
@upgrade_step('tissue', '19', '20')
@upgrade_step('technical_sample', '12', '13')
@upgrade_step('whole_organism', '22', '23')
def sample_19_20(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1803
    if 'product_id' in value and 'sources' not in value:
        notes = value.get('notes', '')
        prod_id = value['product_id']
        notes += f' Product_id {prod_id} was removed from this sample.'
        del value['product_id']
        if 'lot_id' in value:
            lot_id = value.get('lot_id', '')
            notes += f' Lot_id {lot_id} was removed from this sample.'
            del value['lot_id']
        value['notes'] = notes.strip()


@upgrade_step('technical_sample', '13', '14')
@upgrade_step('multiplexed_sample', '7', '8')
@upgrade_step('primary_cell', '20', '21')
@upgrade_step('in_vitro_system', '22', '23')
@upgrade_step('tissue', '20', '21')
@upgrade_step('whole_organism', '23', '24')
def sample_20_21(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1789
    if 'publication_identifiers' in value:
        del value['publication_identifiers']


@upgrade_step('multiplexed_sample', '8', '9')
def multiplexed_sample_8_9(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1886
    if 'barcode_sample_map' in value:
        value['barcode_map'] = value['barcode_sample_map']
        del value['barcode_sample_map']


@upgrade_step('multiplexed_sample', '9', '10')
def multiplexed_sample_9_10(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1928
    value['multiplexing_methods'] = ['barcode based']
    notes = value.get('notes', '')
    notes += f'This object\'s multiplexing_methods has been set to barcode based by an upgrade. Please make sure it is correct before removing the notes.'
    value['notes'] = notes.strip()


@upgrade_step('in_vitro_system', '23', '24')
def in_vitro_system_23_24(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2284
    if value['classifications'] == ['gastruloid'] and 'time_post_change' not in value:
        value['time_post_change'] = 8
        value['time_post_change_units'] = 'day'
        value['targeted_sample_term'] = '/sample-terms/UBERON_0004734/'
        value['cell_fate_change_protocols'] = ['j-michael-cherry:dummy_document']
        notes = value.get('notes', '')
        notes += (
            f'cell_fate_change_protocols, time_post_change, time_post_change_units and targeted_sample_term '
            f'has been arbitrarily set based on an upgrade due to additional gastruloid dependencies.'
            f' Please make sure it is correct before removing the notes.'
        )
        value['notes'] = notes.strip()


@upgrade_step('primary_cell', '21', '22')
@upgrade_step('in_vitro_system', '24', '25')
def sample_21_22(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2310
    if 'calcified' in value.get('biosample_qualifiers', []):
        value['biosample_qualifiers'].remove('calcified')
        value['biosample_qualifiers'].append('6 days calcified')
        notes = value.get('notes', '')
        notes += f'This object\'s biosample_qualifiers has been set to 6 days calcified based by an upgrade. Please make sure it is correct before removing the notes.'
        value['notes'] = notes.strip()


@upgrade_step('in_vitro_system', '25', '26')
def in_vitro_system_25_26(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2486
    if value['classifications'] == ['pooled cell specimen']:
        value['classifications'] = ['cell line', 'pooled cell specimen']
        notes = value.get('notes', '')
        notes += f'This object\'s classifications was previously pooled cell specimen. It has been upgraded to both cell line and pooled cell specimen classifications by an upgrade.'
        value['notes'] = notes.strip()


@upgrade_step('in_vitro_system', '26', '27')
def in_vitro_system_26_27(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2107
    # This upgrade to replace cell_fate_change_treatments with cell_fate_change_protocol was done manually across the every server.
    return


@upgrade_step('primary_cell', '22', '23')
@upgrade_step('in_vitro_system', '27', '28')
@upgrade_step('tissue', '21', '22')
@upgrade_step('whole_organism', '24', '25')
def sample_22_23(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2085
    if 'embryonic' not in value:
        value['embryonic'] = False
