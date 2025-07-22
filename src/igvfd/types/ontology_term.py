from snovault import (
    calculated_property,
    abstract_collection,
    collection,
    load_schema,
)

from .base import (
    Item,
)
from snovault.util import Path


@abstract_collection(
    name='ontology-terms',
    unique_key='ontology_term:name',
    properties={
        'title': 'Ontology Terms',
        'description': 'Ontology terms used by IGVF',
    }
)
class OntologyTerm(Item):
    base_types = ['OntologyTerm'] + Item.base_types
    schema = load_schema('igvfd:schemas/ontology_term.json')
    embedded_with_frame = [
        Path('submitted_by', include=['@id', 'title']),
    ]

    set_status_up = []
    set_status_down = []

    def unique_keys(self, properties):
        keys = super(OntologyTerm, self).unique_keys(properties)
        if 'deprecated_ntr_terms' in properties:
            keys.setdefault('alias', []).extend(properties['deprecated_ntr_terms'])
        keys.setdefault('ontology_term:name', []).append(self.name(properties))
        return keys

    @property
    def __name__(self):
        return self.name()

    @calculated_property(schema={
        'title': 'Name',
        'type': 'string',
        'description': 'A unique identifier for the ontology term, reformatted from the original term ID.',
        'notSubmittable': True,
        'uniqueKey': True
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
        slim_list = sorted(set(
            slim for slim in key
        ))
        return slim_list or None

    @staticmethod
    def _get_ontology_string(registry, term_id, string_key):
        if term_id not in registry['ontology']:
            return ''
        return registry['ontology'][term_id].get(string_key, '')

    @calculated_property(
        condition='term_id',
        schema={
            'title': 'Definition',
            'type': 'string',
            'description': 'Definition for the term that was recorded in an ontology.',
            'notSubmittable': True,
        }
    )
    def definition(self, registry, term_id):
        return self._get_ontology_string(registry, term_id, 'definition')

    @calculated_property(
        condition='term_id',
        schema={
            'title': 'Comments',
            'type': 'array',
            'description': 'Comment for the term that was recorded in an ontology.',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'type': 'string',
            },
            'notSubmittable': True,
        }
    )
    def comments(self, registry, term_id):
        return self._get_ontology_slims(registry, term_id, 'comments')

    @calculated_property(
        condition='term_id',
        schema={
            'title': 'Synonyms',
            'type': 'array',
            'description': 'Synonyms for the term that have been recorded in an ontology.',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'type': 'string',
            },
            'notSubmittable': True,
        }
    )
    def synonyms(self, registry, term_id):
        return self._get_ontology_slims(registry, term_id, 'synonyms')

    @calculated_property(
        condition='term_id',
        schema={
            'title': 'Ancestors',
            'description': 'List of term names of ontological terms that precede the given term in the ontological tree. These ancestor terms are typically more general ontological terms under which the term is classified.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'type': 'string',
            },
            'notSubmittable': True,
        }
    )
    def ancestors(self, registry, term_id):
        return self._get_ontology_slims(registry, term_id, 'ancestors')

    @calculated_property(schema={
        'title': 'Ontology',
        'type': 'string',
        'description': 'The ontology in which the term is recorded.',
        'notSubmittable': True,
    })
    def ontology(self, properties=None):
        if properties is None:
            properties = self.upgrade_properties()
        return properties['term_id'].split(':')[0]

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'description': 'A summary of the ontology term.',
            'notSubmittable': True,
        }
    )
    def summary(self, term_name):
        return term_name


