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
        Path('sorted_from', include=['@id', 'accession']),
        Path('file_sets', include=['@id', 'accession', 'aliases', 'lab', 'status']),
        Path('file_sets.lab', include=['title']),
        Path('multiplexed_in', include=['@id', 'accession'])
    ]

    @calculated_property(schema={
        'title': 'File Sets',
        'type': 'array',
        'items': {
            'title': 'File Set',
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
            'title': 'Multiplexed In',
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
    def summary(self, request, sample_terms, donors, sex, age, age_units=None, embryonic=None, virtual=None, classification=None, time_post_change=None, time_post_change_units=None, targeted_sample_term=None, cellular_sub_pool=None, taxa=None, sorted_from_detail=None, disease_terms=None, biomarkers=None, treatments=None):
        term_object = request.embed(sample_terms[0], '@@object?skip_calculated=true')
        term_name = term_object.get('term_name')
        biosample_type = self.item_type

        # sample term customization based on biosample type
        if biosample_type == 'primary_cell':
            if 'cell' not in term_name:
                summary_terms = f'{term_name} cell'
            else:
                summary_terms = term_name
        elif biosample_type == 'in_vitro_system':
            summary_terms = f'{term_name} {classification}'
            if classification in term_name:
                summary_terms = term_name
            elif 'cell' in classification and 'cell' in term_name:
                summary_terms = term_name.replace('cell', classification)
            elif 'tissue' in classification and 'tissue' in term_name:
                summary_terms = term_name.replace('tissue', classification)
        elif biosample_type == 'tissue':
            if 'tissue' not in term_name:
                summary_terms = f'{term_name} tissue'
            else:
                summary_terms = term_name
        elif biosample_type == 'whole_organism':
            summary_terms = concat_numeric_and_units(len(donors), term_name, no_numeric_on_one=True)
        elif len(sample_terms) > 1:
            summary_terms = 'mixed'

        # embryonic is prepended to the start of the summary
        if (embryonic and
                biosample_type in ['primary_cell', 'tissue']):
            summary_terms = f'embryonic {summary_terms}'

        # virtual is prepended to the start of the summary
        if (virtual and
                biosample_type in ['primary_cell', 'in_vitro_system', 'tissue']):
            summary_terms = f'virtual {summary_terms}'

        # time post change and targeted term are appended to the end of the summary
        if (time_post_change and
                biosample_type in ['in_vitro_system']):
            time_post_change = concat_numeric_and_units(time_post_change, time_post_change_units)
            if targeted_sample_term:
                targeted_term_object = request.embed(targeted_sample_term, '@@object?skip_calculated=true')
                targeted_term_name = targeted_term_object.get('term_name')
                summary_terms += f' induced to {targeted_term_name} for {time_post_change}'
            else:
                summary_terms += f' induced for {time_post_change}'

        # cellular sub pool is appended to the end of the summary in parentheses
        if (cellular_sub_pool and
                biosample_type in ['primary_cell', 'in_vitro_system']):
            summary_terms += f' ({cellular_sub_pool})'

        # a comma is added before sex or taxa if sex is unspecified
        summary_terms += ','

        # sex is appended to the end of the summary
        if (sex and
                biosample_type in ['primary_cell', 'in_vitro_system', 'tissue', 'whole_organism']):
            if sex != 'unspecified':
                if sex == 'mixed':
                    sex = 'mixed sex'
                summary_terms += f' {sex},'

        # taxa of the donor(s) is appended to the end of the summary
        if (donors and
                biosample_type in ['primary_cell', 'in_vitro_system', 'tissue', 'whole_organism']):
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
                biosample_type in ['primary_cell', 'tissue', 'whole_organism']):
            age = concat_numeric_and_units(age, age_units)
            summary_terms += f' ({age})'

        # sorted from detail is appended to the end of the summary
        if (sorted_from_detail and
                biosample_type in ['primary_cell', 'in_vitro_system']):
            summary_terms += f' (sorting details: {sorted_from_detail})'

        # biomarker summaries are appended to the end of the summary
        if (biomarkers and
                biosample_type in ['primary_cell', 'in_vitro_system']):
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
            summary_terms += f' characterized by {", ".join(biomarker_summaries)},'

        # disease terms are appended to the end of the summary
        if (disease_terms and
                biosample_type in ['primary_cell', 'in_vitro_system', 'tissue', 'whole_organism']):
            phenotype_term_names = sorted([request.embed(disease_term).get('term_name')
                                          for disease_term in disease_terms])
            summary_terms += f' associated with {", ".join(phenotype_term_names)},'

        # treatment summaries are appended to the end of the summary
        if (treatments and
                biosample_type in ['primary_cell', 'in_vitro_system', 'tissue', 'whole_organism']):
            treatment_objects = [request.embed(treatment) for treatment in treatments]
            depleted_treatment_summaries = sorted([treatment.get('summary')[13:]
                                                  for treatment in treatment_objects if treatment.get('depletion')])
            perturbation_treatment_summaries = sorted([treatment.get('summary')[13:]
                                                      for treatment in treatment_objects if not treatment.get('depletion')])
            if depleted_treatment_summaries:
                summary_terms += f' depleted of {", ".join(depleted_treatment_summaries)},'
            if perturbation_treatment_summaries:
                summary_terms += f' treated with {", ".join(perturbation_treatment_summaries)}'

        return summary_terms.strip(',')


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

    @calculated_property(
        schema={
            'title': 'Classification',
            'description': 'The general category of this type of sample.',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def classification(self):
        return self.item_type.replace('_', ' ')


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

    @calculated_property(
        schema={
            'title': 'Classification',
            'description': 'The general category of this type of sample.',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def classification(self):
        return self.item_type.replace('_', ' ')


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
    def summary(self, request, sample_terms, sample_material, virtual=None):
        if len(sample_terms) > 1:
            summary_terms = 'mixed'
        else:
            term_object = request.embed(sample_terms[0], '@@object?skip_calculated=true')
            summary_terms = term_object.get('term_name')

        summary_terms = f'{sample_material} {summary_terms}'

        if virtual:
            summary_terms = f'virtual {summary_terms}'

        return summary_terms

    @calculated_property(
        schema={
            'title': 'Classification',
            'description': 'The general category of this type of sample.',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def classification(self):
        return self.item_type.replace('_', ' ')


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

    @calculated_property(
        schema={
            'title': 'Classification',
            'description': 'The general category of this type of sample.',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def classification(self):
        return self.item_type.replace('_', ' ')


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
             'summary', 'sample_terms', 'construct_library_sets', 'disease_terms', 'donors', 'status']),
        Path('multiplexed_samples.sample_terms', include=['term_name']),
        Path('multiplexed_samples.disease_terms', include=['term_name']),
        Path('multiplexed_samples.donors', include=['@id', 'accession']),
        Path('treatments', include=['@id', 'purpose', 'treatment_type', 'summary', 'status']),
        Path('modifications', include=['@id', 'modality', 'summary', 'status']),
        Path('construct_library_sets', include=['@id', 'accession'])
    ]

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, request, multiplexed_samples=None):
        while any(sample.startswith('/multiplexed-samples/') for sample in multiplexed_samples):
            for multiplexed_sample in multiplexed_samples:
                if multiplexed_sample.startswith('/multiplexed-samples/'):
                    decomposed_samples = request.embed(multiplexed_sample, '@@object').get('multiplexed_samples')
                    multiplexed_samples.remove(multiplexed_sample)
                    if decomposed_samples:
                        for decomposed_sample in decomposed_samples:
                            # duplicated samples are not added to the summary
                            if decomposed_sample not in multiplexed_samples:
                                multiplexed_samples += [decomposed_sample]
        if multiplexed_samples:
            sample_summaries = sorted([request.embed(
                sample, '@@object').get('summary') for sample in sorted(multiplexed_samples)[:2]])
            if len(multiplexed_samples) > 2:
                remainder = f'... and {len(multiplexed_samples) - 2} more sample{"s" if len(multiplexed_samples) - 2 != 1 else ""}'
                sample_summaries += [remainder]
            return f'multiplexed sample of {", ".join(sample_summaries)}'
        else:
            return 'multiplexed sample'

    @calculated_property(
        schema={
            'title': 'Sample Terms',
            'type': 'array',
            'notSubmittable': True,
            'items': {
                'title': 'Sample Term',
                'type': 'string',
                'linkTo': 'SampleTerm',
            }
        }
    )
    def sample_terms(self, request, multiplexed_samples):
        return collect_multiplexed_samples_prop(request, multiplexed_samples, 'sample_terms')

    @calculated_property(
        schema={
            'title': 'Disease Terms',
            'type': 'array',
            'notSubmittable': True,
            'items': {
                'title': 'Disease Term',
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
                'title': 'Treatment',
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
                'title': 'Modification',
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
                'title': 'Donor',
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
                'title': 'Biomarker',
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
                'title': 'Source',
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

    @calculated_property(
        schema={
            'title': 'Construct Library Sets',
            'type': 'array',
            'notSubmittable': True,
            'items': {
                'title': 'Construct Library Set',
                'type': 'string',
                'linkTo': 'ConstructLibrarySet'
            }
        }
    )
    def construct_library_sets(self, request, multiplexed_samples):
        return collect_multiplexed_samples_prop(request, multiplexed_samples, 'construct_library_sets')

    @calculated_property(
        schema={
            'title': 'Classification',
            'description': 'The general category of this type of sample.',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def classification(self):
        return self.item_type.replace('_', ' ')
