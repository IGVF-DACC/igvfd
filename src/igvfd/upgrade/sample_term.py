from snovault import upgrade_step


@upgrade_step('sample_term', '1', '2')
def sample_term_1_2(value, system):
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']
