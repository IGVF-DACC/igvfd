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


@upgrade_step('open_reading_frame', '2', '3')
def open_reading_frame_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1792
    if gene := value.pop('gene', None):
        value['genes'] = gene
        new_note = 'This object used gene as a property, which is now upgraded to genes.'
        if notes := value.get('notes', ''):
            new_note = f'{notes} {new_note}'
        value['notes'] = new_note
    return
