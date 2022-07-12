from snovault import upgrade_step


@upgrade_step('technical_sample', '1', '2')
def technical_sample_1_2(value, system):
    if 'dbxrefs' in value and len(value['dbxrefs']) == 0:
        del value['dbxrefs']
