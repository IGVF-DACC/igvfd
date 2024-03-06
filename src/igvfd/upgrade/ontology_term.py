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
    if 'preferred_assay_title' in value:
        if value['preferred_assay_titles'] == 'histone ChIP-seq':
            value['preferred_assay_titles'] = 'Histone ChIP-seq'
        if value['preferred_assay_titles'] == 'Parse Split-seq':
            value['preferred_assay_titles'] = 'Parse SPLiT-seq'
        if value['preferred_assay_titles'] == 'Saturation genome editing':
            value['preferred_assay_titles'] = 'SGE'
        if value['preferred_assay_titles'] == 'SHARE-Seq':
            value['preferred_assay_titles'] = 'SHARE-seq'
        if value['preferred_assay_titles'] == 'Yeast two-hybrid':
            value['preferred_assay_titles'] = 'Y2H'
    return
