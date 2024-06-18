from snovault import upgrade_step


@upgrade_step('crispr_modification', '1', '2')
def crispr_modification_5_6(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1423
    old_to_new = {
        'KRAB': 'ZIM3-KRAB',
        'ZIM3': 'ZIM3-KRAB',
        'VPR': 'VP64-p65-Rta (VPR)',
    }
    if 'fused_domain' in value:
        old_fused_domain = value['fused_domain']
        if old_fused_domain in old_to_new:
            value['fused_domain'] = old_to_new[old_fused_domain]
            if 'notes' in value:
                value['notes'] = f"{value['notes']}. Fused_domain enum {old_fused_domain} has been renamed to be {old_to_new[old_fused_domain]}."
            else:
                value['notes'] = f'Fused_domain enum {old_fused_domain} has been renamed to be {old_to_new[old_fused_domain]}.'
    return
