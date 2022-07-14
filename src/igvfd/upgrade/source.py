from snovault import upgrade_step


@upgrade_step('source', '1', '2')
def source_1_2(value, system):
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']
