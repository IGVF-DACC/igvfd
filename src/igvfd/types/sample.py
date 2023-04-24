from snovault import (
    abstract_collection,
    calculated_property,
    collection,
    load_schema,
)
from snovault.util import Path
from .base import (
    Item,
    paths_filtered_by_status
)


@abstract_collection(
    name='samples',
    unique_key='accession',
    properties={
        'title': 'Samples',
        'description': 'Listing of samples',
    }
)
class Sample(Item):
    item_type = 'sample'
    base_types = ['Sample'] + Item.base_types
    name_key = 'accession'
    schema = load_schema('igvfd:schemas/sample.json')
    rev = {
        'file_sets': ('FileSet', 'samples')
    }

    @calculated_property(schema={
        'title': 'File Sets',
        'type': 'array',
        'items': {
            'type': ['string', 'object'],
            'linkFrom': 'FileSet.samples',
        },
    })
    def file_sets(self, request, file_sets):
        return paths_filtered_by_status(request, file_sets)


@abstract_collection(
    name='biosamples',
    unique_key='accession',
    properties={
        'title': 'Biosamples',
        'description': 'Listing of biosamples',
    }
)
class Biosample(Sample):
    item_type = 'biosample'
    base_types = ['Biosample'] + Sample.base_types
    schema = load_schema('igvfd:schemas/biosample.json')

    @calculated_property(
        schema={
            'title': 'Sex',
            'type': 'string',
            'enum': [
                'female',
                'male',
                'mixed',
                'unspecified'
            ],
            'notSubmittable': True,
        }
    )
    def sex(self, request, donors=None):
        sexes = set()
        if donors:
            for d in donors:
                donor_object = request.embed(d, '@@object')
                if donor_object.get('sex'):
                    sexes.add(donor_object.get('sex'))
        if len(sexes) == 1:
            return list(sexes).pop()
        elif len(sexes) > 1:
            return 'mixed'

    @calculated_property(
        define=True,
        schema={
            'title': 'Age',
            'description': 'Age of organism at the time of collection of the sample.',
            'type': 'string',
            'pattern': '^((\\d+(\\.[1-9])?(\\-\\d+(\\.[1-9])?)?)|(unknown)|([1-8]?\\d)|(90 or above))$',
            'notSubmittable': True,
        }
    )
    def age(self, lower_bound_age=None, upper_bound_age=None, age_units=None):
        if lower_bound_age and upper_bound_age:
            if lower_bound_age == upper_bound_age:
                if lower_bound_age == 90 and upper_bound_age == 90 and age_units == 'year':
                    return '90 or above'
                return str(lower_bound_age)
            return str(lower_bound_age) + '-' + str(upper_bound_age)
        else:
            return 'unknown'

    @calculated_property(
        schema={
            'title': 'Taxa',
            'type': 'string',
            'enum': [
                    'Homo sapiens',
                    'Mus musculus'
            ],
            'notSubmittable': True
        }
    )
    def taxa(self, request, donors=None):
        taxas = set()
        if donors:
            for d in donors:
                donor_object = request.embed(d, '@@object')
                if donor_object.get('taxa'):
                    taxas.add(donor_object.get('taxa'))
        # if taxas equate:
        if len(taxas) == 1:
            return list(taxas).pop()
        # if taxa are mixed:
        elif len(taxas) > 1:
            return None

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, request, biosample_term, taxa, age, age_units=None):
        sample_term_object = request.embed(biosample_term, '@@object?skip_calculated=true')
        term_name = sample_term_object.get('term_name')
        biosample_type = self.item_type.replace('_', ' ')
        term_and_type = f'{term_name} {biosample_type}'
        if 'cell' in biosample_type and 'cell' in term_name:
            term_and_type = term_name
        if 'tissue' in biosample_type and 'tissue' in term_name:
            term_and_type = term_name
        if age == 'unknown':
            return f'{term_and_type}, {taxa}'
        else:
            if age != '1':
                age_units = f'{age_units}s'
            return f'{term_and_type}, {taxa} ({age} {age_units})'


@collection(
    name='primary-cells',
    unique_key='accession',
    properties={
        'title': 'Primary Cells',
        'description': 'Listing of primary cells',
    }
)
class PrimaryCell(Biosample):
    item_type = 'primary_cell'
    schema = load_schema('igvfd:schemas/primary_cell.json')
    embedded = ['treatments']
    embedded_with_frame = [
        Path('award', include=['@id', 'component']),
        Path('biosample_term', include=['@id', 'term_name']),
        Path('disease_terms', include=['@id', 'term_name']),
        Path('lab', include=['@id', 'title']),
        Path('source', include=['@id', 'title']),
    ]


