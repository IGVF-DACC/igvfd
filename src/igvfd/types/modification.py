from snovault import (
    collection,
    load_schema,
    calculated_property
)
from snovault.util import Path
from .base import (
    Item
)


@collection(
    name='modifications',
    properties={
        'title': 'Modifications',
        'description': 'Listing of modifications',
    }
)
class Modification(Item):
    item_type = 'modification'
    schema = load_schema('igvfd:schemas/modification.json')
    embedded_with_frame = [
        Path('award', include=['@id', 'component']),
        Path('lab', include=['@id', 'title']),
        Path('submitted_by', include=['@id', 'title']),
    ]

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, request, cas, cas_species, modality, fused_domain=None, tagged_protein=None):
        crispr_label_mapping = {
            'activation': 'CRISPRa',
            'base editing': 'CRISPR base editing',
            'cutting': 'CRISPR cutting',
            'interference': 'CRISPRi',
            'knockout': 'CRISPRko',
            'localizing': 'CRISPR localizing',
            'prime editing': 'CRISPR prime editing'
        }

        cas_label_mapping = {
            'SpG': 'G',
            'SpRY': 'RY'
        }

        cas_label = cas
        if cas in cas_label_mapping:
            cas_label = cas_label_mapping[cas]

        formatted_domain = ''
        if fused_domain:
            formatted_domain = f'-{fused_domain}'

        species = ''
        if cas_species:
            short = cas_species.split('(')[1].split(')')[0]
            species = f'{short}'

        summary = f'{crispr_label_mapping[modality]} {species}{cas_label}{formatted_domain}'
        if tagged_protein:
            tagged_protein_object = request.embed(tagged_protein, '@@object?skip_calculated=true')
            tagged_protein_symbol = tagged_protein_object.get('symbol')

            summary = f'{summary} fused to {tagged_protein_symbol}'

        return summary
