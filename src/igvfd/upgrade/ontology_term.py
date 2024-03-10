from snovault import upgrade_step


@upgrade_step('phenotype_term', '1', '2')
@upgrade_step('assay_term', '1', '2')
@upgrade_step('sample_term', '1', '2')
def ontology_term_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-221
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']


@upgrade_step('phenotype_term', '2', '3')
@upgrade_step('assay_term', '2', '3')
@upgrade_step('sample_term', '2', '3')
@upgrade_step('platform_term', '1', '2')
def ontology_term_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1170
    if 'description' in value:
        if value['description'] == '':
            del value['description']


@upgrade_step('assay_term', '3', '4')
def assay_term_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1504
    new_assay_titles = []
    new_notes = []
    prefix_note = 'Preferred_assay_titles enum '
    old_to_new = {
        'histone ChIP-seq': 'Histone ChIP-seq',
        'Parse Split-seq': 'Parse SPLiT-seq',
        'Saturation genome editing': 'SGE',
        'SHARE-Seq': 'SHARE-seq',
        'Yeast two-hybrid': 'Y2H'
    }
    if 'preferred_assay_titles' in value:
        for assay_title in value['preferred_assay_titles']:
            if assay_title in old_to_new:
                new_assay_titles.append(old_to_new[assay_title])
                new_notes.append(
                    f'{assay_title} now has been renamed to be {old_to_new[assay_title]}')
            else:
                new_assay_titles.append(assay_title)
    if len(new_assay_titles) >= 1:
        value['preferred_assay_titles'] = list(set(new_assay_titles))
        if 'notes' in value:
            value['notes'] = f"{value['notes']} {prefix_note} {', '.join(new_notes)}."
        else:
            value['notes'] = f"{prefix_note} {', '.join(new_notes)}."


@upgrade_step('phenotype_term', '3', '4')
@upgrade_step('assay_term', '4', '5')
@upgrade_step('sample_term', '3', '4')
@upgrade_step('platform_term', '2', '3')
def ontology_term_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1494
    if value['status'] in ['released', 'archived'] and 'release_timestamp' not in value:
        value['release_timestamp'] = '2024-03-06T12:34:56Z'
        notes = value.get('notes', '')
        notes += f'This object\'s release_timestamp has been set to 2024-03-06T12:34:56Z'
        value['notes'] = notes.strip()

