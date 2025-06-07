from snovault import upgrade_step


@upgrade_step('analysis_step', '1', '2')
def analysis_step_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1212
    notes = value.get('notes', '')
    if 'parents' in value and len(value['parents']) == 0:
        del value['parents']
    if len(value['input_content_types']) == 0:
        value['input_content_types'] = ['reads']
        notes += f' "Reads" was added to input_content_types, which was previously an empty array.'
    if len(value['output_content_types']) == 0:
        value['output_content_types'] = ['reads']
        notes += f' "Reads" was added to output_content_types, which was previously an empty array.'
    if len(value['analysis_step_types']) == 0:
        value['analysis_step_types'] = ['alignment']
        notes += f' "Alignment" was added to analysis_step_types, which was previously an empty array.'
    if notes != '':
        value['notes'] = notes.strip()


@upgrade_step('analysis_step', '2', '3')
def analysis_step_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1219
    notes = value.get('notes', '')
    if 'lab' not in value:
        value['lab'] = '/labs/j-michael-cherry/'
        notes += f' This object\'s lab was missing and has been set to j-michael-cherry as a placeholder.'
    if 'award' not in value:
        value['award'] = '/awards/HG012012/'
        notes += f' This object\'s award was missing and has been set to HG012012 as a placeholder.'
    if notes != '':
        value['notes'] = notes.strip()


@upgrade_step('analysis_step', '3', '4')
def analysis_step_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1170
    if 'description' in value:
        if value['description'] == '':
            del value['description']


@upgrade_step('analysis_step', '4', '5')
def analysis_step_4_5(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1494
    if value['status'] in ['released', 'archived'] and 'release_timestamp' not in value:
        value['release_timestamp'] = '2024-03-06T12:34:56Z'
        notes = value.get('notes', '')
        notes += f'This object\'s release_timestamp has been set to 2024-03-06T12:34:56Z'
        value['notes'] = notes.strip()


@upgrade_step('analysis_step', '5', '6')
def analysis_step_5_6(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2253
    notes = value.get('notes', '')
    for key in ['input_content_types', 'output_content_types']:
        if 'sequence barcodes' in value[key]:
            new_content_list = ['barcode onlist' if content ==
                                'sequence barcodes' else content for content in value[key]]
            value[key] = sorted(set(new_content_list))
            notes += f' "sequence barcodes" was removed from {key}, and has been upgraded to "barcode onlist".'
    if notes != '':
        value['notes'] = notes.strip()


@upgrade_step('analysis_step', '6', '7')
def analysis_step_6_7(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2718
    notes = value.get('notes', '')
    old_enum = 'comprehensive gene count matrix'
    new_enum = 'kallisto single cell RNAseq output'
    for key in ['input_content_types', 'output_content_types']:
        if old_enum in value[key]:
            new_content_list = [new_enum if content == old_enum else content for content in value[key]]
            value[key] = sorted(set(new_content_list))
            notes += f' "{old_enum}" was removed from {key}, and has been upgraded to "{new_enum}".'
    if notes != '':
        value['notes'] = notes.strip()


@upgrade_step('analysis_step', '7', '8')
def analysis_step_7_8(value, system):
    # https://igvf.atlassian.net/browse/IGVF-2733
    notes = value.get('notes', '')
    old_enum = 'variant functional predictions'
    new_enum = 'variant functions'
    for key in ['input_content_types', 'output_content_types']:
        if old_enum in value[key]:
            new_content_list = [new_enum if content == old_enum else content for content in value[key]]
            value[key] = sorted(set(new_content_list))
            notes += f' "{old_enum}" was removed from {key}, and has been upgraded to "{new_enum}".'
    if notes != '':
        value['notes'] = notes.strip()
    old_enum = 'element to gene predictions'
    new_enum = 'element to gene interactions'
    for key in ['input_content_types', 'output_content_types']:
        if old_enum in value[key]:
            new_content_list = [new_enum if content == old_enum else content for content in value[key]]
            value[key] = sorted(set(new_content_list))
            notes += f' "{old_enum}" was removed from {key}, and has been upgraded to "{new_enum}".'
    if notes != '':
        value['notes'] = notes.strip()
