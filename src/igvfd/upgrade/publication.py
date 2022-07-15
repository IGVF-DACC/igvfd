from snovault import upgrade_step


@upgrade_step('publication', '1', '2')
def publication_1_2(value, system):
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']
