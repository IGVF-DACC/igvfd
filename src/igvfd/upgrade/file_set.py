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


@upgrade_step('construct_library', '1', '2')
def construct_library_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-474
    plasmid_map = value.get('plasmid_map', None)
    if plasmid_map is None:
        return
    else:
        if 'documents' in value:
            value['documents'].append(value['plasmid_map'])
            del value['plasmid_map']


@upgrade_step('construct_library', '2', '3')
def construct_library_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-849
    notes = value.get('notes', '')
    if 'expression_vector_library_details' not in value:
        if 'guide_library_details' not in value:
            if 'reporter_library_details' not in value:
                value['guide_library_details'] = {'guide_type': 'sgRNA'}
                notes += f' guide_library_details added via upgrade; update before removing note.'
                value['notes'] = notes.strip()
    if 'origins' not in value:
        value['origins'] = ['TF binding sites']
        notes += f' origins added via upgrade; update before removing note.'
        value['notes'] = notes.strip()


@upgrade_step('measurement_set', '4', '5')
def measurement_set_4_5(value, system):
    # https://igvf.atlassian.net/browse/IGVF-679
    notes = value.get('notes', '')
    if 'seqspec' in value:
        seqspec = value['seqspec']
        notes += f' This meausurement_set previously linked to {seqspec}, but the property for submitting associated seqspec links has been moved to SequenceFile where it should be submitted as a link to the seqspec yaml file submitted as a ConfigurationFile instead.'
        value['notes'] = notes.strip()
        del value['seqspec']


@upgrade_step('construct_library', '3', '4')
def construct_library_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-860
    if 'origins' in value:
        value['selection_criteria'] = value['origins']
        del value['origins']


@upgrade_step('construct_library', '4', '5')
@upgrade_step('curated_set', '3', '4')
@upgrade_step('prediction', '1', '2')
@upgrade_step('model', '1', '2')
@upgrade_step('auxiliary_set', '1', '2')
def file_set_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-802
    if 'references' in value:
        value['publication_identifiers'] = value['references']
        del value['references']