@collection(
    name='in-vitro-systems',
    unique_key='accession',
    properties={
         'title': 'In Vitro Systems',
         'description': 'Listing of in vitro systems',
    })
class InVitroSystem(Biosample):
    item_type = 'in_vitro_system'
    schema = load_schema('igvfd:schemas/in_vitro_system.json')
    embedded_with_frame = [
        Path('award', include=['@id', 'component']),
        Path('biosample_term', include=['@id', 'term_name']),
        Path('disease_terms', include=['@id', 'term_name']),
        Path('lab', include=['@id', 'title']),
        Path('source', include=['@id', 'title']),
        Path('treatments', include=['@id', 'treatment_term_name']),
    ]

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, request, biosample_term, taxa, classification, time_post_factors_introduction=None, time_post_factors_introduction_units=None):
        sample_term_object = request.embed(biosample_term, '@@object?skip_calculated=true')
        term_name = sample_term_object.get('term_name')
        term_and_classification = f'{term_name} {classification}'
        if classification in term_name:
            term_and_classification = term_name
        elif 'cell' in classification and 'cell' in term_name:
            term_and_classification = term_name.replace('cell', classification)
        elif 'tissue' in classification and 'tissue' in term_name:
            term_and_classification = term_name.replace('tissue', classification)
        if time_post_factors_introduction and time_post_factors_introduction_units:
            if time_post_factors_introduction != 1:
                time_post_factors_introduction_units = f'{time_post_factors_introduction_units}s'
            return f'{term_and_classification}, {taxa} ({time_post_factors_introduction} {time_post_factors_introduction_units})'
        else:
            return f'{term_and_classification}, {taxa}'


@collection(
    name='tissues',
    unique_key='accession',
    properties={
        'title': 'Tissues',
        'description': 'Listing of tissues',
    }
)
class Tissue(Biosample):
    item_type = 'tissue'
    schema = load_schema('igvfd:schemas/tissue.json')
    embedded_with_frame = [
        Path('award', include=['@id', 'component']),
        Path('biosample_term', include=['@id', 'term_name']),
        Path('disease_terms', include=['@id', 'term_name']),
        Path('lab', include=['@id', 'title']),
        Path('source', include=['@id', 'title']),
    ]


@collection(
    name='technical-samples',
    unique_key='accession',
    properties={
        'title': 'Technical Samples',
        'description': 'Listing of technical samples',
    }
)
class TechnicalSample(Sample):
    item_type = 'technical_sample'
    schema = load_schema('igvfd:schemas/technical_sample.json')
    embedded_with_frame = [
        Path('award', include=['@id', 'name', 'component']),
        Path('lab', include=['@id', 'title']),
        Path('source', include=['@id', 'title']),
        Path('technical_sample_term', include=['@id', 'term_name']),
    ]

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, request, technical_sample_term, sample_material):
        sample_term_object = request.embed(technical_sample_term, '@@object?skip_calculated=true')
        term_name = sample_term_object.get('term_name')
        return f'{sample_material} {term_name}'


@collection(
    name='whole-organisms',
    unique_key='accession',
    properties={
        'title': 'Whole Organism Samples',
        'description': 'Listing of whole organism samples',
    }
)
class WholeOrganism(Biosample):
    item_type = 'whole_organism'
    schema = load_schema('igvfd:schemas/whole_organism.json')
    embedded_with_frame = [
        Path('award', include=['@id', 'component']),
        Path('biomarkers', include=['@id', 'classification']),
        Path('biosample_term', include=['@id', 'term_name']),
        Path('disease_terms', include=['@id', 'term_name']),
        Path('lab', include=['@id', 'title']),
        Path('source', include=['@id', 'title']),
        Path('treatments', include=['@id', 'treatment_type']),
    ]

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, request, biosample_term, taxa, age, age_units=None):
        sample_term_object = request.embed(biosample_term, '@@object?skip_calculated=true')
        term_name = sample_term_object.get('term_name')
        if age == 'unknown':
            return f'{term_name}, {taxa}'
        else:
            if age != '1':
                age_units = age_units + 's'
            return f'{term_name}, {taxa} ({age} {age_units})'
