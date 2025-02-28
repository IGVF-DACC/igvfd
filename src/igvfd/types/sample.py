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


def collect_multiplexed_samples_prop(request, multiplexed_samples, property_name, skip_calculated=True):
    property_set = set()
    for sample in multiplexed_samples:
        # If to get a specific calculated property
        if skip_calculated is False:
            sample_props = request.embed(sample, f'@@object_with_select_calculated_properties?field={property_name}')
        # If to get non-calculated properties
        else:
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


def decompose_multiplexed_samples(request, samples, visited_multiplexed_samples=None):
    if visited_multiplexed_samples is None:
        visited_multiplexed_samples = set()
    decomposed_samples = set()
    for sample in samples:
        if sample.startswith('/multiplexed-samples/') and sample not in visited_multiplexed_samples:
            visited_multiplexed_samples.add(sample)
            multiplexed_samples = request.embed(sample, '@@object').get('multiplexed_samples')
            if multiplexed_samples:
                decomposed_samples.update(decompose_multiplexed_samples(
                    request, multiplexed_samples, visited_multiplexed_samples))
        else:
            decomposed_samples.add(sample)
    return list(decomposed_samples)


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
        'multiplexed_in': ('MultiplexedSample', 'multiplexed_samples'),
        'sorted_fractions': ('Sample', 'sorted_from'),
        'origin_of': ('Sample', 'originated_from'),
        'institutional_certificates': ('InstitutionalCertificate', 'samples'),
    }
    embedded_with_frame = [
        Path('award', include=['@id', 'component']),
        Path('lab', include=['@id', 'title']),
        Path('sources', include=['@id', 'title', 'status']),
        Path('submitted_by', include=['@id', 'title']),
        Path('sorted_from', include=['@id', 'accession', 'status']),
        Path('file_sets', include=['@id', 'accession', 'summary', 'aliases',
             'lab', 'status', 'preferred_assay_title', 'file_set_type']),
        Path('file_sets.lab', include=['title']),
        Path('multiplexed_in', include=['@id', 'accession', 'status']),
        Path('publications', include=['@id', 'publication_identifiers', 'status']),
        Path('sample_terms', include=['@id', 'term_name', 'status']),
        Path('disease_terms', include=['@id', 'term_name', 'status']),
        Path('treatments', include=['@id', 'purpose', 'treatment_type',
             'status', 'treatment_term_name', 'depletion']),
        Path('biomarkers.gene', include=['@id', 'name_quantification', 'classification', 'gene', 'symbol', 'status']),
        Path('modifications.tagged_proteins', include=[
             '@id', 'summary', 'status', 'tagged_proteins', 'modality', 'fused_domain', 'symbol', 'cas', 'cas_species', 'degron_system']),
        Path('institutional_certificates', include=['@id', 'certificate_identifier', 'status']),
        Path('construct_library_sets.associated_phenotypes', include=[
             '@id', 'accession', 'file_set_type', 'term_name', 'associated_phenotypes', 'status']),
        Path('donors', include=['@id', 'accession', 'status', 'strain', 'ethnicities']),
    ]

    audit_inherit = [
        'award',
        'lab',
        'sources',
        'sample_terms',
        'construct_library_sets',
    ]

    set_status_up = [
        'construct_library_sets',
        'documents',
        'sorted_from'
    ]
    set_status_down = []

    @calculated_property(schema={
        'title': 'File Sets',
        'type': 'array',
        'description': 'The file sets linked to this sample.',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'File Set',
            'type': ['string', 'object'],
            'linkFrom': 'FileSet.samples',
        },
        'notSubmittable': True,
    })
    def file_sets(self, request, file_sets, multiplexed_in=[]):
        # This is required to get the analysis set reverse links since analysis set calculates samples
        for file_set in file_sets:
            file_set_object = request.embed(
                file_set, '@@object_with_select_calculated_properties?field=input_for')
            for input_for in file_set_object.get('input_for', []):
                if input_for.startswith('/analysis-sets/') and input_for not in file_sets:
                    file_sets.append(input_for)
        # file sets associated with a multiplexed sample that a sample was multiplexed in are included
        for multiplexed_sample in multiplexed_in:
            multiplexed_sample_object = request.embed(
                multiplexed_sample, '@@object_with_select_calculated_properties?field=file_sets')
            multiplexed_file_sets = multiplexed_sample_object.get('file_sets')
            for file_set in multiplexed_file_sets:
                if file_set not in file_sets:
                    file_sets.append(file_set)
        return paths_filtered_by_status(request, file_sets)

    @calculated_property(schema={
        'title': 'Multiplexed In',
        'type': 'array',
        'description': 'The multiplexed samples in which this sample is included.',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Multiplexed In',
            'type': ['string', 'object'],
            'linkFrom': 'MultiplexedSample.multiplexed_samples',
        },
        'notSubmittable': True,
    })
    def multiplexed_in(self, request, multiplexed_in):
        return paths_filtered_by_status(request, multiplexed_in)

    @calculated_property(schema={
        'title': 'Sorted Fraction Samples',
        'type': 'array',
        'description': 'The fractions into which this sample has been sorted.',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Sorted Fraction Sample',
            'type': ['string', 'object'],
            'linkFrom': 'Sample.sorted_from',
        },
        'notSubmittable': True,
    })
    def sorted_fractions(self, request, sorted_fractions):
        return paths_filtered_by_status(request, sorted_fractions)

    @calculated_property(schema={
        'title': 'Origin Sample Of',
        'type': 'array',
        'description': 'The samples which originate from this sample, such as through a process of cell differentiation.',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Originated Sample',
            'type': ['string', 'object'],
            'linkFrom': 'InVitroSystem.originated_from',
        },
        'notSubmittable': True,
    })
    def origin_of(self, request, origin_of):
        return paths_filtered_by_status(request, origin_of)

    @calculated_property(schema={
        'title': 'Institutional Certificates',
        'type': 'array',
        'description': 'The institutional certificates under which use of this sample is approved.',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Institutional Certificate',
            'type': ['string', 'object'],
            'linkFrom': 'InstitutionalCertificate.samples',
        },
        'notSubmittable': True,
    })
    def institutional_certificates(self, request, institutional_certificates):
        return paths_filtered_by_status(request, institutional_certificates)


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
    rev = Sample.rev | {'parts': ('Biosample', 'part_of'),
                        'pooled_in': ('Biosample', 'pooled_from')}
    embedded_with_frame = Sample.embedded_with_frame

    audit_inherit = Sample.audit_inherit + [
        'disease_terms',
        'treatments',
        'modifications',
    ]

    set_status_up = Sample.set_status_up + [
        'biomarkers',
        'donors',
        'modifications',
        'originated_from',
        'part_of',
        'pooled_from',
        'sample_terms',
        'targeted_sample_term',
    ]
    set_status_down = Sample.set_status_down + []

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
            'title': 'Upper Bound Age In Hours',
            'description': 'Upper bound of age of organism in hours at the time of collection of the sample.',
            'type': 'number',
            'notSubmittable': True,
        }
    )
    def upper_bound_age_in_hours(self, upper_bound_age=None, age_units=None):
        conversion_factors = {
            'minute': 1/60,
            'hour': 1,
            'day': 24,
            'week': 168,
            'month': 720,
            'year': 8760
        }
        if upper_bound_age:
            return upper_bound_age*conversion_factors[age_units]

    @calculated_property(
        define=True,
        schema={
            'title': 'Lower Bound Age In Hours',
            'description': 'Lower bound of age of organism in hours at the time of collection of the sample .',
            'type': 'number',
            'notSubmittable': True,
        }
    )
    def lower_bound_age_in_hours(self, lower_bound_age=None, age_units=None):
        conversion_factors = {
            'minute': 1/60,
            'hour': 1,
            'day': 24,
            'week': 168,
            'month': 720,
            'year': 8760
        }
        if lower_bound_age:
            return lower_bound_age*conversion_factors[age_units]

    @calculated_property(
        define=True,
        schema={
            'title': 'Taxa',
            'type': 'string',
            'description': 'The species of the organism.',
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
            'description': 'A summary of the sample.',
            'notSubmittable': True,
        }
    )
    def summary(self, request, sample_terms, donors, sex, age, age_units=None, modifications=None, embryonic=None, virtual=None, classifications=None, time_post_change=None, time_post_change_units=None, targeted_sample_term=None, cellular_sub_pool=None, taxa=None, sorted_from_detail=None, disease_terms=None, biomarkers=None, treatments=None, construct_library_sets=None, moi=None, nucleic_acid_delivery=None, growth_medium=None, biosample_qualifiers=None):
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
            if len(classifications) == 1:
                summary_terms = f'{term_name} {classifications[0]}'
                if classifications[0] in term_name:
                    summary_terms = term_name
                elif 'cell' in classifications[0] and 'cell' in term_name:
                    summary_terms = term_name.replace('cell', classifications[0])
                elif 'tissue' in classifications[0] and 'tissue' in term_name:
                    summary_terms = term_name.replace('tissue', classifications[0])
                elif 'gastruloid' in classifications[0]:
                    summary_terms = term_name.replace('gastruloid', '')
            elif len(classifications) == 2:
                if 'differentiated cell specimen' in classifications and 'pooled cell specimen' in classifications:
                    summary_terms = f'{term_name} pooled differentiated cell specimen'
                    if 'cell' in term_name:
                        summary_terms = term_name.replace('cell', 'pooled differentiated cell specimen')
                elif 'reprogrammed cell specimen' in classifications and 'pooled cell specimen' in classifications:
                    summary_terms = f'{term_name} pooled reprogrammed cell specimen'
                    if 'cell' in term_name:
                        summary_terms = term_name.replace('cell', 'pooled reprogrammed cell specimen')
        elif biosample_type == 'tissue':
            if 'tissue' not in term_name:
                summary_terms = f'{term_name} tissue'
            else:
                summary_terms = term_name
        elif biosample_type == 'whole_organism':
            summary_terms = concat_numeric_and_units(len(donors), term_name, no_numeric_on_one=True)
        elif len(sample_terms) > 1:
            summary_terms = 'mixed'

        # Prepend biosample qualifiers if they exist
        if biosample_qualifiers:
            qualifiers_string = ', '.join(biosample_qualifiers)
            summary_terms = f'{qualifiers_string} {summary_terms}'

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
                biosample_type in ['primary_cell', 'in_vitro_system', 'tissue']):
            summary_terms += f' (cellular sub pool: {cellular_sub_pool})'

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
                summary_terms += f' treated with {", ".join(perturbation_treatment_summaries)},'

        # modification summaries are appended to the end of the summary
        if (modifications and
                biosample_type in ['primary_cell', 'in_vitro_system', 'tissue', 'whole_organism']):
            modification_objects = [request.embed(modification) for modification in modifications]
            modification_summaries = sorted([modification.get('summary') for modification in modification_objects])
            if modification_summaries:
                summary_terms += f' modified with {", ".join(modification_summaries)},'

        # construct library set overview is appended to the end of the summary
        if (construct_library_sets and
                biosample_type in ['primary_cell', 'in_vitro_system', 'tissue', 'whole_organism']):
            verb = 'transfected with'
            library_types = set()
            for construct_library_set in construct_library_sets:
                construct_library_set_object = request.embed(construct_library_set, '@@object?skip_calculated=true')
                library_types.add(construct_library_set_object['file_set_type'])
            if nucleic_acid_delivery:
                if nucleic_acid_delivery == 'lentiviral transduction':
                    verb = 'transduced (lentivirus) with'
                elif nucleic_acid_delivery == 'adenoviral transduction':
                    verb = 'transduced (adenovirus) with'
            if len(library_types) == 1:
                library_types = ', '.join(library_types)
                if moi:
                    summary_terms += f' {verb} a {library_types} (MOI of {moi}),'
                else:
                    summary_terms += f' {verb} a {library_types},'
            else:
                if moi:
                    summary_terms += f' {verb} multiple libraries (MOI of {moi}),'
                else:
                    summary_terms += f' {verb} multiple libraries,'

        # growth media is appended to the end of the summary
        if (growth_medium and biosample_type in ['in_vitro_system']):
            summary_terms += f' grown in {growth_medium}'

        return summary_terms.strip(',')

    @calculated_property(schema={
        'title': 'Biosample Parts',
        'type': 'array',
        'description': 'The parts into which this sample has been divided.',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Biosample Part',
            'type': ['string', 'object'],
            'linkFrom': 'Biosample.part_of',
        },
        'notSubmittable': True,
    })
    def parts(self, request, parts):
        return paths_filtered_by_status(request, parts)

    @calculated_property(schema={
        'title': 'Pooled In',
        'type': 'array',
        'description': 'The pooled samples in which this sample is included.',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Biosample Pooled In',
            'type': ['string', 'object'],
            'linkFrom': 'Biosample.pooled_from',
        },
        'notSubmittable': True,
    })
    def pooled_in(self, request, pooled_in):
        return paths_filtered_by_status(request, pooled_in)


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
    audit_inherit = Biosample.audit_inherit
    set_status_up = Biosample.set_status_up + []
    set_status_down = Biosample.set_status_down + []

    @calculated_property(
        schema={
            'title': 'Classifications',
            'description': 'The general category of this type of sample.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Classification',
                'type': 'string'
            },
            'notSubmittable': True,
        }
    )
    def classifications(self):
        return [self.item_type.replace('_', ' ')]


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
    rev = Biosample.rev | {'demultiplexed_to': ('InVitroSystem', 'demultiplexed_from')}
    embedded_with_frame = Biosample.embedded_with_frame + [
        Path('cell_fate_change_treatments', include=['@id', 'purpose', 'treatment_type', 'summary', 'status']),
        Path('targeted_sample_term', include=['@id', 'term_name', 'status']),
        Path('originated_from', include=['@id', 'accession', 'status']),
    ]
    audit_inherit = Biosample.audit_inherit
    set_status_up = Biosample.set_status_up + [
        'cell_fate_change_protocol'
    ]
    set_status_down = Biosample.set_status_down + []

    @calculated_property(schema={
        'title': 'Demultiplexed To',
        'type': 'array',
        'description': 'The parts into which this sample has been demultiplexed.',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Demultiplexed To',
            'type': ['string', 'object'],
            'linkFrom': 'InVitroSystem.demultiplexed_from',
        },
        'notSubmittable': True,
    })
    def demultiplexed_to(self, request, demultiplexed_to):
        return paths_filtered_by_status(request, demultiplexed_to)


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
    audit_inherit = Biosample.audit_inherit
    set_status_up = Biosample.set_status_up + []
    set_status_down = Biosample.set_status_down + []

    @calculated_property(
        schema={
            'title': 'Classifications',
            'description': 'The general category of this type of sample.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Classification',
                'type': 'string'
            },
            'notSubmittable': True,
        }
    )
    def classifications(self):
        return [self.item_type.replace('_', ' ')]


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
        Path('award', include=['@id', 'component']),
        Path('lab', include=['@id', 'title']),
        Path('sources', include=['@id', 'title', 'status']),
        Path('submitted_by', include=['@id', 'title']),
        Path('sorted_from', include=['@id', 'accession', 'status']),
        Path('file_sets', include=['@id', 'accession', 'summary', 'aliases',
             'lab', 'status', 'preferred_assay_title', 'file_set_type']),
        Path('file_sets.lab', include=['title']),
        Path('publications', include=['@id', 'publication_identifiers', 'status']),
        Path('sample_terms', include=['@id', 'term_name', 'status']),
        Path('construct_library_sets.associated_phenotypes', include=[
             '@id', 'accession', 'file_set_type', 'term_name', 'status'])
    ]
    audit_inherit = Sample.audit_inherit
    set_status_up = Biosample.set_status_up + []
    set_status_down = Biosample.set_status_down + []

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'description': 'A summary of this sample.',
            'notSubmittable': True,
        }
    )
    def summary(self, request, sample_terms, sample_material, virtual=None, construct_library_sets=None, moi=None, nucleic_acid_delivery=None):
        if len(sample_terms) > 1:
            summary_terms = 'mixed'
        else:
            term_object = request.embed(sample_terms[0], '@@object?skip_calculated=true')
            summary_terms = term_object.get('term_name')

        summary_terms = f'{sample_material} {summary_terms}'

        if virtual:
            summary_terms = f'virtual {summary_terms}'

        if construct_library_sets:
            verb = 'transfected with'
            library_types = set()
            for construct_library_set in construct_library_sets:
                construct_library_set_object = request.embed(construct_library_set, '@@object?skip_calculated=true')
                library_types.add(construct_library_set_object['file_set_type'])
            if nucleic_acid_delivery:
                if nucleic_acid_delivery == 'lentiviral transduction':
                    verb = 'transduced (lentivirus) with'
                elif nucleic_acid_delivery == 'adenoviral transduction':
                    verb = 'transduced (adenovirus) with'
            if len(library_types) == 1:
                library_types = ', '.join(library_types)
                summary_terms = f'{summary_terms} {verb} a {library_types}'
            else:
                summary_terms = f'{summary_terms} {verb} multiple libraries'
        if moi:
            summary_terms = f'{summary_terms} (MOI of {moi})'
        return summary_terms

    @calculated_property(
        schema={
            'title': 'Classifications',
            'description': 'The general category of this type of sample.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Classification',
                'type': 'string'
            },
            'notSubmittable': True,
        }
    )
    def classifications(self):
        return [self.item_type.replace('_', ' ')]


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
    audit_inherit = Biosample.audit_inherit
    set_status_up = Biosample.set_status_up + []
    set_status_down = Biosample.set_status_down + []

    @calculated_property(
        schema={
            'title': 'Classifications',
            'description': 'The general category of this type of sample.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Classification',
                'type': 'string'
            },
            'notSubmittable': True,
        }
    )
    def classifications(self):
        return [self.item_type.replace('_', ' ')]


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
        Path('multiplexed_samples', include=['@id', 'accession', '@type',
             'summary', 'sample_terms', 'construct_library_sets', 'disease_terms', 'donors', 'status']),
        Path('multiplexed_samples.sample_terms', include=['@id', 'term_name', 'status']),
        Path('multiplexed_samples.disease_terms', include=['@id', 'term_name', 'status']),
        Path('multiplexed_samples.donors', include=['@id', 'accession', 'status']),
    ]
    audit_inherit = Biosample.audit_inherit
    set_status_up = Biosample.set_status_up + [
        'multiplexed_samples'
    ]
    set_status_down = Biosample.set_status_down + [
        'multiplexed_samples'
    ]

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'description': 'A summary of this sample.',
            'notSubmittable': True,
        }
    )
    def summary(self, request, multiplexed_samples=None):
        if multiplexed_samples:
            if any(sample.startswith('/multiplexed-samples/') for sample in multiplexed_samples):
                multiplexed_samples = decompose_multiplexed_samples(request, multiplexed_samples)
            multiplexed_samples = sorted(multiplexed_samples)
            sample_summaries = [request.embed(
                sample, '@@object').get('summary') for sample in multiplexed_samples[:2]]
            if len(multiplexed_samples) > 2:
                remainder = f'... and {len(multiplexed_samples) - 2} more sample{"s" if len(multiplexed_samples) - 2 != 1 else ""}'
                sample_summaries += [remainder]
            return f'multiplexed sample: {"; ".join(sample_summaries)}'
        else:
            return 'multiplexed sample'

    @calculated_property(
        schema={
            'title': 'Sample Terms',
            'type': 'array',
            'description': 'The sample terms of the samples included in this multiplexed sample.',
            'minItems': 1,
            'uniqueItems': True,
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
        define=True,
        schema={
            'title': 'Taxa',
            'type': 'string',
            'description': 'The species of the organism.',
            'enum': [
                    'Homo sapiens',
                    'Mus musculus',
                    'Mixed species',
                    'Saccharomyces cerevisiae'
            ],
            'notSubmittable': True
        }
    )
    def taxa(self, request, multiplexed_samples):
        taxas = set()
        if multiplexed_samples:
            for sample in multiplexed_samples:
                sample_object = request.embed(sample, '@@object_with_select_calculated_properties?field=taxa')
                taxas.add(sample_object.get('taxa'))

        if len(taxas) == 1:
            return list(taxas).pop()
        elif len(taxas) > 1:
            return 'Mixed species'
        else:
            return None

    @calculated_property(
        schema={
            'title': 'Disease Terms',
            'type': 'array',
            'description': 'The disease terms of the samples included in this multiplexed sample.',
            'minItems': 1,
            'uniqueItems': True,
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
            'description': 'The treatments of the samples included in this multiplexed sample.',
            'minItems': 1,
            'uniqueItems': True,
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
            'description': 'The modifications of the samples included in this multiplexed sample.',
            'minItems': 1,
            'uniqueItems': True,
            'notSubmittable': True,
            'items': {
                'title': 'Modification',
                'type': 'string',
                'linkTo': ['CrisprModification', 'DegronModification']
            }
        }
    )
    def modifications(self, request, multiplexed_samples):
        return collect_multiplexed_samples_prop(request, multiplexed_samples, 'modifications')

    @calculated_property(
        schema={
            'title': 'Donors',
            'type': 'array',
            'description': 'The donors of the samples included in this multiplexed sample.',
            'minItems': 1,
            'uniqueItems': True,
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
            'description': 'The biomarkers of the samples included in this multiplexed sample.',
            'minItems': 1,
            'uniqueItems': True,
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
            'description': 'The sources of the samples included in this multiplexed sample.',
            'minItems': 1,
            'uniqueItems': True,
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
            'description': 'The construct library sets of the samples included in this multiplexed sample.',
            'minItems': 1,
            'uniqueItems': True,
            'notSubmittable': True,
            'items': {
                'title': 'Construct Library Set',
                'type': 'string',
                'linkTo': 'ConstructLibrarySet'
            }
        }
    )
    def construct_library_sets(self, request, multiplexed_samples):
        if 'construct_library_sets' in request:
            return collect_multiplexed_samples_prop(request, multiplexed_samples, 'construct_library_sets')

    @calculated_property(
        schema={
            'title': 'Institutional Certificates',
            'type': 'array',
            'description': 'The institutional certificates of the samples included in this multiplexed sample.',
            'minItems': 1,
            'uniqueItems': True,
            'notSubmittable': True,
            'items': {
                'title': 'Institutional Certificate',
                'type': 'string',
                'linkTo': 'InstitutionalCertificate'
            }
        }
    )
    def institutional_certificates(self, request, multiplexed_samples):
        return collect_multiplexed_samples_prop(request, multiplexed_samples, 'institutional_certificates')

    @calculated_property(
        schema={
            'title': 'Classifications',
            'description': 'The general category of this type of sample.',
            'minItems': 1,
            'uniqueItems': True,
            'type': 'array',
            'items': {
                'title': 'Classification',
                'type': 'string'
            },
            'notSubmittable': True,
        }
    )
    def classifications(self, request, multiplexed_samples):
        # Get unique properties of individual samples' item types
        sample_classfications = collect_multiplexed_samples_prop(
            request, multiplexed_samples, 'classifications', skip_calculated=False)
        self_classification = [self.item_type.replace('_', ' ')]
        return sample_classfications + self_classification
