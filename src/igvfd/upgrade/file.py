from snovault import upgrade_step


@upgrade_step('sequence_file', '2', '3')
def file_2b_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-615
    notes = value.get('notes', '')
    value['sequencing_platform'] = '/platform-terms/EFO_0004203/'
    notes += f' PlatformTerm added via upgrade; verify before removing note.'
    value['notes'] = notes.strip()
    return


@upgrade_step('reference_file', '2', '3')
def ref_file_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-794
    if 'source' in value:
        value['source_url'] = value['source']
        del value['source']


@upgrade_step('reference_file', '3', '4')
def ref_file_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-795
    if 'transcriptome_annotation' in value:
        original_value = value['transcriptome_annotation']
        if original_value.startswith('V'):
            original_value = original_value.split('V')[1]
        new_value = 'GENCODE ' + original_value
        value['transcriptome_annotation'] = new_value


@upgrade_step('sequence_file', '3', '4')
def sequence_file_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1005
    if 'minimum_read_length' in value and value['minimum_read_length'] > 300000000:
        value['minimum_read_length'] = 300000000
        notes = value.get('notes', '')
        if notes:
            notes += f' The minimum read length previously exceeded the upper limit of 300000000 so was set to 300000000, please assign the appropriate length.'
        else:
            notes = f'The minimum read length previously exceeded the upper limit of 300000000 so was set to 300000000, please assign the appropriate length.'
        value['notes'] = notes
    if 'maximum_read_length' in value and value['maximum_read_length'] > 300000000:
        value['maximum_read_length'] = 300000000
        notes = value.get('notes', '')
        if notes:
            notes += f' The maximum read length previously exceeded the upper limit of 300000000 so was set to 300000000, please assign the appropriate length.'
        else:
            notes = f'The maximum read length previously exceeded the upper limit of 300000000 so was set to 300000000, please assign the appropriate length.'
        value['notes'] = notes
    if 'mean_read_length' in value and value['mean_read_length'] > 300000000:
        value['mean_read_length'] = 300000000
        notes = value.get('notes', '')
        if notes:
            notes += f' The mean read length previously exceeded the upper limit of 300000000 so was set to 300000000, please assign the appropriate length.'
        else:
            notes = f'The mean read length previously exceeded the upper limit of 300000000 so was set to 300000000, please assign the appropriate length.'
        value['notes'] = notes


