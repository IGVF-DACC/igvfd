from snovault import upgrade_step


@upgrade_step('cell_line', 'a', 'b')
@upgrade_step('differentiated_cell_line', 'a', 'b')
@upgrade_step('differentiated_tissue', 'a', 'b')
@upgrade_step('primary_cell', 'a', 'b')
@upgrade_step('whole_organism', 'a', 'b')
def biosample_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-249
