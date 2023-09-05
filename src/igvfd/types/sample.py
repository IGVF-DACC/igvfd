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


def collect_multiplexed_samples_prop(request, multiplexed_samples, property_name):
    property_set = set()
    for sample in multiplexed_samples:
        sample_props = request.embed(sample, '@@object?skip_calculated=true')
        property_contents = sample_props.get(property_name, None)
        if property_contents:
            if type(property_contents) == list:
                for item in property_contents:
                    property_set.add(item)
            else:
                property_set.add(property_contents)
    property_list = sorted(property_set)
    return property_list


def concat_numeric_and_units(numeric, numeric_units, no_numeric_on_one=False):
    if str(numeric) == '1':
        if no_numeric_on_one:
            return f'{numeric_units}'
        else:
            return f'{numeric} {numeric_units}'
    else:
        return f'{numeric} {numeric_units}s'


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
        'file_sets': ('FileSet', 'samples'),
        'multiplexed_in': ('MultiplexedSample', 'multiplexed_samples')
    }
    embedded_with_frame = [
        Path('award', include=['@id', 'component']),
        Path('lab', include=['@id', 'title']),
        Path('sources', include=['@id', 'title']),
        Path('submitted_by', include=['@id', 'title']),
        Path('sorted_fraction', include=['@id', 'accession']),
        Path('file_sets', include=['@id', 'accession', 'aliases', 'lab', 'status']),
        Path('file_sets.lab', include=['title']),
        Path('multiplexed_in', include=['@id', 'accession'])
    ]

    @calculated_property(schema={
        'title': 'File Sets',
        'type': 'array',
        'items': {
            'type': ['string', 'object'],
            'linkFrom': 'FileSet.samples',
        },
        'notSubmittable': True,
    })
    def file_sets(self, request, file_sets):
        return paths_filtered_by_status(request, file_sets)

    @calculated_property(schema={
        'title': 'Multiplexed In',
        'type': 'array',
        'items': {
            'type': ['string', 'object'],
            'linkFrom': 'MultiplexedSample.multiplexed_samples',
        },
        'notSubmittable': True,
    })
    def multiplexed_in(self, request, multiplexed_in):
        return paths_filtered_by_status(request, multiplexed_in)


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
    embedded_with_frame = Sample.embedded_with_frame + [
        Path('sample_terms', include=['@id', 'term_name']),
        Path('disease_terms', include=['@id', 'term_name']),
        Path('treatments', include=['@id', 'purpose', 'treatment_type', 'summary', 'status']),
        Path('modifications', include=['@id', 'modality', 'summary', 'status'])
    ]

    @calculated_property(
        define=True,
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
        define=True,
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
    def taxa(self, request, donors):
        taxas = set()
        if donors:
            for d in donors:
                donor_object = request.embed(d, '@@object?skip_calculated=true')
                if donor_object.get('taxa'):
                    taxas.add(donor_object.get('taxa'))

        if len(taxas) == 1:
            return list(taxas).pop()

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, request, sample_terms, donors, sex, age, age_units=None, embryonic=None, virtual=None, classification=None, cellular_sub_pool=None, time_post_change=None, time_post_change_units=None, targeted_sample_term=None, taxa=None, sorted_fraction_detail=None, biomarkers=None, treatments=None):
        term_object = request.embed(sample_terms[0], '@@object?skip_calculated=true')
        term_name = term_object.get('term_name')

        # sample term customization based on biosample type
        if self.item_type == 'primary_cell':
            if 'cell' not in term_name:
                summary_terms = f'{term_name} cell'
            else:
                summary_terms = term_name
        elif self.item_type == 'in_vitro_system':
            summary_terms = f'{term_name} {classification}'
            if classification in term_name:
                summary_terms = term_name
            elif 'cell' in classification and 'cell' in term_name:
                summary_terms = term_name.replace('cell', classification)
            elif 'tissue' in classification and 'tissue' in term_name:
                summary_terms = term_name.replace('tissue', classification)
        elif self.item_type == 'tissue':
            if 'tissue' not in term_name:
                summary_terms = f'{term_name} tissue'
            else:
                summary_terms = term_name
        elif self.item_type == 'whole_organism':
            summary_terms = concat_numeric_and_units(len(donors), term_name, no_numeric_on_one=True)

        # embryonic is prepended to the start of the summary
        if (embryonic and
                self.item_type in ['primary_cell', 'tissue']):
            summary_terms = f'embryonic {summary_terms}'

        # virtual is prepended to the start of the summary
        if (virtual and
                self.item_type in ['primary_cell', 'in_vitro_system', 'tissue']):
            summary_terms = f'virtual {summary_terms}'

        # cellular sub pool is appended to the end of the summary in parentheses
        if (cellular_sub_pool and
                self.item_type in ['primary_cell']):
            summary_terms += f' ({cellular_sub_pool})'

        # time post change and targeted term are appended to the end of the summary
        if (time_post_change and
                self.item_type in ['in_vitro_system']):
            time_post_change = concat_numeric_and_units(time_post_change, time_post_change_units)
            if targeted_sample_term:
                targeted_term_object = request.embed(targeted_sample_term, '@@object?skip_calculated=true')
                targeted_term_name = targeted_term_object.get('term_name')
                summary_terms += f' induced to {targeted_term_name} for {time_post_change}'
            else:
                summary_terms += f' induced for {time_post_change}'

        # a comma is added before sex or taxa if sex is unspecified
        summary_terms += ','

        # sex is appended to the end of the summary
        if (sex and
                self.item_type in ['primary_cell', 'in_vitro_system', 'tissue', 'whole_organism']):
            if sex != 'unspecified':
                if sex == 'mixed':
                    sex = 'mixed sex'
                elif len(donors) > 1:
                    sex = f'{sex}s'
                summary_terms += f' {sex}'

        # taxa of the donor(s) is appended to the end of the summary
        if (donors and
                self.item_type in ['primary_cell', 'in_vitro_system', 'tissue', 'whole_organism']):
            if not taxa or taxa == 'Mus musculus':
                taxa_set = set()
                strains_set = set()
                for donor in donors:
                    donor_object = request.embed(donor, '@@object?skip_calculated=true')
                    taxa_set.add(donor_object['taxa'])
                    if donor_object['taxa'] == 'Mus musculus':
                        strains_set.add(donor_object.get('strain', ''))
                strains = ', '.join(sorted(strains_set))
                taxa_list = sorted(list(taxa_set))
                if 'Mus musculus' in taxa_list:
                    mouse_index = taxa_list.index('Mus musculus')
                    taxa_list[mouse_index] += f' {strains}'
                taxa = ' and '.join(taxa_list)
            summary_terms += f' {taxa}'

        # age is appended to the end of the summary
        if (age != 'unknown' and
                self.item_type in ['primary_cell', 'tissue', 'whole_organism']):
            age = concat_numeric_and_units(age, age_units)
            summary_terms += f' ({age})'

        # sorted fraction detail is appended to the end of the summary
        if (sorted_fraction_detail and
                self.item_type in ['in_vitro_system']):
            summary_terms += f' (sorting details: {sorted_fraction_detail})'

        # biomarker summaries are appended to the end of the summary
        if (biomarkers and
                self.item_type in ['primary_cell', 'in_vitro_system']):
            biomarker_summaries = []
            for biomarker in biomarkers:
                biomarker_object = request.embed(biomarker)
                if biomarker_object['quantification'] in ['positive', 'negative']:
                    biomarker_summary = f'{biomarker_object["quantification"]} detection of {biomarker_object["name"]}'
                elif biomarker_object['quantification'] in ['high', 'intermediate', 'low']:
                    if biomarker_object.get('classification') == 'marker gene':
                        biomarker_summary = f'{biomarker_object["quantification"]} expression of {biomarker_object["name"]}'
                    else:
                        biomarker_summary = f'{biomarker_object["quantification"]} level of {biomarker_object["name"]}'
                biomarker_summaries.append(biomarker_summary)
                biomarker_summaries = sorted(biomarker_summaries)
            summary_terms += f' characterized by {", ".join(biomarker_summaries)}'

        # treatment summaries are appended to the end of the summary
        if (treatments and
                self.item_type in ['primary_cell', 'in_vitro_system', 'tissue']):
            treatment_objects = [request.embed(treatment) for treatment in treatments]
            depleted_treatment_summaries = sorted([treatment.get('summary')[13:]
                                                  for treatment in treatment_objects if treatment.get('depletion')])
            perturbation_treatment_summaries = sorted([treatment.get('summary')[13:]
                                                      for treatment in treatment_objects if not treatment.get('depletion')])
            if depleted_treatment_summaries:
                summary_terms += f' depleted of {", ".join(depleted_treatment_summaries)}'
            if perturbation_treatment_summaries:
                summary_terms += f' treated with {", ".join(perturbation_treatment_summaries)}'

        return summary_terms


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
    embedded_with_frame = Biosample.embedded_with_frame


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
    embedded_with_frame = Biosample.embedded_with_frame + [
        Path('cell_fate_change_treatments', include=['@id', 'purpose', 'treatment_type', 'summary', 'status']),
        Path('originated_from', include=['@id', 'accession']),
    ]


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
    embedded_with_frame = Biosample.embedded_with_frame


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
    embedded_with_frame = Sample.embedded_with_frame + [
        Path('sample_terms', include=['@id', 'term_name']),
    ]

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, request, sample_terms, sample_material):
        if len(sample_terms) > 1:
            term_name = 'mixed'
        else:
            term_object = request.embed(sample_terms[0], '@@object?skip_calculated=true')
            term_name = (term_object.get('term_name'))
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
    embedded_with_frame = Biosample.embedded_with_frame


