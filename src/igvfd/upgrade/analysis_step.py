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
