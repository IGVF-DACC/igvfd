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


@collection(
    name='sample-ontology-terms',
    unique_key='term_id',
    properties={
        'title': 'Sample ontology term',
        'description': 'Ontology terms used by IGVF for samples',
    })
class SampleOntologyTerm(OntologyTerm):
    item_type = 'sample_ontology_term'
    schema = load_schema('igvfd:schemas/sample_ontology_term.json')

    @calculated_property(condition='term_id', schema={
        'title': 'Organ',
        'type': 'array',
        'items': {
            'type': 'string',
        },
    })
    def organ_slims(self, registry, term_id):
        return self._get_ontology_slims(registry, term_id, 'organs')

    @calculated_property(condition='term_id', schema={
        'title': 'Cell',
        'type': 'array',
        'items': {
            'type': 'string',
        },
    })
    def cell_slims(self, registry, term_id):
        return self._get_ontology_slims(registry, term_id, 'cells')

    @calculated_property(condition='term_id', schema={
        'title': 'Developmental slims',
        'type': 'array',
        'items': {
            'type': 'string',
        },
    })
    def developmental_slims(self, registry, term_id):
        return self._get_ontology_slims(registry, term_id, 'developmental')

    @calculated_property(condition='term_id', schema={
        'title': 'System slims',
        'type': 'array',
        'items': {
            'type': 'string',
        },
    })
    def system_slims(self, registry, term_id):
        return self._get_ontology_slims(registry, term_id, 'systems')


@collection(
    name='assay-ontology-terms',
    unique_key='term_id',
    properties={
        'title': 'Assay ontology term',
        'description': 'Ontology terms used by IGVF for assays',
    })
class AssayOntologyTerm(OntologyTerm):
    item_type = 'assay_ontology_term'
    schema = load_schema('igvfd:schemas/assay_ontology_term.json')

    @calculated_property(condition='term_id', schema={
        'title': 'Assay category',
        'type': 'array',
        'items': {
            'type': 'string',
        },
    })
    def category_slims(self, registry, term_id):
        return self._get_ontology_slims(registry, term_id, 'assay')


@collection(
    name='disease-ontology-terms',
    unique_key='term_id',
    properties={
        'title': 'Disease ontology term',
        'description': 'Ontology terms used by IGVF for diseases',
    })
class DiseaseOntologyTerm(OntologyTerm):
    item_type = 'disease_ontology_term'
    schema = load_schema('igvfd:schemas/disease_ontology_term.json')


@collection(
    name='trait-ontology-terms',
    unique_key='term_id',
    properties={
        'title': 'Trait ontology term',
        'description': 'Ontology terms used by IGVF for traits',
    })
class TraitOntologyTerm(OntologyTerm):
    item_type = 'trait_ontology_term'
    schema = load_schema('igvfd:schemas/trait_ontology_term.json')