@collection(
    name='sample-terms',
    unique_key='sample_term:name',
    properties={
        'title': 'Sample Ontology Terms',
        'description': 'Ontology terms used by IGVF for samples',
    }
)
class SampleTerm(OntologyTerm):
    item_type = 'sample_term'
    schema = load_schema('igvfd:schemas/sample_term.json')
    embedded_with_frame = OntologyTerm.embedded_with_frame

    def unique_keys(self, properties):
        keys = super(OntologyTerm, self).unique_keys(properties)
        if 'deprecated_ntr_terms' in properties:
            keys.setdefault('alias', []).extend(properties['deprecated_ntr_terms'])
        keys.setdefault('sample_term:name', []).append(self.name(properties))
        return keys

    @calculated_property(
        condition='term_id',
        schema={
            'title': 'Organ',
            'type': 'array',
            'description': 'Organs associated with the sample term.',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'type': 'string',
            },
            'notSubmittable': True,
        }
    )
    def organ_slims(self, registry, term_id):
        return self._get_ontology_slims(registry, term_id, 'organs')

    @calculated_property(
        condition='term_id',
        schema={
            'title': 'Cell',
            'type': 'array',
            'description': 'Cells associated with the sample term.',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'type': 'string',
            },
            'notSubmittable': True,
        }
    )
    def cell_slims(self, registry, term_id):
        return self._get_ontology_slims(registry, term_id, 'cells')

    @calculated_property(
        condition='term_id',
        schema={
            'title': 'Developmental Slims',
            'type': 'array',
            'description': 'Developmental stages associated with the sample term.',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'type': 'string',
            },
            'notSubmittable': True,
        }
    )
    def developmental_slims(self, registry, term_id):
        return self._get_ontology_slims(registry, term_id, 'developmental')

    @calculated_property(
        condition='term_id',
        schema={
            'title': 'System Slims',
            'type': 'array',
            'description': 'Organ systems associated with the sample term.',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'type': 'string',
            },
            'notSubmittable': True,
        }
    )
    def system_slims(self, registry, term_id):
        return self._get_ontology_slims(registry, term_id, 'systems')


@collection(
    name='assay-terms',
    unique_key='assay_term:name',
    properties={
        'title': 'Assay Ontology Terms',
        'description': 'Ontology terms used by IGVF for assays',
    }
)
class AssayTerm(OntologyTerm):
    item_type = 'assay_term'
    schema = load_schema('igvfd:schemas/assay_term.json')
    embedded_with_frame = OntologyTerm.embedded_with_frame

    def unique_keys(self, properties):
        keys = super(OntologyTerm, self).unique_keys(properties)
        if 'deprecated_ntr_terms' in properties:
            keys.setdefault('alias', []).extend(properties['deprecated_ntr_terms'])
        keys.setdefault('assay_term:name', []).append(self.name(properties))
        return keys

    @calculated_property(
        condition='term_id',
        schema={
            'title': 'Assay Type',
            'type': 'array',
            'description': 'A broad categorization of the assay term.',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'type': 'string',
            },
            'notSubmittable': True,
        }
    )
    def assay_slims(self, registry, term_id):
        slims = self._get_ontology_slims(registry, term_id, 'assay')
        if slims:
            return slims
        else:
            return ['no category']

    @calculated_property(
        condition='term_id',
        schema={
            'title': 'Assay Category',
            'type': 'array',
            'description': 'The type of feature or interaction measured by the assay.',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'type': 'string',
            },
            'notSubmittable': True,
        }
    )
    def category_slims(self, registry, term_id):
        return self._get_ontology_slims(registry, term_id, 'category')

    @calculated_property(
        condition='term_id',
        schema={
            'title': 'Assay Objective',
            'type': 'array',
            'description': 'The purpose of the assay.',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'type': 'string',
            },
            'notSubmittable': True,
        }
    )
    def objective_slims(self, registry, term_id):
        return self._get_ontology_slims(registry, term_id, 'objectives')


@collection(
    name='phenotype-terms',
    unique_key='phenotype_term:name',
    properties={
        'title': 'Phenotype Ontology Terms',
        'description': 'Ontology terms used by IGVF for phenotypes, such as traits or diseases.',
    }
)
class PhenotypeTerm(OntologyTerm):
    item_type = 'phenotype_term'
    schema = load_schema('igvfd:schemas/phenotype_term.json')
    embedded_with_frame = OntologyTerm.embedded_with_frame

    def unique_keys(self, properties):
        keys = super(OntologyTerm, self).unique_keys(properties)
        if 'deprecated_ntr_terms' in properties:
            keys.setdefault('alias', []).extend(properties['deprecated_ntr_terms'])
        keys.setdefault('phenotype_term:name', []).append(self.name(properties))
        return keys


@collection(
    name='platform-terms',
    unique_key='platform_term:name',
    properties={
        'title': 'Platform Ontology Terms',
        'description': 'Ontology terms used by IGVF for platforms used for library construction or sequencing.',
    }
)
class PlatformTerm(OntologyTerm):
    item_type = 'platform_term'
    schema = load_schema('igvfd:schemas/platform_term.json')
    embedded_with_frame = OntologyTerm.embedded_with_frame

    def unique_keys(self, properties):
        keys = super(OntologyTerm, self).unique_keys(properties)
        if 'deprecated_ntr_terms' in properties:
            keys.setdefault('alias', []).extend(properties['deprecated_ntr_terms'])
        keys.setdefault('platform_term:name', []).append(self.name(properties))
        return keys