@upgrade_step('reference_file', '4', '5')
def reference_file_4_5(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1215
    notes = value.get('notes', '')
    if value['file_format'] == 'bed':
        value['file_format_type'] = 'bed9+'
        notes += f' The file_format_type of this bed file was automatically set to bed9+.'
    if notes != '':
        value['notes'] = notes.strip()


@upgrade_step('reference_file', '5', '6')
@upgrade_step('matrix_file', '1', '2')
@upgrade_step('signal_file', '1', '2')
@upgrade_step('configuration_file', '1', '2')
@upgrade_step('alignment_file', '1', '2')
@upgrade_step('sequence_file', '4', '5')
@upgrade_step('genome_browser_annotation_file', '1', '2')
@upgrade_step('tabular_file', '1', '2')
def file_5_6(value, system):
    if 'dbxrefs' in value:
        new_dbxrefs = [dbxref for dbxref in value['dbxrefs'] if dbxref != '']
        if new_dbxrefs:
            value['dbxrefs'] = new_dbxrefs
        else:
            del value['dbxrefs']


@upgrade_step('reference_file', '6', '7')
def reference_file_6_7(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1272
    if 'external' not in value:
        value['external'] = False


@upgrade_step('reference_file', '7', '8')
@upgrade_step('matrix_file', '2', '3')
@upgrade_step('signal_file', '2', '3')
@upgrade_step('configuration_file', '2', '3')
@upgrade_step('alignment_file', '2', '3')
@upgrade_step('sequence_file', '5', '6')
@upgrade_step('genome_browser_annotation_file', '2', '3')
@upgrade_step('tabular_file', '2', '3')
def file_6_7(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1170
    if 'description' in value:
        if value['description'] == '':
            del value['description']


@upgrade_step('reference_file', '8', '9')
@upgrade_step('matrix_file', '3', '4')
@upgrade_step('signal_file', '3', '4')
@upgrade_step('configuration_file', '3', '4')
@upgrade_step('alignment_file', '3', '4')
@upgrade_step('sequence_file', '6', '7')
@upgrade_step('genome_browser_annotation_file', '3', '4')
@upgrade_step('tabular_file', '3', '4')
def file_7_8(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1327
    if value['status'] in ['released', 'revoked', 'archived']:
        if value['upload_status'] in ['pending', 'file not found']:
            value['upload_status'] = 'invalidated'
            notes = value.get('notes', '')
            notes += f' This publicly available file was previously pending or file not found upload_status, and was moved to invalidated upload_status.'
            value['notes'] = notes.strip()


@upgrade_step('alignment_file', '4', '5')
@upgrade_step('genome_browser_annotation_file', '4', '5')
@upgrade_step('reference_file', '9', '10')
@upgrade_step('signal_file', '4', '5')
@upgrade_step('tabular_file', '4', '5')
def file_8_9(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1293
    if value['file_format'] in [
        'bam',
        'bed',
        'bedpe',
        'bigBed',
        'bigWig',
        'bigInteract',
        'tabix',
        'vcf'
    ]:
        if 'assembly' not in value:
            value['assembly'] = 'GRCh38'
            notes = value.get('notes', '')
            notes += f' This file was automatically upgraded to have assembly GRCh38.'
            value['notes'] = notes.strip()


@upgrade_step('sequence_file', '7', '8')
def sequence_file_7_8(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1250
    # https://igvf.atlassian.net/browse/IGVF-1484
    # https://igvf.atlassian.net/browse/IGVF-1487
    if value['content_type'] == 'reads' and value['file_format'] == 'bam':
        notes = value.get('notes', '')
        notes += f' This file\'s content_type was upgraded from \"{value["content_type"]}\" to "PacBio subreads".'
        value['content_type'] = 'PacBio subreads'
        value['notes'] = notes.strip()
    elif value['content_type'] == 'subreads' and value['file_format'] == 'bam':
        notes = value.get('notes', '')
        notes += f' This file\'s content_type was upgraded from \"{value["content_type"]}\" to "PacBio subreads".'
        value['content_type'] = 'PacBio subreads'
        value['notes'] = notes.strip()
    elif value['content_type'] != 'reads' and value['file_format'] == 'fastq':
        notes = value.get('notes', '')
        notes += f' This file\'s content_type was upgraded from \"{value["content_type"]}\" to "reads".'
        value['content_type'] = 'reads'
        value['notes'] = notes.strip()


@upgrade_step('image_file', '1', '2')
def image_file_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1492
    return


@upgrade_step('alignment_file', '5', '6')
@upgrade_step('genome_browser_annotation_file', '5', '6')
@upgrade_step('signal_file', '5', '6')
@upgrade_step('tabular_file', '5', '6')
def file_9_10(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1016
    if value.get('assembly') == 'hg19':
        notes = value.get('notes', '')
        notes += f' This file\'s assembly was upgraded from {value["assembly"]} to "GRCh38".'
        value['assembly'] = 'GRCh38'
        value['notes'] = notes.strip()
    elif value.get('assembly') == 'mm10':
        notes = value.get('notes', '')
        notes += f' This file\'s assembly was upgraded from {value["assembly"]} to "GRCm39".'
        value['assembly'] = 'GRCm39'
        value['notes'] = notes.strip()
    return


@upgrade_step('sequence_file', '8', '9')
def sequence_file_8_9(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1481
    if 'seqspec' in value:
        notes = value.get('notes', '')
        notes += f' This file previously linked to the configuration file at {value["seqspec"]}.'
        value['notes'] = notes.strip()
        del value['seqspec']


@upgrade_step('configuration_file', '4', '5')
def configuration_file_4_5(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1481
    return


@upgrade_step('reference_file', '10', '11')
@upgrade_step('matrix_file', '4', '5')
@upgrade_step('signal_file', '6', '7')
@upgrade_step('configuration_file', '5', '6')
@upgrade_step('alignment_file', '6', '7')
@upgrade_step('sequence_file', '9', '10')
@upgrade_step('genome_browser_annotation_file', '6', '7')
@upgrade_step('tabular_file', '6', '7')
@upgrade_step('image_file', '2', '3')
def file_10_11(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1494
    if value['status'] in ['released', 'archived', 'revoked'] and 'release_timestamp' not in value:
        value['release_timestamp'] = '2024-03-06T12:34:56Z'
        notes = value.get('notes', '')
        notes += f'This object\'s release_timestamp has been set to 2024-03-06T12:34:56Z'
        value['notes'] = notes.strip()


@upgrade_step('alignment_file', '7', '8')
@upgrade_step('configuration_file', '6', '7')
@upgrade_step('genome_browser_annotation_file', '7', '8')
@upgrade_step('image_file', '3', '4')
@upgrade_step('matrix_file', '5', '6')
@upgrade_step('reference_file', '11', '12')
@upgrade_step('sequence_file', '10', '11')
@upgrade_step('signal_file', '7', '8')
@upgrade_step('tabular_file', '7', '8')
def file_11_12(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1533
    if 'derived_from' in value:
        if len(value['derived_from']) < 1:
            del value['derived_from']
    if 'file_format_specifications' in value:
        if len(value['file_format_specifications']) < 1:
            del value['file_format_specifications']
    if 'seqspec_of' in value:
        if len(value['seqspec_of']) < 1:
            del value['seqspec_of']


@upgrade_step('alignment_file', '8', '9')
@upgrade_step('reference_file', '12', '13')
@upgrade_step('sequence_file', '11', '12')
@upgrade_step('tabular_file', '8', '9')
def file_12_13(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1531
    return


@upgrade_step('sequence_file', '12', '13')
def sequence_file_12_13(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1629
    if 'sequencing_kit' in value:
        if value['sequencing_kit'] == 'NovaSeq 6000 S4 Reagent Kit V1.5':
            value['sequencing_kit'] = 'NovaSeq 6000 S4 Reagent Kit v1.5'
    return


@upgrade_step('alignment_file', '9', '10')
@upgrade_step('reference_file', '13', '14')
@upgrade_step('sequence_file', '13', '14')
@upgrade_step('tabular_file', '9', '10')
def file_13_14(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1682
    notes = value.get('notes', '')
    if 'controlled_access' not in value:
        value['controlled_access'] = False
        notes += f'This object\'s property controlled_access was set to be False, because it was previously missing.'
    elif (value['controlled_access'] is True and value['status'] in ['released', 'archived', 'revoked']):
        notes += f'This object\'s property status was {value["status"]}, and has been changed to in progress.'
        value['status'] = 'in progress'
        if 'release_timestamp' in value:
            notes += f'This object\'s property release_timestamp was {value["release_timestamp"]}, and has been removed.'
            del value['release_timestamp']
    if 'anvil_source_url' in value:
        notes += f'This object\'s property anvil_source_url was {value["anvil_source_url"]}.'
        del value['anvil_source_url']
    if value['upload_status'] == 'deposited':
        value['upload_status'] = 'pending'
        notes += f'This object\'s upload_status was deposited, and changed to pending.'
    if notes.strip() != '':
        value['notes'] = notes.strip()


@upgrade_step('signal_file', '8', '9')
@upgrade_step('tabular_file', '10', '11')
def tabular_file_10_11_signal_file_8_9(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1694
    if value.get('content_type') == 'fold over change control':
        value['content_type'] = 'fold change over control'
    return


@upgrade_step('tabular_file', '11', '12')
def tabular_file_11_12(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1948
    notes = value.get('notes', '')
    if value.get('content_type') == 'SNP effect matrix':
        value['content_type'] = 'variant effects'
        notes += f'This object\'s content_type was SNP effect matrix, and changed to variants effects via upgrade.'
    return


@upgrade_step('matrix_file', '6', '7')
def matrix_file_6_7(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1950
    if 'dimension1' in value:
        value['principal_dimension'] = value['dimension1']
        del value['dimension1']
    if 'dimension2' in value:
        value['secondary_dimensions'] = [value['dimension2']]
        del value['dimension2']


@upgrade_step('tabular_file', '12', '13')
def tabular_file_12_13(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2011
    notes = value.get('notes', '')
    if value.get('file_format') == 'txt':
        value['file_format'] = 'tsv'
        notes += f'This object\'s file_format was txt, and changed to tsv via upgrade.'
    if notes.strip() != '':
        value['notes'] = notes.strip()


@upgrade_step('reference_file', '14', '15')
def reference_file_14_15(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2040
    notes = value.get('notes', '')
    if 'external_id' in value:
        external_id = value['external_id']
        notes += f' This file previously had {external_id} submitted as external_id, but the property external_id has been now removed.'
        del value['external_id']
    if notes.strip() != '':
        value['notes'] = notes.strip()


@upgrade_step('alignment_file', '10', '11')
def alignment_file_10_11(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2113
    notes = value.get('notes', '')
    if value['file_format'] == 'bai':
        value['file_format'] = 'bam'
        notes += f' This file\'s file_format was .bai, but has been upgraded to .bam.'
    if notes.strip() != '':
        value['notes'] = notes.strip()


@upgrade_step('genome_browser_annotation_file', '8', '9')
def genome_browser_annotation_file_8_9(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2113
    notes = value.get('notes', '')
    if value['file_format'] == 'tabix':
        value['file_format'] = 'bigBed'
        notes += f' This file\'s file_format was .tabix, but has been upgraded to .bigBed.'
    if notes.strip() != '':
        value['notes'] = notes.strip()


@upgrade_step('alignment_file', '11', '12')
def alignment_file_11_12(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2175
    notes = value.get('notes', '')
    if 'assembly' not in value:
        value['assembly'] = 'custom'
        notes += f' This file lacked a newly required property assembly, and the assembly has been assigneed to be custom via an upgrade.'
    if notes.strip() != '':
        value['notes'] = notes.strip()


@upgrade_step('sequence_file', '14', '15')
@upgrade_step('alignment_file', '12', '13')
def sequence_file_14_15_alignment_file_12_13(value, system):
    # https://igvf.atlassian.net/browse/SNO2-71
    keys = ['read_count', 'minimum_read_length', 'maximum_read_length']
    for k in keys:
        # Coerce values like 28.0 to ints.
        if k in value:
            value[k] = int(value[k])


@upgrade_step('reference_file', '15', '16')
def reference_file_15_16(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2381
    notes = value.get('notes', '')
    if value['content_type'] == 'regulatory_regions':
        value['content_type'] = 'genomic_elements'
        notes += f' This file\'s content_type was regulatory_regions, but has been upgraded to genomic_elements.'
    if notes.strip() != '':
        value['notes'] = notes.strip()
    if value['content_type'] == 'regulatory_regions_genes':
        value['content_type'] = 'genomic_elements_genes'
        notes += f' This file\'s content_type was regulatory_regions_genes, but has been upgraded to genomic_elements_genes.'
    if notes.strip() != '':
        value['notes'] = notes.strip()
    if value['content_type'] == 'regulatory_regions_genes_biosamples':
        value['content_type'] = 'genomic_elements_genes_biosamples'
        notes += f' This file\'s content_type was regulatory_regions_genes_biosamples, but has been upgraded to genomic_elements_genes_biosamples.'
    if notes.strip() != '':
        value['notes'] = notes.strip()
    if value['content_type'] == 'regulatory_regions_genes_biosamples_donors':
        value['content_type'] = 'genomic_elements_genes_biosamples_donors'
        notes += f' This file\'s content_type was regulatory_regions_genes_biosamples_donors, but has been upgraded to genomic_elements_genes_biosamples_donors.'
    if notes.strip() != '':
        value['notes'] = notes.strip()
    if value['content_type'] == 'regulatory_regions_genes_biosamples_treatments_chebi':
        value['content_type'] = 'genomic_elements_genes_biosamples_treatments_chebi'
        notes += f' This file\'s content_type was regulatory_regions_genes_biosamples_treatments_chebi, but has been upgraded to genomic_elements_genes_biosamples_treatments_chebi.'
    if notes.strip() != '':
        value['notes'] = notes.strip()
    if value['content_type'] == 'regulatory_regions_genes_biosamples_treatments_proteins':
        value['content_type'] = 'genomic_elements_genes_biosamples_treatments_proteins'
        notes += f' This file\'s content_type was regulatory_regions_genes_biosamples_treatments_proteins, but has been upgraded to genomic_elements_genes_biosamples_treatments_proteins.'
    if notes.strip() != '':
        value['notes'] = notes.strip()
    if value['content_type'] == 'regulatory_regions_regulatory_regions':
        value['content_type'] = 'genomic_elements_genomic_elements'
        notes += f' This file\'s content_type was regulatory_regions_regulatory_regions, but has been upgraded to genomic_elements_genomic_elements.'
    if notes.strip() != '':
        value['notes'] = notes.strip()
    if value['content_type'] == 'variants_regulatory_regions':
        value['content_type'] = 'variants_genomic_elements'
        notes += f' This file\'s content_type was variants_regulatory_regions, but has been upgraded to variants_genomic_elements.'
    if notes.strip() != '':
        value['notes'] = notes.strip()


@upgrade_step('alignment_file', '13', '14')
@upgrade_step('genome_browser_annotation_file', '9', '10')
@upgrade_step('reference_file', '16', '17')
@upgrade_step('signal_file', '9', '10')
@upgrade_step('tabular_file', '13', '14')
def file_14_15(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2468
    notes = value.get('notes', '')
    if value.get('transcriptome_annotation') == 'GENCODE 28, GENCODE M17':
        value['transcriptome_annotation'] = 'GENCODE 32, GENCODE M23'
        notes += f'This object\'s transcriptome_annotation was GENCODE 28, GENCODE M17 but has been upgraded to GENCODE 32, GENCODE M23 as requested by the lab.'
        value['notes'] = notes.strip()
    return
