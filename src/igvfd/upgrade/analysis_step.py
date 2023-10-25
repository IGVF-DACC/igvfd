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
