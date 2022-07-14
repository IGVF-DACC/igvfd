from snovault import upgrade_step


@upgrade_step('document', '1', '2')
def document_1_2(value, system):
    if 'urls' in value:
        if len(value['urls']) == 0:
            del value['urls']
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']
