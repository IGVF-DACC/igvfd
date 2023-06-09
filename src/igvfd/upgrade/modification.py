from snovault import upgrade_step


@upgrade_step('modification', '1', '2')
def modification_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-729
    if 'cas_species' not in value:
        new_notes = value.get('notes', '')
        new_notes += 'For upgrade, cas_species has been automatically designated as Streptococcus pyogenes (Sp), follow up with associated lab to check if upgrade is valid.'
        value['notes'] = new_notes.strip()
        value['cas_species'] = 'Streptococcus pyogenes (Sp)'
