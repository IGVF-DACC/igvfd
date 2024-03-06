from snovault import upgrade_step


@upgrade_step('analysis_set', '1', '2')
@upgrade_step('curated_set', '1', '2')
@upgrade_step('measurement_set', '1', '2')
def file_set_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-321
    if 'sample' in value:
        value['samples'] = value['sample']
        del value['sample']
    if 'donor' in value:
        value['donors'] = value['donor']
        del value['donor']
    if 'input_file_set' in value:
        value['input_file_sets'] = value['input_file_set']
        del value['input_file_set']


@upgrade_step('analysis_set', '2', '3')
@upgrade_step('curated_set', '2', '3')
@upgrade_step('measurement_set', '2', '3')
def file_set_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-398
    if 'accession' in value:
        accession_suffix = value['accession'][6:]
        value['accession'] = f'IGVFDS0{accession_suffix}A'


@upgrade_step('measurement_set', '3', '4')
def measurement_set_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-537
    if 'protocol' in value:
        if value['protocol'] == 'https://www.protocols.io/':
            del value['protocol']


@upgrade_step('measurement_set', '4', '5')
def measurement_set_4_5(value, system):
    # https://igvf.atlassian.net/browse/IGVF-679
    notes = value.get('notes', '')
    if 'seqspec' in value:
        seqspec = value['seqspec']
        notes += f' This meausurement_set previously linked to {seqspec}, but the property for submitting associated seqspec links has been moved to SequenceFile where it should be submitted as a link to the seqspec yaml file submitted as a ConfigurationFile instead.'
        value['notes'] = notes.strip()
        del value['seqspec']


@upgrade_step('curated_set', '3', '4')
@upgrade_step('auxiliary_set', '1', '2')
def file_set_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-802
    if 'references' in value:
        value['publication_identifiers'] = value['references']
        del value['references']


@upgrade_step('auxiliary_set', '2', '3')
def auxiliary_set_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1036
    if 'auxiliary_type' in value:
        value['file_set_type'] = value['auxiliary_type']
        del value['auxiliary_type']


