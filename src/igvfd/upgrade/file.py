from snovault import upgrade_step


@upgrade_step('reference_data', '1', '2')
@upgrade_step('sequence_data', '1', '2')
def file_1_2(value, system):
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
    if 'dbxrefs' in value:
        value['dbxref'] = value['dbxrefs']
        del value['dbxrefs']
