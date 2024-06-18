from snovault import upgrade_step


@upgrade_step('crispr_modification', '1', '2')
def crispr_modification_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1423
    old_to_new = {
        'ZIM3': 'ZIM3-KRAB',
        'VPR': 'VP64-p65-Rta (VPR)',
    }
    sentence_end = ''
    if 'fused_domain' in value:
        if value['fused_domain'] == 'KRAB':
            old_fused_domain = 'KRAB'
            value.pop('fused_domain')
            sentence_end = 'removed'
        elif value['fused_domain'] in old_to_new:
            old_fused_domain = value['fused_domain']
            sentence_end = f'renamed to be {old_to_new[old_fused_domain]}'
            value['fused_domain'] = old_to_new[old_fused_domain]
    if sentence_end != '':
        notes = value.get('notes', '')
        notes += f'Fused_domain enum {old_fused_domain} has been {sentence_end}.'
        value['notes'] = notes.strip()
