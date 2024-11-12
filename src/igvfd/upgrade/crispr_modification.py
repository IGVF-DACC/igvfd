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


@upgrade_step('crispr_modification', '2', '3')
def crispr_modification_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1803
    notes = value.get('notes', '')
    if 'lot_id' in value and 'product_id' not in value:
        notes += f' Lot_id {value["lot_id"]} was removed from this modification.'
        del value['lot_id']
    if 'product_id' in value and 'sources' not in value:
        notes += f' Product_id {value["product_id"]} was removed from this modification.'
        del value['product_id']
        if 'lot_id' in value:
            notes += f' Lot_id {value["lot_id"]} was removed from this modification.'
            del value['lot_id']
    if notes:
        value['notes'] = notes.strip()


@upgrade_step('crispr_modification', '3', '4')
def crispr_modification_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-1908
    if 'tagged_protein' in value:
        value['tagged_proteins'] = [value['tagged_protein']]
        del value['tagged_protein']
