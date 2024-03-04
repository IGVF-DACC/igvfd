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


@upgrade_step('phenotype_term', '3', '4')
@upgrade_step('assay_term', '3', '4')
@upgrade_step('sample_term', '3', '4')
@upgrade_step('platform_term', '2', '3')
def ontology_term_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1494
    if value['status'] == 'released' or value['status'] == 'archived':
        if 'release_timestamp' not in value:
            value['release_timestamp'] == '2024-03-06T12:34:56Z'
            notes = value.get('notes', '')
            notes += f'This object\'s release_timestamp has been set to 2024-03-06T12:34:56Z'
            value['notes'] = notes.strip()
