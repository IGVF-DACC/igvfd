from snovault import upgrade_step


@upgrade_step('treatment', '1', '2')
def treatment_1_2(value, system):
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']
    if 'documents' in value:
        if len(value['documents']) == 0:
            del value['documents']
