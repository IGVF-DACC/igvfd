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
    return


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


@upgrade_step('measurement_set', '14', '15')
def measurement_set_14_15(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1533
    if 'auxiliary_sets' in value:
        if len(value['auxiliary_sets']) < 1:
            del value['auxiliary_sets']
    if 'control_file_sets' in value:
        if len(value['control_file_sets']) < 1:
            del value['control_file_sets']
    if 'protocols' in value:
        if len(value['protocols']) < 1:
            del value['protocols']
    if 'sequencing_library_types' in value:
        if len(value['sequencing_library_types']) < 1:
            del value['sequencing_library_types']


@upgrade_step('measurement_set', '15', '16')
def measurement_set_15_16(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1571
    if len(value['samples']) > 1:
        sample = value['samples'][0]
        other_samples = ', '.join(value['samples'][1:])
        notes = value.get('notes', '')
        notes = f'{notes} This measurement set used to link to samples: {other_samples}, but has since been upgraded to only link to {sample}.'
        value['notes'] = notes
        value['samples'] = [sample]


@upgrade_step('measurement_set', '16', '17')
def measurement_set_16_17(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1602
    if 'readout' in value:
        readout = value['readout']
        del value['readout']
        notes = value.get('notes', '')
        notes = f'{notes} The readout {readout} was removed from this measurement set.'
        value['notes'] = notes.strip()


@upgrade_step('analysis_set', '6', '7')
def analysis_set_6_7(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1701
    if value.get('file_set_type', '') == 'primary analysis':
        value['file_set_type'] = 'principal analysis'
        notes = value.get('notes', '')
        notes += f'This object\'s file_set_type was primary analysis and has been updated to be principal analysis.'
        value['notes'] = notes.strip()


@upgrade_step('auxiliary_set', '7', '8')
def auxiliary_set_7_8(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1757
    if value.get('file_set_type', '') == 'circularized barcode detection':
        value['file_set_type'] = 'circularized RNA barcode detection'
    if value.get('file_set_type', '') == 'quantification barcode sequencing':
        value['file_set_type'] = 'quantification DNA barcode sequencing'


@upgrade_step('measurement_set', '17', '18')
@upgrade_step('auxiliary_set', '8', '9')
@upgrade_step('analysis_set', '7', '8')
@upgrade_step('construct_library_set', '8', '9')
@upgrade_step('curated_set', '7', '8')
@upgrade_step('model_set', '3', '4')
@upgrade_step('prediction_set', '7', '8')
def file_set_17_18(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1789
    if 'publication_identifiers' in value:
        del value['publication_identifiers']


@upgrade_step('measurement_set', '18', '19')
@upgrade_step('auxiliary_set', '9', '10')
def measurement_set_18_19_auxiliary_set_9_10(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1776
    notes = value.get('notes', '')
    if 'library_construction_platform' in value:
        library_construction_platform = value['library_construction_platform']
        notes += f' This file_set previously had {library_construction_platform} submitted as library_construction_platform, but the property library_construction_platform has been now removed.'
        value['notes'] = notes.strip()
        del value['library_construction_platform']


@upgrade_step('auxiliary_set', '10', '11')
def auxiliary_set_10_11(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1797
    old_to_new = {
        'cell hashing': 'cell hashing barcode sequencing',
        'oligo-conjugated lipids': 'lipid-conjugated oligo sequencing'
    }
    if 'file_set_type' in value:
        old_file_set_type = value['file_set_type']
        if old_file_set_type in old_to_new:
            value['file_set_type'] = old_to_new[old_file_set_type]
            if 'notes' in value:
                value['notes'] = f"{value['notes']}. File_set_type enum {old_file_set_type} has been renamed to be {old_to_new[old_file_set_type]}."
            else:
                value['notes'] = f'File_set_type enum {old_file_set_type} has been renamed to be {old_to_new[old_file_set_type]}.'
    return


@upgrade_step('measurement_set', '19', '20')
def measurement_set_19_20(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1855
    if value.get('preferred_assay_title') == 'CRISPR FlowFISH':
        value['preferred_assay_title'] = 'CRISPR FlowFISH screen'


@upgrade_step('measurement_set', '20', '21')
def measurement_set_20_21(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1840
    if not (value.get('preferred_assay_title', '')):
        value['preferred_assay_title'] = 'SUPERSTARR'
        notes = value.get('notes', '')
        added_phrase = 'This measurement set previously did not specify a preferred_assay_title, but the property is now required so it has been defaulted to SUPERSTARR. Please update with an appropriate preferred_assay_title.'
        if notes:
            value['notes'] = f'{notes} {added_phrase}'
        else:
            value['notes'] = added_phrase


@upgrade_step('measurement_set', '21', '22')
def measurement_set_21_22(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1957
    notes = value.get('notes', '')
    if value.get('preferred_assay_title') == 'Variant painting':
        value['preferred_assay_title'] = 'Variant painting via fluorescence'
        notes += f' This measurement set previously used Variant painting as a preferred_assay_title, but this enum is now removed. So it has been defaulted to Variant painting via fluorescence.'
        value['notes'] = notes.strip()


@upgrade_step('construct_library_set', '9', '10')
def construct_library_set_9_10(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1917
    root = system['registry']['root']
    keep = ['reference_file', 'tabular_file']
    notes = value.get('notes', '')
    filtered_integrated_content_files = []
    removed_integrated_content_files = []
    if 'integrated_content_files' in value:
        for integrated_content_file in value['integrated_content_files']:
            if root.get_by_uuid(integrated_content_file).item_type not in keep:
                removed_integrated_content_files.append(integrated_content_file)
            else:
                filtered_integrated_content_files.append(integrated_content_file)
        if filtered_integrated_content_files:
            value['integrated_content_files'] = filtered_integrated_content_files
        else:
            del value['integrated_content_files']
        if removed_integrated_content_files:
            notes += f" Integrated content files {', '.join(removed_integrated_content_files)} were removed via upgrade."
            value['notes'] = notes.strip()


@upgrade_step('analysis_set', '8', '9')
def analysis_set_8_9(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1929
    if value.get('samples'):
        del value['samples']


@upgrade_step('measurement_set', '22', '23')
def measurement_set_22_23(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2188
    notes = value.get('notes', '')
    if value.get('preferred_assay_title') == 'Variant FlowFISH':
        value['preferred_assay_title'] = 'Variant-EFFECTS'
        notes += f' This measurement set previously used Variant FlowFISH as a preferred_assay_title, but this enum is now removed. So it has been defaulted to Variant-EFFECTS.'
        value['notes'] = notes.strip()


@upgrade_step('auxiliary_set', '11', '12')
def auxiliary_set_11_12(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2162
    notes = value.get('notes', '')
    if value.get('file_set_type') == 'variant sequencing':
        value['file_set_type'] = 'gRNA sequencing'
        notes += f' This auxiliary set previously used variant sequencing as its file_set_type, but this enum is now removed. So it has been defaulted to gRNA sequencing.'
        value['notes'] = notes.strip()


@upgrade_step('model_set', '4', '5')
def model_set_4_5(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2239
    notes = value.get('notes', '')
    software_version = value.get('software_version', '')
    if software_version:
        notes += f' This model set previously specified {software_version}, but this property has been removed and replaced by software_versions calculated through analysis_step_version on the model file.'
        value['notes'] = notes.strip()
        del value['software_version']


@upgrade_step('measurement_set', '23', '24')
def measurement_set_23_24(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2431
    notes = value.get('notes', '')
    if value.get('preferred_assay_title') == 'scMito-seq':
        value['preferred_assay_title'] = '10x multiome with scMito-seq'
        notes += f' This measurement set previously used scMito-seq as a preferred_assay_title, but this enum is now replaced with 10x multiome with scMito-seq.'
        value['notes'] = notes.strip()


@upgrade_step('measurement_set', '24', '25')
def measurement_set_24_25(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2426
    notes = value.get('notes', '')
    if value.get('preferred_assay_title') == 'Growth CRISPR screen':
        value['preferred_assay_title'] = 'Proliferation CRISPR screen'
        notes += f' This measurement set previously used Growth CRISPR screen as a preferred_assay_title, but the preferred_assay_title has now been updated to Proliferation CRISPR screen via an upgrade.'
        value['notes'] = notes.strip()


@upgrade_step('measurement_set', '25', '26')
def measurement_set_25_26(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2541
    notes = value.get('notes', '')
    if value.get('strand_specificity') == "5' to 3'":
        value['strand_specificity'] = '5 prime to 3 prime'
        notes += f' This measurement set previously used 5\' to 3\' as strand_specificity, but the strand_specificity has now been updated to 5 prime to 3 prime via an upgrade.'
        value['notes'] = notes.strip()
    if value.get('strand_specificity') == "3' to 5'":
        value['strand_specificity'] = '3 prime to 5 prime'
        notes += f' This measurement set previously used 3\' to 5\' as strand_specificity, but the strand_specificity has now been updated to 3 prime to 5 prime via an upgrade.'
        value['notes'] = notes.strip()


@upgrade_step('analysis_set', '9', '10')
def analysis_set_9_10(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2318
    if 'demultiplexed_sample' in value:
        value['demultiplexed_samples'] = [value['demultiplexed_sample']]
        del value['demultiplexed_sample']


@upgrade_step('measurement_set', '26', '27')
@upgrade_step('construct_library_set', '10', '11')
def file_set_26_27(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2692
    notes = value.get('notes', '')
    if value.get('control_type') == 'control transduction':
        value['control_type'] = 'reference transduction'
        notes += f' This file set previously specified control_type control transduction but has since been upgraded to reference transduction.'


@upgrade_step('measurement_set', '27', '28')
def measurement_set_27_28(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2634
    notes = value.get('notes', '')
    if value.get('preferred_assay_title') == 'SUPERSTARR':
        value['preferred_assay_title'] = 'STARR-seq'
        notes += f' This measurement set previously used SUPERSTARR as a preferred_assay_title, but the preferred_assay_title has now been updated to STARR-seq via an upgrade.'
        value['notes'] = notes.strip()


@upgrade_step('measurement_set', '28', '29')
def measurement_set_28_29(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2691
    notes = value.get('notes', '')
    if value.get('preferred_assay_title') == '10x multiome with scMito-seq':
        value['preferred_assay_title'] = 'mtscMultiome'
        notes += f' This measurement set previously used 10x multiome with scMito-seq as a preferred_assay_title, but the preferred_assay_title has now been updated to mtscMultiome via an upgrade.'
        value['notes'] = notes.strip()


@upgrade_step('measurement_set', '29', '30')
def measurement_set_29_30(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2730
    notes = value.get('notes', '')
    if value.get('preferred_assay_title') == 'CERES-seq':
        value['preferred_assay_title'] = 'Perturb-seq'
        notes += f' This measurement set previously used CERES-seq as a preferred_assay_title, but the preferred_assay_title has now been updated to Perturb-seq via an upgrade.'
        value['notes'] = notes.strip()


@upgrade_step('measurement_set', '30', '31')
def measurement_set_30_31(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2450
    notes = value.get('notes', '')
    old_to_new = {
        'mN2H': 'Arrayed mN2H',
        'semi-qY2H': 'Arrayed semi-qY2H v1',
        'Y2H': 'Arrayed Y2H v1',
        'yN2H': 'Arrayed yN2H'
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
