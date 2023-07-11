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
