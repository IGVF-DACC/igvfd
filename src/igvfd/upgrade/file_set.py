from snovault import upgrade_step


@upgrade_step('analysis_set', '1', '2')
@upgrade_step('curated_set', '1', '2')
@upgrade_step('measurement_set', '1', '2')
def file_set_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-321
    if 'aliases' in value:
        value['alias'] = value['aliases']
        del value['aliases']
    if 'alternate_accessions' in value:
        value['alternate_accession'] = value['alternate_accessions']
        del value['alternate_accessions']
    if 'collections' in value:
        value['collection'] = value['collections']
        del value['collections']
    if 'documents' in value:
        value['document'] = value['documents']
        del value['documents']
    if 'references' in value:
        value['reference'] = value['references']
        del value['references']