@collection(
    name='multiplexed-samples',
    unique_key='accession',
    properties={
        'title': 'Multiplexed Samples',
        'description': 'Listing of multiplexed samples',
    }
)
class MultiplexedSample(Sample):
    item_type = 'multiplexed_sample'
    schema = load_schema('igvfd:schemas/multiplexed_sample.json')
    embedded_with_frame = Sample.embedded_with_frame + [
        Path('sample_terms', include=['@id', 'term_name']),
        Path('disease_terms', include=['@id', 'term_name']),
        Path('multiplexed_samples', include=['@id', 'accession', '@type',
             'summary', 'sample_terms', 'disease_terms', 'donors', 'status']),
        Path('multiplexed_samples.sample_terms', include=['term_name']),
        Path('multiplexed_samples.disease_terms', include=['term_name']),
        Path('multiplexed_samples.donors', include=['@id', 'accession']),
        Path('treatments', include=['@id', 'purpose', 'treatment_type', 'summary', 'status']),
        Path('modifications', include=['@id', 'modality', 'summary', 'status'])
    ]

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, request, multiplexed_samples=None):
        if multiplexed_samples:
            multiplexed_sample_summaries = [request.embed(
                multiplexed_sample, '@@object').get('summary') for multiplexed_sample in multiplexed_samples[:2]]
            if len(multiplexed_samples) > 2:
                remainder = f'... and {len(multiplexed_samples) - 2} more sample{"s" if len(multiplexed_samples) - 2 != 1 else ""}'
                multiplexed_sample_summaries = multiplexed_sample_summaries + [remainder]
            return f'multiplexed sample of {", ".join(multiplexed_sample_summaries)}'
        else:
            return 'multiplexed sample'

    @calculated_property(
        schema={
            'title': 'Sample terms',
            'type': 'array',
            'notSubmittable': True,
            'items': {
                'type': 'string',
                'linkTo': 'SampleTerm',
            }
        }
    )
    def sample_terms(self, request, multiplexed_samples):
        return collect_multiplexed_samples_prop(request, multiplexed_samples, 'sample_terms')

    @calculated_property(
        schema={
            'title': 'Disease terms',
            'type': 'array',
            'notSubmittable': True,
            'items': {
                'type': 'string',
                'linkTo': 'PhenotypeTerm'
            }
        }
    )
    def disease_terms(self, request, multiplexed_samples):
        return collect_multiplexed_samples_prop(request, multiplexed_samples, 'disease_terms')

    @calculated_property(
        schema={
            'title': 'Treatments',
            'type': 'array',
            'notSubmittable': True,
            'items': {
                'type': 'string',
                'linkTo': 'Treatment'
            }
        }
    )
    def treatments(self, request, multiplexed_samples):
        return collect_multiplexed_samples_prop(request, multiplexed_samples, 'treatments')

    @calculated_property(
        schema={
            'title': 'Modifications',
            'type': 'array',
            'notSubmittable': True,
            'items': {
                'type': 'string',
                'linkTo': 'Modification'
            }
        }
    )
    def modifications(self, request, multiplexed_samples):
        return collect_multiplexed_samples_prop(request, multiplexed_samples, 'modifications')

    @calculated_property(
        schema={
            'title': 'Donors',
            'type': 'array',
            'notSubmittable': True,
            'items': {
                'type': 'string',
                'linkTo': 'Donor'
            }
        }
    )
    def donors(self, request, multiplexed_samples):
        return collect_multiplexed_samples_prop(request, multiplexed_samples, 'donors')

    @calculated_property(
        schema={
            'title': 'Biomarkers',
            'type': 'array',
            'notSubmittable': True,
            'items': {
                'type': 'string',
                'linkTo': 'Biomarker'
            }
        }
    )
    def biomarkers(self, request, multiplexed_samples):
        return collect_multiplexed_samples_prop(request, multiplexed_samples, 'biomarkers')

    @calculated_property(
        schema={
            'title': 'Sources',
            'type': 'array',
            'notSubmittable': True,
            'items': {
                'type': 'string',
                'linkTo': [
                    'Source',
                    'Lab'
                ]
            }
        }
    )
    def sources(self, request, multiplexed_samples):
        return collect_multiplexed_samples_prop(request, multiplexed_samples, 'sources')
