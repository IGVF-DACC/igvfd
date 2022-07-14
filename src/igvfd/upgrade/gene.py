from snovault import upgrade_step


@upgrade_step('gene', '1', '2')
def gene_1_2(value, system):
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']
