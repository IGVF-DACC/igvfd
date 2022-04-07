from snovault import (
    calculated_property,
    abstract_collection,
    collection,
    load_schema,
)

from .base import (
    Item,
)


@abstract_collection(
    name='ontology-terms',
    unique_key='term_id',
    properties={
        'title': 'Ontology term',
        'description': 'Ontology terms used by IGVF',
    })
class OntologyTerm(Item):
    base_types = ['OntologyTerm'] + Item.base_types
    schema = load_schema('igvfd:schemas/ontology_term.json')
    embedded = []
    embedded_with_frame = []

    @staticmethod
    def _get_ontology_slims(registry, term_id, slim_key):
        if term_id not in registry['ontology']:
            return []
        return list(set(
            slim for slim in registry['ontology'][term_id][slim_key]
        ))

    @calculated_property(condition='term_id', schema={
        'title': 'Synonyms',
        'type': 'array',
        'items': {
            'type': 'string',
        },
    })
    def synonyms(self, registry, term_id):
        return self._get_ontology_slims(registry, term_id, 'synonyms')
