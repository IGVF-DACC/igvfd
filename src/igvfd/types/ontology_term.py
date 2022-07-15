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
    unique_key='ontology_term:name',
    properties={
        'title': 'Ontology term',
        'description': 'Ontology terms used by IGVF',
    })
class OntologyTerm(Item):
    base_types = ['OntologyTerm'] + Item.base_types
    schema = load_schema('igvfd:schemas/ontology_term.json')

    def unique_keys(self, properties):
        keys = super(OntologyTerm, self).unique_keys(properties)
        keys.setdefault('ontology_term:name', []).append(self.name(properties))
        return keys

    @property
    def __name__(self):
        return self.name()

    @calculated_property(schema={
        'title': 'Name',
        'type': 'string',
    })
    def name(self, properties=None):
        if properties is None:
            properties = self.upgrade_properties()
        format_cleaned_term_id = properties['term_id'].replace(' ', '_').replace(':', '_')
        return u'{}'.format(format_cleaned_term_id)

    @staticmethod
    def _get_ontology_slims(registry, term_id, slim_key):
        if term_id not in registry['ontology']:
            return []
        key = registry['ontology'][term_id].get(slim_key, [])
        return list(set(
            slim for slim in key
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

    @calculated_property(condition='term_id', schema={
        'title': 'Ancestors',
        'description': 'List of term names of ontological terms that precede the given term in the ontological tree. These ancestor terms are typically more general ontological terms under which the term is classified.',
        'type': 'array',
        'items': {
            'type': 'string',
        },
    })
    def ancestors(self, registry, term_id):
        return self._get_ontology_slims(registry, term_id, 'ancestors')


@collection(
    name='sample-terms',
    unique_key='sample_term:name',
    properties={
        'title': 'Sample ontology term',
        'description': 'Ontology terms used by IGVF for samples',
    })
class SampleTerm(OntologyTerm):
    item_type = 'sample_term'
    schema = load_schema('igvfd:schemas/sample_term.json')

    def unique_keys(self, properties):
        keys = super(OntologyTerm, self).unique_keys(properties)
        keys.setdefault('sample_term:name', []).append(self.name(properties))
        return keys

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
    name='assay-terms',
    unique_key='assay_term:name',
    properties={
        'title': 'Assay ontology term',
        'description': 'Ontology terms used by IGVF for assays',
    })
class AssayTerm(OntologyTerm):
    item_type = 'assay_term'
    schema = load_schema('igvfd:schemas/assay_term.json')

    def unique_keys(self, properties):
        keys = super(OntologyTerm, self).unique_keys(properties)
        keys.setdefault('assay_term:name', []).append(self.name(properties))
        return keys

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
    name='phenotype-terms',
    unique_key='phenotype_term:name',
    properties={
        'title': 'Phenotype ontology term',
        'description': 'Ontology terms used by IGVF for phenotypes, such as traits or diseases.',
    })
class PhenotypeTerm(OntologyTerm):
    item_type = 'phenotype_term'
    schema = load_schema('igvfd:schemas/phenotype_term.json')

    def unique_keys(self, properties):
        keys = super(OntologyTerm, self).unique_keys(properties)
        keys.setdefault('phenotype_term:name', []).append(self.name(properties))
        return keys
