from snovault import upgrade_step


@upgrade_step('crispr_modification', '1', '2')
def crispr_modification_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1423
    old_to_new = {
        'ZIM3': 'ZIM3-KRAB',
        'VPR': 'VP64-p65-Rta (VPR)',
    }
    if 'fused_domain' in value:
        if value['fused_domain'] == 'KRAB':
            value.pop('fused_domain', None)
            sentence_end = 'removed'
        else:
            old_fused_domain = value['fused_domain']
            sentence_end = f'renamed to be {old_to_new[old_fused_domain]}.'
            if old_fused_domain in old_to_new:
                value['fused_domain'] = old_to_new[old_fused_domain]
                if 'notes' in value:
                    value['notes'] = f"{value['notes']}. Fused_domain enum {old_fused_domain} has been {sentence_end}."
                else:
                    value['notes'] = f'Fused_domain enum {old_fused_domain} has been {sentence_end}.'
    return
