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
@upgrade_step('configuration_file', '7', '8')
@upgrade_step('genome_browser_annotation_file', '8', '9')
@upgrade_step('image_file', '4', '5')
@upgrade_step('matrix_file', '6', '7')
@upgrade_step('reference_file', '12', '13')
@upgrade_step('sequence_file', '11', '12')
@upgrade_step('signal_file', '8', '9')
@upgrade_step('tabular_file', '8', '9')
def file_12_13(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1531
