from snovault import upgrade_step


@upgrade_step('human_donor', '1', '2')
@upgrade_step('rodent_donor', '1', '2')
def donor_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-221
    if 'parents' in value:
        if len(value['parents']) == 0:
            del value['parents']
    if 'external_resources' in value:
        if len(value['external_resources']) == 0:
            del value['external_resources']
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']
    if 'collections' in value:
        if len(value['collections']) == 0:
            del value['collections']
    if 'alternate_accessions' in value:
        if len(value['alternate_accessions']) == 0:
            del value['alternate_accessions']
    if 'documents' in value:
        if len(value['documents']) == 0:
            del value['documents']
    if 'references' in value:
        if len(value['references']) == 0:
            del value['references']


@upgrade_step('human_donor', '2', '3')
def human_donor_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-90
    if 'health_status_history' in value:
        del value['health_status_history']


@upgrade_step('human_donor', '3', '4')
def donor_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-321
    if 'ethnicity' in value:
        value['ethnicities'] = value['ethnicity']
        del value['ethnicity']


@upgrade_step('human_donor', '4', '5')
@upgrade_step('rodent_donor', '2', '3')
def donor_4_5(value, system):
    # https://igvf.atlassian.net/browse/IGVF-398
    if 'accession' in value:
        accession_prefix = value['accession'][0:6]
        accession_suffix = value['accession'][6:]
        value['accession'] = f'{accession_prefix}0{accession_suffix}A'


@upgrade_step('human_donor', '5', '6')
@upgrade_step('rodent_donor', '3', '4')
def donor_5_6(value, system):
    # https://igvf.atlassian.net/browse/IGVF-386
    if 'external_resources' in value:
        del value['external_resources']


@upgrade_step('rodent_donor', '4', '5')
def rodent_donor_4_5(value, system):
    # https://igvf.atlassian.net/browse/IGVF-384
    if 'individual_rodent' not in value:
        value['individual_rodent'] = False


@upgrade_step('human_donor', '6', '7')
@upgrade_step('rodent_donor', '5', '6')
def donor_6_7(value, system):
    # https://igvf.atlassian.net/browse/IGVF-444
    if 'traits' in value:
        traits = value['traits']
        new_notes_value = ''
        if 'notes' in value:
            new_notes_value = value.get('notes')
        for current_trait in traits:
            if len(new_notes_value) > 0:
                new_notes_value += '  '
            new_notes_value += f'traits: {current_trait}'
        value['notes'] = new_notes_value
        del value['traits']


@upgrade_step('rodent_donor', '6', '7')
def rodent_donor_6_7(value, system):
    # https://igvf.atlassian.net/browse/IGVF-408
    if 'parents' in value:
        parents = value['parents']
        if 'notes' in value:
            new_notes_value = value.get('notes')
        for parent in parents:
            if len(new_notes_value) > 0:
                new_notes_value += '  '
            new_notes_value += f'parents: {parent}'
        value['notes'] = new_notes_value
        del value['parents']


@upgrade_step('human_donor', '7', '8')
def human_donor_7_8(value, system):
    # https://igvf.atlassian.net/browse/IGVF-408
    if 'parents' in value:
        parents = value['parents']
        related_donors = []
        for parent in parents:
            related_donors.append(
                {
                    'donor': parent,
                    'relationship_type': 'parent'
                }
            )
        value['related_donors'] = related_donors
        del value['parents']


@upgrade_step('human_donor', '8', '9')
@upgrade_step('rodent_donor', '7', '8')
def donor_8_9(value, system):
    # https://igvf.atlassian.net/browse/IGVF-726
    # This upgrade is to update previous data with
    # default value for 'virtual' property.
    # The default value will be automatically populated.
    return


@upgrade_step('human_donor', '9', '10')
def human_donor_9_10(value, system):
    # https://igvf.atlassian.net/browse/IGVF-765
    if 'human_donor_identifier' in value:
        value['human_donor_identifiers'] = value['human_donor_identifier']
        del value['human_donor_identifier']


@upgrade_step('human_donor', '10', '11')
@upgrade_step('rodent_donor', '8', '9')
def donor_10_11(value, system):
    # https://igvf.atlassian.net/browse/IGVF-802
    if 'references' in value:
        value['publication_identifiers'] = value['references']
        del value['references']
