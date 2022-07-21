from snovault import upgrade_step


@upgrade_step('differentiated_tissue', '1', '2')
def differentiated_tissue_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-207
    return


@upgrade_step('differentiated_tissue', '2', '3')
def differentiated_tissue_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-210
    return


@upgrade_step('differentiated_tissue', '3', '4')
def differentiated_tissue_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-221
    if 'treatments' in value:
        if len(value['treatments']) == 0:
            del value['treatments']
    if 'donors' in value:
        if len(value['donors']) == 0:
            del value['donors']
    if 'dbxrefs' in value:
        if len(value['dbxrefs']) == 0:
            del value['dbxrefs']
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']
    if 'collections' in value:
        if len(value['collections']) == 0:
            del value['collections']
    if 'alternate_accessions' in value:
        if len(value['alternate_accessions']) == 0:
            del value['alternate_accessions']


@upgrade_step('differentiated_tissue', '4', '5')
def differentiated_tissue_4_5(value, system):
    # https://igvf.atlassian.net/browse/IGVF-239
    if 'post_differentiation_time_units' in value:
        if value['post_differentiation_time_units'] == 'stage':
            old_diff_time = value['post_differentiation_time']
            if 'notes' in value:
                old_notes_value = value['notes']
                if old_diff_time == 1:
                    value['notes'] = old_notes_value + f'\nDifferentiation used one stage.'
                else:
                    value['notes'] = old_notes_value + f'\nDifferentiation used {old_diff_time} stages.'
            else:
                if old_diff_time == 1:
                    value['notes'] = f'Differentiation used one stage.'
                else:
                    value['notes'] = f'Differentiation used {old_diff_time} stages.'
            del value['post_differentiation_time_units']
            del value['post_differentiation_time']
    return