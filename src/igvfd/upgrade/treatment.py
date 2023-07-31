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
    # https://igvf.atlassian.net/browse/IGVF-895
    # Source property is pluralized
    if 'source' in value:
        value['sources'] = value['source']
        del value['source']