@upgrade_step('measurement_set', '5', '6')
@upgrade_step('prediction_set', '1', '2')
def file_set_5_6(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1111
    return


@upgrade_step('measurement_set', '6', '7')
@upgrade_step('auxiliary_set', '3', '4')
def file_set_6_7(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1177
    notes = value.get('notes', '')
    if 'construct_libraries' in value:
        notes += f" ConstructLibrary object(s) {value['construct_libraries']} was removed via upgrade."
        del value['construct_libraries']
    if 'moi' in value:
        notes += f" MOI {value['moi']} was removed via upgrade."
        del value['moi']
    if 'nucleic_acid_delivery' in value:
        notes += f" Nucleic acid delivery {value['nucleic_acid_delivery']} was removed via upgrade."
        del value['nucleic_acid_delivery']
    if 'control_file_sets' in value:
        filtered_control_file_sets = []
        removed_control_file_sets = []
        for ctrl_file_set in value['control_file_sets']:
            if ctrl_file_set.startswith('/construct-libraries/'):
                removed_control_file_sets.append(ctrl_file_set)
            else:
                filtered_control_file_sets.append(ctrl_file_set)
        value['control_file_sets'] = filtered_control_file_sets
        if len(removed_control_file_sets) > 0:
            notes += f" Control file sets {', '.join(removed_control_file_sets)} were removed via upgrade."
    if notes != '':
        value['notes'] = notes.strip()


@upgrade_step('curated_set', '4', '5')
def curated_set_type_4_5(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1070
    if 'curated_set_type' in value:
        value['file_set_type'] = value['curated_set_type']
        del value['curated_set_type']
    return


@upgrade_step('measurement_set', '7', '8')
def measurement_set_7_8(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1169
    if 'multiome_size' in value:
        value['multiome_size'] = int(value['multiome_size'])


@upgrade_step('measurement_set', '8', '9')
def measurement_set_8_9(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1167
    if 'sequencing_library_type' in value:
        value['sequencing_library_types'] = value['sequencing_library_type']
        del value['sequencing_library_type']


@upgrade_step('analysis_set', '3', '4')
def analysis_set_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1241
    if 'file_set_type' not in value:
        value['file_set_type'] = 'intermediate analysis'
        notes = value.get('notes', '')
        notes += f' This analyis set has been defaulted to "intermediate analysis" for its file_set_type as this is now a required property, please see the property description and patch with the appropriate file_set_type.'
        value['notes'] = notes.strip()


@upgrade_step('construct_library_set', '1', '2')
def construct_library_set_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1151
    if 'exon' in value:
        if value['exon'] == '':
            value['exon'] = 'exon_ID'
            notes = value.get('notes', '')
            notes += f' The required exon identifier was defaulted to "exon_ID" in an upgrade, please patch this property with the correct identifier.'
            value['notes'] = notes.strip()
    return


@upgrade_step('measurement_set', '9', '10')
@upgrade_step('auxiliary_set', '4', '5')
@upgrade_step('analysis_set', '4', '5')
@upgrade_step('construct_library_set', '2', '3')
@upgrade_step('curated_set', '5', '6')
@upgrade_step('model_set', '1', '2')
@upgrade_step('prediction_set', '2', '3')
def file_set_7_8(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1177
    if 'description' in value:
        if value['description'] == '':
            del value['description']


@upgrade_step('measurement_set', '10', '11')
def measurement_set_10_11(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1171
    if 'file_set_type' not in value:
        value['file_set_type'] = 'experimental data'


@upgrade_step('auxiliary_set', '5', '6')
def auxiliary_set_5_6(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1337
    if 'file_set_type' in value:
        if value['file_set_type'] == 'oligo-conjugated antibodies':
            value['file_set_type'] = 'cell hashing'
            notes = value.get('notes', '')
            notes += f' Original file_set_type was oligo-conjugated antibodies. This was replaced to be cell hashing during upgrade.'
            value['notes'] = notes.strip()
    return


@upgrade_step('measurement_set', '11', '12')
def measurement_set_11_12(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1373
    if 'protocol' in value:
        value['protocols'] = [value['protocol']]
        del value['protocol']


@upgrade_step('prediction_set', '3', '4')
def prediction_set_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1311
    if 'targeted_genes' in value:
        value['genes'] = value['targeted_genes']
        del value['targeted_genes']
    if 'targeted_loci' in value:
        value['loci'] = value['targeted_loci']
        del value['targeted_loci']
    return


@upgrade_step('construct_library_set', '3', '4')
def construct_library_set_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1311
    return


@upgrade_step('construct_library_set', '4', '5')
@upgrade_step('prediction_set', '4', '5')
def construct_library_set_prediction_set_4_5(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1426
    if 'genes' in value:
        if len(value.get('genes', [])) <= 100:
            value['small_scale_gene_list'] = value['genes']
        else:
            notes = value.get('notes', '')
            genes = ', '.join(value.get('genes', []))
            value['small_scale_gene_list'] = value['genes'][:100]
            notes += f' This file set previously listed `genes`: {genes}, which has more than 100 genes, please resubmit the genes in large_scale_gene_list.'
            value['notes'] = notes.strip()
        del value['genes']
    elif 'loci' in value:
        if len(value.get('loci', [])) <= 100:
            value['small_scale_loci_list'] = value['loci']
        else:
            notes = value.get('notes', '')
            loci = ', '.join(value.get('loci', []))
            value['small_scale_loci_list'] = value['loci'][:100]
            notes += f' This file set previously listed `loci`: {loci}, which has more than 100 loci, please resubmit the loci in large_scale_loci_list.'
            value['notes'] = notes.strip()
        del value['loci']
    return


@upgrade_step('construct_library_set', '5', '6')
@upgrade_step('prediction_set', '5', '6')
def construct_library_set_prediction_set_5_6(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1016
    for loci in value.get('small_scale_loci_list', []):
        if loci['assembly'] == 'hg19':
            notes = value.get('notes', '')
            notes += f' This file set listed {loci} as one of its loci but the assembly for this loci has been upgraded to GRCh38.'
            value['notes'] = notes.strip()
            loci['assembly'] = 'GRCh38'
        elif loci['assembly'] in ['mm9', 'mm10']:
            notes = value.get('notes', '')
            notes += f' This file set listed {loci} as one of its loci but the assembly for this loci has been upgraded to GRCm39.'
            value['notes'] = notes.strip()
            loci['assembly'] = 'GRCm39'
<<<<<<< HEAD
<<<<<<< HEAD


@upgrade_step('measurement_set', '12', '13')
def measurement_set_12_13(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1504
    old_to_new = {
        'histone ChIP-seq': 'Histone ChIP-seq',
        'Parse Split-seq': 'Parse SPLiT-seq',
        'Saturation genome editing': 'SGE',
        'SHARE-Seq': 'SHARE-seq',
        'Yeast two-hybrid': 'Y2H'
    }
    if 'preferred_assay_title' in value:
        old_assay_title = value['preferred_assay_title']
        if old_assay_title in old_to_new:
            value['preferred_assay_title'] = old_to_new[old_assay_title]
            if 'notes' in value:
                value['notes'] = f"{value['notes']}. Preferred_assay_titles enum {old_assay_title} has been renamed to be {old_to_new[old_assay_title]}."
            else:
                value['notes'] = f'Preferred_assay_titles enum {old_assay_title} has been renamed to be {old_to_new[old_assay_title]}.'
    return


@upgrade_step('measurement_set', '13', '14')
@upgrade_step('auxiliary_set', '6', '7')
@upgrade_step('analysis_set', '5', '6')
@upgrade_step('construct_library_set', '6', '7')
@upgrade_step('curated_set', '6', '7')
@upgrade_step('model_set', '2', '3')
@upgrade_step('prediction_set', '6', '7')
def file_set_8_9(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1494
    if value['status'] in ['released', 'archived', 'revoked'] and 'release_timestamp' not in value:
        value['release_timestamp'] = '2024-03-06T12:34:56Z'
        notes = value.get('notes', '')
        notes += f'This object\'s release_timestamp has been set to 2024-03-06T12:34:56Z'
        value['notes'] = notes.strip()


@upgrade_step('construct_library_set', '7', '8')
def construct_library_set_7_8(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1507
    return
