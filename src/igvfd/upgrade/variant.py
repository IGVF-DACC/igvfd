from snovault import upgrade_step


@upgrade_step('human_genomic_variant', '1', '2')
def human_genomic_variant_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-538
    if 'refseq_id' in value:
        if value['refseq_id'][9] != '.':
            new_refseq_id = list(value['refseq_id'])
            new_refseq_id[9] = '.'
            new_refseq_id = ''.join(new_refseq_id)
            value['notes'] = f"This human genomic variant's `refseq_id` was originally {value['refseq_id']}, but was changed to {new_refseq_id} due to an upgrade in the regex pattern for the property."
            value['refseq_id'] = new_refseq_id


@upgrade_step('human_genomic_variant', '2', '3')
def human_genomic_variant_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1170
    if 'description' in value:
        if value['description'] == '':
            del value['description']


@upgrade_step('human_genomic_variant', '3', '4')
def human_genomic_variant_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1494
    if value['status'] in ['released', 'archived'] and 'release_timestamp' not in value:
        value['release_timestamp'] = '2024-03-06T12:34:56Z'
        notes = value.get('notes', '')
        notes += f'This object\'s release_timestamp has been set to 2024-03-06T12:34:56Z'
        value['notes'] = notes.strip()
