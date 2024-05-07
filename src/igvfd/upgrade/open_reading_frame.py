from snovault import upgrade_step


@upgrade_step('open_reading_frame', '1', '2')
def open_reading_frame_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1622
    notes = value.get('notes', '')
    if 'award' not in value and 'lab' not in value:
        value['award'] = '/awards/HG012012'
        value['lab'] = '/labs/j-michael-cherry'
        if 'notes' in value:
            value['notes'] = f'{value.get("notes")}. This object does not have award and lab specified previously, it was upgraded to have Cherry lab/award.'
        else:
            value['notes'] = 'This object does not have award and lab specified previously, it was upgraded to have Cherry lab/award.'
    return
