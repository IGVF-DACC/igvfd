from snovault import upgrade_step


@upgrade_step('treatment', '1', '2')
def treatment_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-221
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']
    if 'documents' in value:
        if len(value['documents']) == 0:
            del value['documents']


@upgrade_step('treatment', '2', '3')
def treatment_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-292
    notes = value.get('notes', '')
    if 'purpose' not in value:
        value['purpose'] = 'perturbation'
        if 'notes' in value:
            value['notes'] = f'{value.get("notes")}. This treatment did not have purpose specified previously, it was upgraded to have perturbation purpose.'
        else:
            value['notes'] = 'This treatment did not have purpose specified previously, it was upgraded to have perturbation purpose.'
    return


@upgrade_step('treatment', '3', '4')
def treatment_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-845
    notes = value.get('notes', '')
    if 'award' not in value and 'lab' not in value and 'depletion' not in value:
        value['award'] = '/awards/HG012012'
        value['lab'] = '/labs/j-michael-cherry'
        value['depletion'] = False
        if 'notes' in value:
            value['notes'] = f'{value.get("notes")}. This treatment does not have award, lab, depletion specified previously, it was upgraded to have Cherry lab/award and depletion=False.'
        else:
            value['notes'] = 'This treatment does not have award, lab, depletion specified previously, it was upgraded to have Cherry lab/award and depletion=False.'
    return


@upgrade_step('treatment', '4', '5')
def treatment_4_5(value, system):
    # https://igvf.atlassian.net/browse/IGVF-895
    # Source property is pluralized
    if 'source' in value:
        value['sources'] = [value['source']]
        del value['source']


@upgrade_step('treatment', '5', '6')
def treatment_5_6(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1170
    if 'description' in value:
        if value['description'] == '':
            del value['description']


@upgrade_step('treatment', '6', '7')
def treatment_6_7(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1494
    if value['status'] in ['released', 'archived'] and 'release_timestamp' not in value:
        value['release_timestamp'] = '2024-03-06T12:34:56Z'
        notes = value.get('notes', '')
        notes += f'This object\'s release_timestamp has been set to 2024-03-06T12:34:56Z'
        value['notes'] = notes.strip()


@upgrade_step('treatment', '7', '8')
def treatment_7_8(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1803
    notes = value.get('notes', '')
    if 'lot_id' in value and 'product_id' not in value:
        notes += f' Lot_id {value["lot_id"]} was removed from this treatment.'
        del value['lot_id']
    if 'product_id' in value and 'sources' not in value:
        notes += f' Product_id {value["product_id"]} was removed from this treatment.'
        del value['product_id']
        if 'lot_id' in value:
            notes += f' Lot_id {value["lot_id"]} was removed from this treatment.'
            del value['lot_id']
    if notes:
        value['notes'] = notes.strip()


@upgrade_step('treatment', '8', '9')
def treatment_8_9(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2085
    if 'depletion' not in value:
        value['depletion'] = False
    return


@upgrade_step('treatment', '9', '10')
def treatment_9_10(value, system):
    # https://igvf.atlassian.net/browse/IGVF-3018
    notes = value.get('notes', '')
    if value['treatment_type'] == 'environmental':
        value['treatment_type'] = 'protein'
        value['treatment_term_id'] = 'NTR:0000000'
        notes += f'This treatment object was previously modeled as an environmental treatment but has been upgraded to protein. Stiffness environmental treatments are now reflected as growth_medium on in vitro system. This object should be deleted.'
    if notes:
        value['notes'] = notes.strip()
    return
