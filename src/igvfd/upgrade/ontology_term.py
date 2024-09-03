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


@upgrade_step('assay_term', '5', '6')
def ontology_term_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1533
    if 'preferred_assay_titles' in value:
        if len(value['preferred_assay_titles']) < 1:
            del value['preferred_assay_titles']


@upgrade_step('platform_term', '3', '4')
def platform_term_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1629
    if 'sequencing_kits' in value:
        if 'NovaSeq 6000 S4 Reagent Kit V1.5' in value['sequencing_kits']:
            value['sequencing_kits'].remove('NovaSeq 6000 S4 Reagent Kit V1.5')
            value['sequencing_kits'].append('NovaSeq 6000 S4 Reagent Kit v1.5')


@upgrade_step('sample_term', '4', '5')
def sample_term_4_5(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1073
    if 'dbxrefs' in value:
        if len(value['dbxrefs']) == 0:
            del value['dbxrefs']


@upgrade_step('assay_term', '6', '7')
def assay_term_6_7(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1855
    preferred_assay_titles = value.get('preferred_assay_titles', [])
    if 'CRISPR FlowFISH' in preferred_assay_titles:
        index = preferred_assay_titles.index('CRISPR FlowFISH')
        preferred_assay_titles[index] = 'CRISPR FlowFISH screen'
        value['preferred_assay_titles'] = preferred_assay_titles
