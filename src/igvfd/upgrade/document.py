from snovault import upgrade_step


@upgrade_step('document', '1', '2')
def document_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-221
    if 'urls' in value:
        if len(value['urls']) == 0:
            del value['urls']
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']


@upgrade_step('document', '2', '3')
def document_2_3(value, system):
    if 'description' in value:
        if value['description'] == '':
            value['description'] = 'Default upgrade text: please add details about document in description.'
