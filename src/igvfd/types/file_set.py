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

from datetime import datetime


def get_donors_from_samples(request, samples):
    donor_objects = []
    for sample in samples:
        donor_objects += request.embed(sample, '@@object').get('donors', [])
    return sorted(set(donor_objects)) or None


def get_file_objs_from_files(request, files):
    '''Get file objects from an array of files'''
    file_objs = []
    if files is not None:
        for file in files:
            file_objs.append(request.embed(file, '@@object?skip_calculated=true'))
    return file_objs


def get_assessed_gene_symbols(request, assessed_genes=None):
    '''Get gene symbols from an array of assessed genes.'''
    if not assessed_genes:
        return ''
    else:
        gene_symbols = []
        for assessed_gene in assessed_genes:
            gene_symbols.append(request.embed(
                assessed_gene, '@@object?skip_calculated=true').get('symbol', ''))
        return ', '.join(sorted(gene_symbols))


def get_assessed_gene_phrase(request, assessed_genes=None):
    """Get the assessed gene phrase from assessed_genes. If more than 5, return the number of assessed genes.
    """
    len_assessed_genes = len(assessed_genes) if assessed_genes else 0
    if len_assessed_genes > 5:
        assessed_gene_phrase = f'{len_assessed_genes} assessed genes'
    else:
        assessed_gene_phrase = get_assessed_gene_symbols(request, assessed_genes)
    return assessed_gene_phrase


def get_cls_phrase(cls_set, only_cls_input=False):
    cls_set = sorted(cls_set)
    cls_phrases = []
    for summary in cls_set:
        article = 'a'
        if any(summary.startswith(x) for x in ['a', 'e', 'i', 'o', 'u']):
            article = 'an'
        if only_cls_input:
            cls_phrases.append(f'{summary[0].lower()}{summary[1:]}')
        else:
            cls_phrases.append(f'{article} {summary[0].lower()}{summary[1:]}')
    if len(cls_phrases) == 1:
        cls_phrase = cls_phrases[0]
    elif len(cls_phrases) == 2:
        cls_phrase = ' and '.join(cls_phrases)
    # make special case for SGE assays: >20 CLS under each analysis set
    elif len(cls_phrases) > 2:
        if cls_phrases[0].startswith('an editing template library'):
            common_phrase = cls_phrases[0].split(' in ')[0]
            # only condense sentence if all CLS have the same selection criteria (i.e. sequence variants)
            if all(cls_phrase.startswith(common_phrase) for cls_phrase in cls_phrases):
                targeton_dict = {}
                for cls_phrase in cls_phrases:
                    # e.g. editing template library targeting sequence variants in exon6B of BARD1
                    gene = cls_phrase.split(' ')[-1]
                    targeton = cls_phrase.split(' ')[-3]
                    if gene not in targeton_dict:
                        targeton_dict[gene] = set([targeton])
                    else:
                        targeton_dict[gene].add(targeton)
                cls_count_phrases = []
                for gene, targetons in targeton_dict.items():
                    cls_count_phrases.append(f'in {len(targetons)} targetons of {gene}')
                cls_phrase = common_phrase.replace('an ', '').replace(
                    'library', 'libraries') + ' ' + ', '.join(cls_count_phrases)
            else:
                cls_phrase = ', '.join(cls_phrases[:-1]) + ', and ' + cls_phrases[-1]
        else:
            cls_phrase = ', '.join(cls_phrases[:-1]) + ', and ' + cls_phrases[-1]
    if not only_cls_input:
        # Do not add "integrating" when all input file sets are CLS.
        cls_phrase = f'integrating {cls_phrase}'
    return cls_phrase


def get_first_matching_classification(classifications, candidates):
    return next((candidate for candidate in candidates if candidate in classifications), None)


def get_file_set_props_for_summary_and_samples(request, file_set):
    '''Get properties from a file set needed for summary and samples calculation'''
    return request.embed(
        file_set,
        '@@object_with_select_calculated_properties?'
        'field=@type&field=file_set_type&field=measurement_sets'
        '&field=input_file_sets&field=targeted_genes.symbol'
        '&field=assay_term&field=samples'
        '&field=assay_titles&field=preferred_assay_titles'
    )


def _sample_summary_get_disease_terms(request, sample_object):
    '''Get disease terms from phenotypic features.'''
    disease_prefixes = ('DOID:', 'EFO:', 'HP:', 'MONDO:')
    disease_terms = []
    for phenotypic_feature in sample_object.get('phenotypic_features', []):
        feature_obj = request.embed(phenotypic_feature, '@@object?skip_calculated=true')
        # Disease only ones have no quality or quantity
        if 'quality' not in feature_obj and 'quantity' not in feature_obj:
            feature_id = feature_obj.get('feature')
            if not feature_id:
                continue
        feature_term_obj = request.embed(feature_id, '@@object?skip_calculated=true')
        # Check against term_id prefix to futher filter out non-disease ones
        term_id = feature_term_obj.get('term_id', '')
        term_name = feature_term_obj.get('term_name', '')
        if term_name and any(term_id.startswith(prefix) for prefix in disease_prefixes):
            disease_terms.append(term_name)
    return sorted(set(disease_terms))


def _sample_summary_format_disease_phrase(disease_terms):
    '''Format disease phrase based on number of disease terms.'''
    if not disease_terms:
        return ''
    if len(disease_terms) == 1:
        return disease_terms[0]
    if len(disease_terms) == 2:
        return f'{disease_terms[0]} and 1 other phenotype'
    return f'{disease_terms[0]} and {len(disease_terms) - 1} other phenotypes'


def _sample_summary_get_disease_phrase(request, sample_object):
    '''Get disease phrase for a sample object based on its phenotypic features.'''
    disease_terms = _sample_summary_get_disease_terms(request, sample_object)
    return _sample_summary_format_disease_phrase(disease_terms)


def _sample_summary_get_donor_data(request, sample_object):
    '''Get donor data from a sample object.'''
    donor_accessions = set()
    donor_strains = set()
    donor_taxa = set()
    for donor in sample_object.get('donors', []):
        donor_obj = request.embed(donor, '@@object?skip_calculated=true')
        accession = donor_obj.get('accession')
        if accession:
            donor_accessions.add(accession)
        strain = donor_obj.get('strain')
        if strain:
            donor_strains.add(strain)
        taxa = donor_obj.get('taxa')
        if taxa:
            donor_taxa.add(taxa)
    return {
        'accessions': donor_accessions,
        'strains': donor_strains,
        'taxa': donor_taxa,
    }


def _sample_summary_get_taxa(sample_object):
    '''Get taxa info and rephrase'''
    taxa_to_label = {
        'Homo sapiens': 'Human',
        'Mus musculus': 'Mouse',
        'Saccharomyces cerevisiae': 'Yeast'
    }
    taxa_value = sample_object.get('taxa', '')

    if not taxa_value:
        return ''

    if taxa_value == 'Mixed species':
        return 'Mixed species'
    return taxa_to_label.get(taxa_value, taxa_value)


def _get_sample_summary_taxa_phrase(taxa_values):
    '''Summarize a list of taxa values.'''
    if len(taxa_values) > 1:
        return 'Mixed species'
    return list(taxa_values)[0] if taxa_values else ''


def _sample_summary_join_with_and(values):
    '''Helper func for phrasing with different nums of elements.'''
    values = [value for value in sorted(set(values)) if value]
    if not values:
        return ''
    if len(values) == 1:
        return values[0]
    if len(values) == 2:
        return f'{values[0]}, {values[1]}'
    return ', '.join(values[:-1]) + f', and {values[-1]}'


def _sample_summary_get_term_name(request, term_path):
    '''Get term name from a term path.'''
    if not term_path:
        return ''
    return request.embed(term_path, '@@object?skip_calculated=true').get('term_name', '')


def _sample_summary_get_sample_term_names(request, sample_object):
    '''Get sample term names from a sample object.'''
    sample_term_names = []
    for term in sample_object.get('sample_terms', []):
        term_name = _sample_summary_get_term_name(request, term)
        if term_name:
            sample_term_names.append(term_name)
    return sorted(set(sample_term_names))


def _sample_summary_get_targeted_sample_term_name(request, sample_object):
    '''Get targeted sample term name from a sample object.'''
    if 'targeted_sample_term' in sample_object:
        targeted_sample_term = sample_object.get('targeted_sample_term')
        if not targeted_sample_term:
            return ''
        return _sample_summary_get_term_name(request, targeted_sample_term)


def _sample_summary_get_slim_for_sample_term(request, term_path):
    '''Especially for multiple tissues, summarize by system or organ slims.'''
    term_obj = request.embed(
        term_path,
        '@@object_with_select_calculated_properties?field=system_slims&field=organ_slims'
    )
    system_slims = term_obj.get('system_slims', [])
    if system_slims:
        return system_slims[0]
    organ_slims = term_obj.get('organ_slims', [])
    if organ_slims:
        return organ_slims[0]
    return ''


def _sample_summary_build_tissue_group_phrase(request, tissue_sample_objects):
    def _format_tissue_phrase(term_name):
        if term_name.endswith((' tissue', 'tissues')):
            return term_name
        return f'{term_name} tissue'

    # Get all sample terms
    all_term_names = set()
    for sample_obj in tissue_sample_objects:
        for term_path in sample_obj.get('sample_terms', []):
            term_name = _sample_summary_get_term_name(request, term_path)
            if term_name:
                all_term_names.add(term_name)

    # For single tissue, include disease if present
    if len(tissue_sample_objects) == 1:
        sample_obj = tissue_sample_objects[0]
        sample_term_phrase = _sample_summary_join_with_and(
            _sample_summary_get_sample_term_names(request, sample_obj)
        )
        disease_phrase = _sample_summary_get_disease_phrase(request, sample_obj)
        if disease_phrase:
            return f'{disease_phrase} {_format_tissue_phrase(sample_term_phrase)}'.strip()
        else:
            return _format_tissue_phrase(sample_term_phrase).strip()

    # For multiple tissues with 2 unique tissue terms, list all tissue terms without disease emphasis
    if len(all_term_names) == 2:
        parts = [_format_tissue_phrase(name) for name in sorted(all_term_names)]
        tissue_phrase = _sample_summary_join_with_and(parts)
        samples_disease_terms = [
            _sample_summary_get_disease_terms(request, sample_obj)
            for sample_obj in tissue_sample_objects
        ]
        # Elevate disease phrase when at least one tissue sample has disease terms.
        if any(samples_disease_terms):
            group_disease_terms = sorted(set(
                term
                for disease_terms in samples_disease_terms
                for term in disease_terms
            ))
            disease_phrase = _sample_summary_format_disease_phrase(group_disease_terms)
            if disease_phrase:
                return f'{disease_phrase} {tissue_phrase}'.strip()
        return tissue_phrase

    # Helper to build slim group phrase (reused below)
    def _build_tissue_slim_group_phrase():
        slim_groups = {}
        no_slim_term_names = set()
        for sample_obj in tissue_sample_objects:
            slim = ''
            for term_path in sample_obj.get('sample_terms', []):
                slim = _sample_summary_get_slim_for_sample_term(request, term_path)
                if slim:
                    break
            if slim:
                slim_groups[slim] = slim_groups.get(slim, 0) + 1
            else:
                for term_path in sample_obj.get('sample_terms', []):
                    term_name = _sample_summary_get_term_name(request, term_path)
                    if term_name:
                        no_slim_term_names.add(term_name)
        parts = []
        for slim in sorted(slim_groups):
            count = slim_groups[slim]
            if count == 1:
                parts.append(f'1 {slim} tissue')
            else:
                parts.append(f'{count} {slim} tissues')
        for term_name in sorted(no_slim_term_names):
            parts.append(_format_tissue_phrase(term_name))
        return _sample_summary_join_with_and(parts)

    # For >2 unique tissue terms where any sample has multiple disease terms,
    # aggregate all diseases and group by slim: "disease X in Y slim tissues"
    samples_disease_terms = [
        _sample_summary_get_disease_terms(request, sample_obj)
        for sample_obj in tissue_sample_objects
    ]
    if len(all_term_names) > 2 and any(len(dt) > 1 for dt in samples_disease_terms):
        group_disease_terms = sorted(set(
            term
            for dt in samples_disease_terms
            for term in dt
        ))
        disease_phrase = _sample_summary_format_disease_phrase(group_disease_terms)
        if disease_phrase:
            slim_phrase = _build_tissue_slim_group_phrase()
            if slim_phrase:
                return f'{disease_phrase} in {slim_phrase}'.strip()

    # For >2 unique tissue terms, flatten disease and tissue terms together
    tissue_phrases_with_disease = set()
    for sample_obj in tissue_sample_objects:
        sample_term_phrase = _sample_summary_join_with_and(
            _sample_summary_get_sample_term_names(request, sample_obj)
        )
        disease_phrase = _sample_summary_get_disease_phrase(request, sample_obj)
        if disease_phrase:
            tissue_phrases_with_disease.add(
                f'{disease_phrase} {_format_tissue_phrase(sample_term_phrase)}'.strip()
            )

    if tissue_phrases_with_disease:
        return _sample_summary_join_with_and(tissue_phrases_with_disease)

    # Only use slim grouping when there are more than 2 unique tissue terms.
    if len(all_term_names) <= 2:
        parts = [_format_tissue_phrase(name) for name in sorted(all_term_names)]
        return _sample_summary_join_with_and(parts)

    return _build_tissue_slim_group_phrase()


def _sample_summary_build_single_sample_phrase(request, sample_object):
    sample_classifications = set(sample_object.get('classifications', []))
    sample_terms = _sample_summary_get_sample_term_names(request, sample_object)
    sample_term_phrase = _sample_summary_join_with_and(sample_terms)
    targeted_sample_term_phrase = _sample_summary_get_targeted_sample_term_name(request, sample_object)
    disease_phrase = _sample_summary_get_disease_phrase(request, sample_object)

    pooled_prefix = 'pooled ' if 'pooled cell specimen' in sample_classifications else ''
    primary_prefix = 'primary ' if 'primary cell' in sample_classifications else ''
    embryonic_prefix = 'embryonic ' if sample_object.get('embryonic', False) else ''
    disease_prefix = f'{disease_phrase} ' if disease_phrase else ''
    organoid_sample_term = f'{embryonic_prefix}{sample_term_phrase}' if embryonic_prefix else sample_term_phrase

    if 'reprogrammed cell specimen' in sample_classifications:
        phrase = (
            f'{pooled_prefix}{disease_prefix}{primary_prefix}{sample_term_phrase} '
            f'reprogrammed to {targeted_sample_term_phrase}'
        ).strip()
    elif 'differentiated cell specimen' in sample_classifications:
        phrase = (
            f'{pooled_prefix}{disease_prefix}{primary_prefix}{sample_term_phrase} '
            f'differentiated to {targeted_sample_term_phrase}'
        ).strip()
    elif 'tissue/organ' in sample_classifications:
        phrase = f'{disease_prefix}{sample_term_phrase} tissue'.strip()
    else:
        organoid_type = get_first_matching_classification(
            sample_classifications,
            ['gastruloid', 'embryoid', 'organoid']
        )
        if organoid_type:
            phrase = f'{organoid_sample_term} {organoid_type}'.strip()
        elif 'primary cell' in sample_classifications:
            phrase = f'{disease_prefix}primary {sample_term_phrase}'.strip()
        else:
            phrase = f'{disease_prefix}{sample_term_phrase}'.strip()

    comparison_key = (
        tuple(sample_terms),
        tuple(sorted(sample_classifications)),
        disease_phrase,
        bool(sample_object.get('embryonic', False)),
    )
    return {
        'phrase': phrase,
        'comparison_key': comparison_key,
        'has_targeted_term': bool(targeted_sample_term_phrase),
    }


EMBEDDED_FILE_FIELDS = [
    '@id',
    'accession',
    'aliases',
    'assembly',
    'anvil_url',
    'content_type',
    'controlled_access',
    'creation_timestamp',
    'derived_from',
    'file_format',
    'file_format_type',
    'file_size',
    'flowcell_id',
    'href',
    'illumina_read_type',
    'lane',
    'md5sum',
    'mean_read_length',
    's3_uri',
    'sequencing_run',
    'sequencing_kit',
    'sequencing_platform',
    'seqspecs',
    'seqspec_document',
    'submitted_file_name',
    'status',
    'summary',
    'transcriptome_annotation',
    'upload_status',
    'workflows',
]


@abstract_collection(
    name='file-sets',
    unique_key='accession',
    properties={
        'title': 'File Sets',
        'description': 'Listing of file sets',
    }
)
class FileSet(Item):
    item_type = 'file_set'
    base_types = ['FileSet'] + Item.base_types
    name_key = 'accession'
    schema = load_schema('igvfd:schemas/file_set.json')
    rev = {
        'files': ('File', 'file_set'),
        'control_for': ('FileSet', 'control_file_sets'),
        'input_for': ('FileSet', 'input_file_sets'),
        'superseded_by': ('FileSet', 'supersedes')
    }
    embedded_with_frame = [
        Path('award.contact_pi', include=['@id', 'contact_pi', 'component', 'title']),
        Path('lab', include=['@id', 'title']),
        Path('submitted_by', include=['@id', 'title']),
        Path(
            'files',
            include=EMBEDDED_FILE_FIELDS
        ),
        Path(
            'files.sequencing_platform',
            include=[
                '@id',
                'term_name',
                'status'
            ]
        ),
        Path(
            'files.imaging_platform',
            include=[
                '@id',
                'term_name',
                'status'
            ]
        ),
        Path(
            'files.workflows',
            include=[
                '@id',
                'accession',
            ]
        ),
        Path('control_for', include=['@id', 'accession', 'aliases', 'status']),
        Path('donors', include=['@id', 'accession', 'aliases', 'sex', 'status', 'strain_background', 'taxa']),
        Path(
            'samples.sample_terms',
            include=[
                '@id',
                '@type',
                'accession',
                'aliases',
                'treatments',
                'cellular_sub_pool',
                'classifications',
                'phenotypic_features',
                'growth_medium',
                'modifications',
                'sample_terms',
                'status',
                'summary',
                'targeted_sample_term',
                'taxa',
                'term_name',
                'treatments',
                'institutional_certificates',
            ]
        ),
        Path('samples.phenotypic_features.feature', include=['@id', 'term_name', 'status']),
        Path('samples.targeted_sample_term', include=['@id', 'term_name', 'status']),
        Path('samples.modifications', include=['@id', 'modality', 'status']),
        Path('samples.treatments', include=['@id', 'treatment_term_name',
             'purpose', 'treatment_type', 'summary', 'status']),
        Path('samples.institutional_certificates', include=['@id',
             'certificate_identifier', 'status', 'data_use_limitation', 'data_use_limitation_modifiers', 'controlled_access']),
        Path('construct_library_sets', include=[
             '@id', 'accession', 'file_set_type', 'summary', 'status', 'selection_criteria', 'small_scale_gene_list', 'integrated_content_files', 'associated_phenotypes']),
        Path('construct_library_sets.integrated_content_files', include=[
             '@id', 'accession', 'summary', 'status', 'content_type']),
        Path('construct_library_sets.small_scale_gene_list', include=[
             '@id', 'summary', 'geneid', 'symbol', 'name', 'status']),
        Path('construct_library_sets.associated_phenotypes', include=[
             '@id', 'term_name', 'status']),
        Path('publications', include=['@id', 'publication_identifiers', 'status']),
    ]

    audit_inherit = [
        'award',
        'lab',
        'files',
        'documents',
        'samples',
        'samples.sample_terms',
        'samples.phenotypic_features',
        'samples.treatments',
        'samples.modifications',
        'donors',
    ]

    set_status_up = [
        'documents',
        'files',
        'input_file_sets',
        'samples'
    ]
    set_status_down = [
    ]

    @calculated_property(schema={
        'title': 'Files',
        'type': 'array',
        'description': 'The files associated with this file set.',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'File',
            'type': 'string',
            'linkFrom': 'File.file_set',
        },
        'notSubmittable': True
    })
    def files(self, request, files):
        return paths_filtered_by_status(request, files)

    @calculated_property(schema={
        'title': 'File Sets Controlled By This File Set',
        'type': 'array',
        'description': 'The file sets for which this file set is a control.',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'File Set Controlled By This File Set',
            'type': 'string',
            'linkFrom': 'FileSet.control_file_sets',
        },
        'notSubmittable': True
    })
    def control_for(self, request, control_for):
        return paths_filtered_by_status(request, control_for) or None

    @calculated_property(schema={
        'title': 'Superseded By',
        'description': 'File set(s) this file set is superseded by virtue of those file set(s) being newer, better, or a fixed version of etc. than this one.',
        'type': 'array',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Superseded By',
            'type': 'string',
            'linkFrom': 'FileSet.supersedes',
        },
        'notSubmittable': True
    })
    def superseded_by(self, request, superseded_by):
        return paths_filtered_by_status(request, superseded_by) or None

    @calculated_property(schema={
        'title': 'Submitted Files Timestamp',
        'description': 'The timestamp the first file object in the file_set or associated auxiliary sets was created.',
        'comment': 'Do not submit. The timestamp is automatically calculated.',
        'type': 'string',
        'format': 'date-time',
        'notSubmittable': True
    })
    def submitted_files_timestamp(self, request, files, auxiliary_sets=None):
        if auxiliary_sets is None:
            auxiliary_sets = []
        timestamps = set()
        files_to_traverse = []
        if files:
            files_to_traverse.extend(files)
        if auxiliary_sets:
            for auxiliary_set in auxiliary_sets:
                aux_set_object = request.embed(auxiliary_set, '@@object_with_select_calculated_properties?field=files')
                if 'files' in aux_set_object:
                    files_to_traverse.extend(aux_set_object['files'])
        for current_file_path in files_to_traverse:
            file_object = request.embed(current_file_path, '@@object?skip_calculated=true')
            timestamp = file_object.get('creation_timestamp', None)
            if timestamp:
                timestamps.add(timestamp)
        if timestamps:
            res = sorted(timestamps, key=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f%z'))
            return res[0]

    @calculated_property(schema={
        'title': 'Input For',
        'description': 'The file sets that use this file set as an input.',
        'type': 'array',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Input For',
            'type': 'string',
            'linkFrom': 'FileSet.input_file_sets',
        },
        'notSubmittable': True
    })
    def input_for(self, request, input_for):
        return paths_filtered_by_status(request, input_for) or None

    @calculated_property(
        define=True,
        condition='samples',
        schema={
            'title': 'Construct Library Sets',
            'description': 'The construct library sets associated with the samples of this file set.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Construct Library Set',
                'description': 'A construct library set associated with a sample of this file set.',
                'type': 'string',
                'linkTo': 'FileSet',
            },
            'notSubmittable': True
        })
    def construct_library_sets(self, request, samples=None):
        construct_library_sets = set()
        if self.item_type != 'construct_library_set':  # construct library sets should not calculate construct_library_sets
            for sample in samples:
                sample_object = request.embed(sample,
                                              '@@object_with_select_calculated_properties?'
                                              'field=construct_library_sets'
                                              )
                if sample_object.get('construct_library_sets', []):
                    construct_library_sets = construct_library_sets | set(
                        sample_object.get('construct_library_sets', []))
        return sorted(construct_library_sets) or None

    @calculated_property(
        condition='samples',
        schema={
            'title': 'Data Use Limitation Summaries',
            'description': 'The data use limitation summaries of institutional certificates covering the sample associated with this file set which are signed by the same lab (or their partner lab) as the lab that submitted this file set.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Data Use Limitation Summary',
                'description': 'A combination of the data use limitation and its modifiers.',
                'type': 'string'
            },
            'notSubmittable': True,
        }
    )
    def data_use_limitation_summaries(self, request, lab, samples=None):
        summaries_to_return = []
        for sample in samples:
            sample_object = request.embed(
                sample, '@@object_with_select_calculated_properties?field=institutional_certificates')
            for ic in sample_object.get('institutional_certificates', []):
                ic_object = request.embed(
                    ic, '@@object_with_select_calculated_properties?field=data_use_limitation_summary')
                ic_labs = [ic_object.get('lab', None)] + ic_object.get('partner_labs', [])
                if lab in ic_labs:
                    summaries_to_return.append(ic_object.get('data_use_limitation_summary', None))
        if summaries_to_return:
            return sorted(set(summaries_to_return))
        else:
            return ['no certificate']

    @calculated_property(
        condition='samples',
        schema={
            'title': 'Controlled Access',
            'description': 'The controlled access of the institutional certificates covering the sample associated with this file set which are signed by the same lab (or their partner lab) as the lab that submitted this file set.',
            'type': 'boolean',
            'notSubmittable': True,
        }
    )
    def controlled_access(self, request, lab, samples=None):
        controlled_access_to_return = []
        for sample in samples:
            sample_object = request.embed(
                sample, '@@object_with_select_calculated_properties?field=institutional_certificates')
            for ic in sample_object.get('institutional_certificates', []):
                ic_object = request.embed(ic, '@@object?skip_calculated=true')
                ic_labs = [ic_object.get('lab', None)] + ic_object.get('partner_labs', [])
                if lab in ic_labs:
                    controlled_access_to_return.append(ic_object.get('controlled_access'))
        if controlled_access_to_return:
            if any(controlled_access_to_return):
                return True
            else:
                return False


@collection(
    name='analysis-sets',
    unique_key='accession',
    properties={
        'title': 'Analysis Sets',
        'description': 'Listing of analysis sets',
    }
)
class AnalysisSet(FileSet):
    item_type = 'analysis_set'
    schema = load_schema('igvfd:schemas/analysis_set.json')
    embedded_with_frame = FileSet.embedded_with_frame + [
        Path('input_file_sets', include=['@id', 'accession', 'aliases', 'file_set_type', 'status', 'assay_term']),
        Path('input_file_sets.assay_term', include=['@id', 'term_name', 'assay_slims']),
        Path('functional_assay_mechanisms', include=['@id', 'term_id', 'term_name', 'status']),
        Path('workflows', include=['@id', 'accession', 'name', 'uniform_pipeline', 'status', 'workflow_version']),
        Path('targeted_genes', include=['@id', 'symbol'])]
    audit_inherit = FileSet.audit_inherit
    set_status_up = FileSet.set_status_up + [
        'pipeline_parameters'
    ]
    set_status_down = FileSet.set_status_down + []

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, request, file_set_type, input_file_sets=None, files=None, samples=None, construct_library_sets=None):
        if input_file_sets is None:
            input_file_sets = []
        if files is None:
            files = []
        if samples is None:
            samples = []
        if construct_library_sets is None:
            construct_library_sets = []

        inspected_filesets = set()
        fileset_subclasses = set()
        target_assays = ['10x multiome', '10x multiome with MULTI-seq', 'SHARE-seq', 'Multiome Perturb-seq']

        fileset_types = set()
        file_content_types = set()
        targeted_genes = set()
        assay_terms = set()
        cls_derived_assay_titles = set()

        all_assay_summaries = set()
        cls_type_set = set()
        cls_set = set()
        control_type_set = set()
        crispr_modalities = set()
        multiplexing_methods = set()
        crispr_screen_terms = [
            '/assay-terms/OBI_0003659/',
            '/assay-terms/OBI_0003661/',
            '/assay-terms/OBI_0003660/',  # in vitro CRISPR screen using single-cell RNA-seq
            '/assay-terms/NTR_0000798/',  # in vitro CRISPR screen using single-cell ATAC-seq
            '/assay-terms/NTR_0001101/',  # in vivo CRISPR screen using single cell RNA-seq
        ]
        any_sample_sorted_from = False

        def format_assay(assay_titles, preferred_assay_titles):
            if any(t in target_assays for t in preferred_assay_titles):
                return f"{', '.join(assay_titles)} ({', '.join(preferred_assay_titles)})"
            return ', '.join(preferred_assay_titles or assay_titles)

        if input_file_sets:
            # The file_set_types are included based on the subclass
            # of only the directly associated input_file_sets, not
            # on the subclass of all file sets that are checked.
            for directly_linked_input in input_file_sets:
                fileset_object = request.embed(
                    directly_linked_input,
                    '@@object_with_select_calculated_properties?field=@type'
                )
                fileset_subclasses.add(fileset_object['@type'][0])
            filesets_to_inspect = set(input_file_sets.copy())
            while filesets_to_inspect:
                input_fileset = filesets_to_inspect.pop()
                if input_fileset not in inspected_filesets:
                    inspected_filesets.add(input_fileset)
                    fileset_object = get_file_set_props_for_summary_and_samples(request, input_fileset)
                    # Trace back from Analysis Sets to identify their
                    # input file sets.
                    if (input_fileset.startswith('/analysis-sets/') and
                            fileset_object.get('input_file_sets', False)):
                        for candidate_fileset in fileset_object.get('input_file_sets'):
                            if candidate_fileset not in inspected_filesets:
                                filesets_to_inspect.add(candidate_fileset)
                    # Retrieve targeted_genes from Measurement Sets.
                    elif input_fileset.startswith('/measurement-sets/'):
                        if 'targeted_genes' in fileset_object:
                            for gene in fileset_object['targeted_genes']:
                                gene_object = request.embed(gene, '@@object?skip_calculated=true')
                                targeted_genes.add(gene_object['symbol'])
                        assay_terms.add(fileset_object['assay_term'])
                        preferred_assay_titles = fileset_object.get('preferred_assay_titles', [])
                        assays_titles = fileset_object.get('assay_titles', [])
                        summary = format_assay(assays_titles, preferred_assay_titles)
                        if summary:
                            all_assay_summaries.add(summary)
                    elif input_fileset.startswith('/auxiliary-sets/'):
                        measurement_sets = fileset_object.get('measurement_sets', [])
                        file_set_type = fileset_object.get('file_set_type')
                        if file_set_type:
                            fileset_types.add(file_set_type)
                        if measurement_sets:
                            for candidate_fileset in measurement_sets:
                                measurement_set_object = request.embed(
                                    candidate_fileset, '@@object?skip_calculated=true')
                                assay_terms.add(measurement_set_object['assay_term'])
                                if candidate_fileset not in inspected_filesets:
                                    filesets_to_inspect.add(candidate_fileset)
                    elif input_fileset.startswith('/construct-library-sets/'):
                        preferred_assay_titles = fileset_object.get('preferred_assay_titles', [])
                        assays_titles = fileset_object.get('assay_titles', [])
                        summary = format_assay(assays_titles, preferred_assay_titles)
                        if summary:
                            cls_derived_assay_titles.add(summary)
                    elif not input_fileset.startswith('/analysis-sets/'):
                        fileset_types.add(fileset_object['file_set_type'])
                    # Collect control types.
                    if 'control_types' in fileset_object:
                        control_type_set = control_type_set | set(fileset_object['control_types'])

        # Collect content_types of files.
        if files:
            for file in files:
                file_object = request.embed(file, '@@object?skip_calculated=true')
                file_content_types.add(file_object['content_type'])

        # Collect construct library set summaries and types
        prop_with_cls = None
        only_cls_input = False
        if construct_library_sets:
            prop_with_cls = construct_library_sets
            only_cls_input = False
        elif fileset_subclasses.issubset({'ConstructLibrarySet', 'CuratedSet'}):
            prop_with_cls = [
                input_file_set for input_file_set in input_file_sets
                if input_file_set.startswith('/construct-library-sets/')
            ]
            only_cls_input = True
        if prop_with_cls:
            for construct_library_set in prop_with_cls:
                construct_library_set_object = request.embed(
                    construct_library_set, '@@object_with_select_calculated_properties?field=summary')
                cls_type_set.add(construct_library_set_object['file_set_type'])
                cls_set.add(construct_library_set_object['summary'])
        cls_phrase = ''
        if len(cls_set) > 0:
            cls_phrase = get_cls_phrase(cls_set, only_cls_input=only_cls_input)

        # Collect CRISPR modalities, file set type, and sorted_from from associated samples.
        if samples:
            for sample in samples:
                sample_object = request.embed(sample, '@@object?skip_calculated=true')
                if 'sorted_from' in sample_object:
                    any_sample_sorted_from = True
                if 'modifications' in sample_object and 'guide library' in cls_type_set:
                    for modification in sample_object['modifications']:
                        modification_object = request.embed(modification, '@@object?skip_calculated=true')
                        crispr_modalities.add(modification_object['modality'])
                if 'multiplexing_methods' in sample_object:
                    for method in sample_object['multiplexing_methods']:
                        multiplexing_methods.add(method)

        # Assay titles if there are input file sets, otherwise unspecified.
        # Only use the CLS derived assay titles if there were no other assay titles.
        if cls_derived_assay_titles and not all_assay_summaries:
            all_assay_summaries = cls_derived_assay_titles
        assay_title_phrase = 'Unspecified assay'
        if all_assay_summaries:
            assay_title_phrase = ', '.join(sorted(all_assay_summaries))
        if 'guide library' in cls_type_set:
            if 'CRISPR' not in assay_title_phrase:
                assay_title_phrase = f'CRISPR {assay_title_phrase}'
        # Add modalities to the assay titles.
        if crispr_modalities:
            if len(crispr_modalities) > 1:
                modality_set = ', '.join(crispr_modalities)
            elif len(crispr_modalities) == 1:
                modality_set = ''.join(crispr_modalities)
            if 'CRISPR' in assay_title_phrase:
                assay_title_phrase = assay_title_phrase.replace('CRISPR', f'CRISPR {modality_set}')
            else:
                assay_title_phrase = f'{modality_set} {assay_title_phrase}'
        if multiplexing_methods:
            method_phrase_map = {
                'barcode based': 'barcode based',
                'genetic': 'genetically'
            }
            mux_method_list = [method_phrase_map[x] for x in sorted(multiplexing_methods)]
            mux_method_phrase = f'({", ".join(mux_method_list)} multiplexed)'
            assay_title_phrase = f'{assay_title_phrase} {mux_method_phrase}'
        # Targeted genes: "sorted on expression of X" when samples have sorted_from (flow cytometry), else "targeting X".
        targeted_genes_phrase = ''
        if targeted_genes:
            if any_sample_sorted_from:
                targeted_genes_phrase = f'sorted on expression of {", ".join(sorted(targeted_genes))}'
            else:
                targeted_genes_phrase = f'targeting {", ".join(sorted(targeted_genes))}'
        # The file set types are only shown if the inputs are all Auxiliary Sets
        # and the Measurement Sets related to the Auxiliary Sets are not CRISPR screens.
        file_set_type_phrase = ''
        if fileset_types and len(fileset_subclasses) == 1 and ('AuxiliarySet' in fileset_subclasses):
            if not assay_terms:
                file_set_type_phrase = ', '.join(fileset_types)
            elif not all(x in crispr_screen_terms for x in assay_terms):
                file_set_type_phrase = ', '.join(fileset_types)

        control_phrase = ''
        if len(control_type_set) > 0:
            suffix = ''
            if len(control_type_set) > 1:
                suffix = 's'
            control_types = [control_type for control_type in control_type_set if control_type not in cls_phrase]
            if control_types:
                control_phrase = f'with {", ".join(sorted(control_types))} control{suffix}'

        all_phrases = [
            assay_title_phrase,
            targeted_genes_phrase,
            cls_phrase,
            file_set_type_phrase,
            control_phrase
        ]
        merged_phrase = ' '.join([x for x in all_phrases if x != '']).replace(' : ', ': ')
        if merged_phrase:
            return merged_phrase
        else:
            # Failsafe return value.
            return file_set_type

    @calculated_property(
        define=True,
        schema={
            'title': 'Preferred Assay Titles',
            'description': 'Preferred Assay Title(s) of assays that produced data analyzed in the analysis set.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Preferred Assay Titles',
                'description': 'Title of assay that produced data analyzed in the analysis set.',
                'type': 'string'
            },
            'notSubmittable': True,
        }
    )
    def preferred_assay_titles(self, request, input_file_sets=None):
        if input_file_sets is None:
            input_file_sets = []
        preferred_assay_list = set()
        for fileset in input_file_sets:
            file_set_object = request.embed(
                fileset,
                '@@object_with_select_calculated_properties?field=preferred_assay_titles'
            )
            preferred_assay_list.update(
                file_set_object.get(
                    'preferred_assay_titles',
                    []
                )
            )
        return sorted(preferred_assay_list)

    @calculated_property(
        define=True,
        schema={
            'title': 'Assay Term Names',
            'description': 'Ontology term names from Ontology of Biomedical Investigations (OBI) for assays',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Assay Term Names',
                'description': 'Title of assay that produced data analyzed in the analysis set.',
                'type': 'string'
            },
            'notSubmittable': True,
        }
    )
    def assay_titles(self, request, input_file_sets=None):
        if input_file_sets is None:
            input_file_sets = []
        assay_list = set()
        for fileset in input_file_sets:
            file_set_object = request.embed(
                fileset,
                '@@object_with_select_calculated_properties?field=assay_titles'
            )
            assay_list.update(
                file_set_object.get(
                    'assay_titles',
                    []
                )
            )
        return sorted(assay_list) or None

    @calculated_property(
        define=True,
        schema={
            'title': 'Assay Slims',
            'description': 'A broad categorization of the assay term.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'type': 'string'
            },
            'notSubmittable': True,
        }
    )
    def assay_slims(self, request, input_file_sets=None):
        if input_file_sets is None:
            input_file_sets = []
        assay_type = set()
        for fileset in input_file_sets:
            file_set_object = request.embed(
                fileset,
                '@@object_with_select_calculated_properties?field=assay_slims'
            )
            assay_type.update(
                file_set_object.get(
                    'assay_slims',
                    []
                )
            )
        return sorted(assay_type) or None

    @calculated_property(
        condition='input_file_sets',
        define=True,
        schema={
            'title': 'Samples',
            'description': 'Samples associated with this analysis set.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Sample',
                'description': 'Sample associated with this analysis set.',
                'type': 'string',
                'linkTo': 'Sample'
            },
            'notSubmittable': True,
        }
    )
    def samples(self, request, input_file_sets=None, demultiplexed_samples=None):
        samples = set()
        if input_file_sets is not None:
            for fileset in input_file_sets:
                if not (fileset.startswith('/construct-library-sets/')):
                    # Change the embed link to match summary() to reduce the amount of data caching.
                    # These two funcs use similary query links that will look up the samples property.
                    input_file_set_object = get_file_set_props_for_summary_and_samples(request, fileset)
                    input_file_set_samples = set(input_file_set_object.get('samples', []))
                    if input_file_set_samples:
                        samples = samples | input_file_set_samples
            if demultiplexed_samples:
                # if the analysis set specifies a demultiplexed sample and all input data is multiplexed return just the demultiplexed_sample
                if not ([sample for sample in samples if not (sample.startswith('/multiplexed-samples/'))]):
                    return demultiplexed_samples
        return sorted(samples)

    @calculated_property(
        condition='samples',
        schema={
            'title': 'Donors',
            'description': 'The donors of the samples associated with this analysis set.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Donor',
                'description': 'Donor of a sample associated with this analysis set.',
                'type': 'string',
                'linkTo': 'Donor'
            },
            'notSubmittable': True,
        }
    )
    def donors(self, request, samples=None):
        return get_donors_from_samples(request, samples)

    @calculated_property(
        schema={
            'title': 'Protocols',
            'description': 'Links to the protocol(s) for conducting the assay on Protocols.io.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Protocol',
                'type': 'string',
                'pattern': '^https://www\\.protocols\\.io/(private|view)/(\\S+)$'
            },
            'notSubmittable': True
        }
    )
    def protocols(self, request, input_file_sets=None):
        '''Calculate an array of unique protocols for all measurement sets associated with an analysis set.'''
        protocols = set()
        file_set_objs = []
        if input_file_sets is None:
            input_file_sets = []
        for fileset in input_file_sets:
            file_set_objs.append(
                request.embed(
                    fileset,
                    '@@object_with_select_calculated_properties?field=@type&field=protocols'
                )
            )
        for file_set_obj in file_set_objs:
            if 'MeasurementSet' in file_set_obj.get('@type'):
                protocol = file_set_obj.get('protocols', [])
                protocols.update(protocol)
        return sorted(protocols) or None

    @calculated_property(
        condition='samples',
        schema={
            'title': 'Simplified Sample Summary',
            'description': 'A summary of the samples associated with input file sets of this analysis set.',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def sample_summary(self, request, samples=None):
        if not samples:
            return None

        sample_objects = [request.embed(sample, '@@object') for sample in samples]
        all_classifications = set()
        taxa_values = set()
        for sample_object in sample_objects:
            all_classifications.update(sample_object.get('classifications', []))
            taxa_values.add(_sample_summary_get_taxa(sample_object))
        taxa_phrase = _get_sample_summary_taxa_phrase(taxa_values)

        if 'multiplexed sample' in all_classifications:
            mux_sample_term_names = set()
            mux_tissue_sample_objs = []
            mux_donor_accessions = set()
            mux_donor_strains = set()
            mux_donor_taxa = set()
            mux_taxa_values = set()
            mux_has_mixed_taxa = False
            for sample_object in sample_objects:
                multiplexed_samples = sample_object.get('multiplexed_samples', [])
                for multiplexed_sample in multiplexed_samples:
                    multiplexed_sample_obj = request.embed(multiplexed_sample, '@@object')
                    mux_donor_data = _sample_summary_get_donor_data(request, multiplexed_sample_obj)
                    mux_donor_accessions.update(mux_donor_data['accessions'])
                    mux_donor_strains.update(mux_donor_data['strains'])
                    mux_donor_taxa.update(mux_donor_data['taxa'])
                    mux_taxa_values.add(_sample_summary_get_taxa(multiplexed_sample_obj))
                    mux_classifications = set(multiplexed_sample_obj.get('classifications', []))
                    if 'tissue/organ' in mux_classifications:
                        mux_tissue_sample_objs.append(multiplexed_sample_obj)
                    else:
                        for sample_term in multiplexed_sample_obj.get('sample_terms', []):
                            term_name = _sample_summary_get_term_name(request, sample_term)
                            if term_name:
                                mux_sample_term_names.add(term_name)

            # taxa phrase
            mux_taxa_phrase = _get_sample_summary_taxa_phrase(mux_taxa_values)
            mux_all_phrases = list(mux_sample_term_names)
            if mux_tissue_sample_objs:
                tissue_phrase = _sample_summary_build_tissue_group_phrase(
                    request,
                    mux_tissue_sample_objs,
                )
                if tissue_phrase:
                    mux_all_phrases.append(tissue_phrase)
            sample_term_phrase = _sample_summary_join_with_and(mux_all_phrases) if mux_all_phrases else ''
            donor_phrase = ''
            is_all_mouse_donors = mux_donor_taxa and mux_donor_taxa == {'Mus musculus'}
            if is_all_mouse_donors and mux_donor_strains:
                if len(mux_donor_strains) == 1:
                    donor_phrase = f'from {sorted(mux_donor_strains)[0]} mouse'
                else:
                    donor_phrase = f'from {len(mux_donor_accessions)} mice of {len(mux_donor_strains)} strains'
            else:
                donor_count = len(mux_donor_accessions)
                donor_phrase = f'from {donor_count} donors'
                if donor_count == 1:
                    donor_phrase = f'from donor {sorted(mux_donor_accessions)[0]}'
            return f'{mux_taxa_phrase} multiplexed sample of {sample_term_phrase} {donor_phrase}'.strip()

        donor_accessions = set()
        donor_strains = set()
        donor_taxa = set()
        for sample_object in sample_objects:
            donor_data = _sample_summary_get_donor_data(request, sample_object)
            donor_accessions.update(donor_data['accessions'])
            donor_strains.update(donor_data['strains'])
            donor_taxa.update(donor_data['taxa'])

        donor_phrase = ''
        is_all_mouse_donors = donor_taxa and donor_taxa == {'Mus musculus'}
        if is_all_mouse_donors and donor_strains:
            if len(donor_strains) == 1:
                donor_phrase = f' from {sorted(donor_strains)[0]}'
            else:
                donor_phrase = f' from {len(donor_accessions)} mice of {len(donor_strains)} strains'
        else:
            if len(donor_accessions) == 1:
                donor_phrase = f' from donor {sorted(donor_accessions)[0]}'
            elif len(donor_accessions) > 1:
                donor_phrase = f' from {len(donor_accessions)} donors'

        tissue_sample_objs = [
            s for s in sample_objects
            if 'tissue/organ' in set(s.get('classifications', []))
        ]
        non_tissue_sample_objs = [
            s for s in sample_objects
            if 'tissue/organ' not in set(s.get('classifications', []))
        ]

        candidates_by_key = {}
        for sample_object in non_tissue_sample_objs:
            sample_phrase_data = _sample_summary_build_single_sample_phrase(
                request,
                sample_object,
            )
            key = sample_phrase_data['comparison_key']
            if key not in candidates_by_key:
                candidates_by_key[key] = sample_phrase_data
            elif sample_phrase_data['has_targeted_term'] and not candidates_by_key[key]['has_targeted_term']:
                candidates_by_key[key] = sample_phrase_data

        all_phrases = [d['phrase'] for d in candidates_by_key.values()]
        if tissue_sample_objs:
            tissue_phrase = _sample_summary_build_tissue_group_phrase(
                request,
                tissue_sample_objs,
            )
            if tissue_phrase:
                all_phrases.append(tissue_phrase)

        sample_phrase = _sample_summary_join_with_and(all_phrases)
        return f'{taxa_phrase} {sample_phrase}{donor_phrase}'.strip()

    @calculated_property(
        schema={
            'title': 'Functional Assay Mechanisms',
            'description': 'The biological processes measured by the functional assays.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Phenotype Term',
                'type': 'string',
                'linkTo': 'PhenotypeTerm'
            },
            'notSubmittable': True
        }
    )
    def functional_assay_mechanisms(self, request, input_file_sets=None):
        mechanism_objects = []
        file_set_objs = []
        if input_file_sets is None:
            input_file_sets = []
        for fileset in input_file_sets:
            file_set_objs.append(
                request.embed(
                    fileset,
                    '@@object_with_select_calculated_properties?field=@type&field=functional_assay_mechanisms'
                )
            )
        for file_set_object in file_set_objs:
            if 'MeasurementSet' in file_set_object.get('@type') or 'AnalysisSet' in file_set_object.get('@type'):
                mechanism_objects.extend(file_set_object.get('functional_assay_mechanisms', []))
        return sorted(set(mechanism_objects)) or None

    @calculated_property(
        schema={
            'title': 'Workflows',
            'description': 'A workflow for computational analysis of genomic data. A workflow is made up of analysis steps.',
            'type': 'array',
            'notSubmittable': True,
            'uniqueItem': True,
            'minItems': 1,
            'items': {
                'title': 'Workflow',
                'type': 'string',
                'linkTo': 'Workflow'
            }
        }
    )
    def workflows(self, request, files=None):
        if files is None:
            files = []
        unique_workflows = set()
        for file_ in files:
            file_workflows = request.embed(
                file_,
                '@@object_with_select_calculated_properties?field=workflows',
            ).get('workflows', [])
            unique_workflows.update(file_workflows)
        return sorted(unique_workflows)

    @calculated_property(
        condition='input_file_sets',
        schema={
            'title': 'Targeted Genes',
            'description': 'A list of genes targeted by the input measurement sets assays.',
            'type': 'array',
            'notSubmittable': True,
            'uniqueItem': True,
            'minItems': 1,
            'items': {
                'title': 'Targeted Gene',
                'type': 'string',
                'linkTo': 'Gene'
            }
        }
    )
    def targeted_genes(self, request, input_file_sets=None):
        if input_file_sets is None:
            input_file_sets = []
        analysis_set_targeted_genes = set()
        for input_file_set in input_file_sets:
            if input_file_set.startswith(('/measurement-sets/', '/analysis-sets/')):
                input_file_set_object = request.embed(
                    input_file_set, '@@object_with_select_calculated_properties?field=targeted_genes')
                if 'targeted_genes' in input_file_set_object:
                    analysis_set_targeted_genes.update(input_file_set_object['targeted_genes'])
        return sorted(analysis_set_targeted_genes) or None

    @calculated_property(
        condition='input_file_sets',
        schema={
            'title': 'Enrichment Designs',
            'description': 'The enrichment designs used by the inputs of this analysis set.',
            'type': 'array',
            'notSubmittable': True,
            'uniqueItem': True,
            'minItems': 1,
            'items': {
                'title': 'Enrichment Design',
                'type': 'string',
                'linkTo': 'TabularFile'
            }
        }
    )
    def enrichment_designs(self, request, input_file_sets=None):
        if input_file_sets is None:
            input_file_sets = []
        analysis_set_enrichment_designs = set()
        for input_file_set in input_file_sets:
            if input_file_set.startswith(('/measurement-sets/', '/analysis-sets/')):
                input_file_set_object = request.embed(
                    input_file_set, '@@object?skip_calculated=true')
                if 'enrichment_designs' in input_file_set_object:
                    analysis_set_enrichment_designs.update(input_file_set_object['enrichment_designs'])
        return sorted(analysis_set_enrichment_designs) or None


@collection(
    name='curated-sets',
    unique_key='accession',
    properties={
        'title': 'Curated Sets',
        'description': 'Listing of curated sets',
    }
)
class CuratedSet(FileSet):
    item_type = 'curated_set'
    schema = load_schema('igvfd:schemas/curated_set.json')
    embedded_with_frame = FileSet.embedded_with_frame
    audit_inherit = FileSet.audit_inherit
    set_status_up = FileSet.set_status_up + []
    set_status_down = FileSet.set_status_down + []

    @calculated_property(
        define=True,
        schema={
            'title': 'Assay Term Names',
            'description': 'Ontology term names from Ontology of Biomedical Investigations (OBI) for assays',
            'type': 'array',
            'minItems': 1,
            'items': {
                'type': 'string'
            },
            'notSubmittable': True
        }
    )
    def assay_titles(self, request, assay_term=None):
        if assay_term:
            assay_term_obj = request.embed(assay_term, '@@object?skip_calculated=true')
            term_name = assay_term_obj.get('term_name')
            if term_name:
                return [term_name]

    @calculated_property(
        define=True,
        schema={
            'title': 'Assemblies',
            'description': 'The genome assemblies to which the referencing files in the file set are utilizing (e.g., GRCh38).',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Assembly',
                'type': 'string'
            },
            'notSubmittable': True,
        }
    )
    def assemblies(self, request, files=None):
        if files:
            assembly_values = set()
            for current_file_path in files:
                file_object = request.embed(current_file_path, '@@object?skip_calculated=true')
                if file_object.get('assembly'):
                    assembly_values.add(file_object.get('assembly'))
            return sorted(assembly_values) or None

    @calculated_property(
        define=True,
        schema={
            'title': 'Transcriptome Annotations',
            'description': 'The annotation versions of the reference resource.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Transcriptome Annotation',
                'type': 'string'
            },
            'notSubmittable': True,
        }
    )
    def transcriptome_annotations(self, request, files=None):
        if files:
            annotation_values = set()
            for current_file_path in files:
                file_object = request.embed(current_file_path, '@@object?skip_calculated=true')
                if file_object.get('transcriptome_annotation'):
                    annotation_values.add(file_object.get('transcriptome_annotation'))
            return sorted(annotation_values) or None

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, file_set_type, assemblies=None, transcriptome_annotations=None, taxa=None):
        summary_message = ''
        if taxa:
            summary_message += f'{taxa} '
        if assemblies:
            assembly_values_joined = ' '.join(assemblies)
            summary_message += f'{assembly_values_joined} '
        if transcriptome_annotations:
            annotation_values_joined = ' '.join(transcriptome_annotations)
            summary_message += f'{annotation_values_joined} '
        summary_message += file_set_type
        return summary_message


@collection(
    name='measurement-sets',
    unique_key='accession',
    properties={
        'title': 'Measurement Sets',
        'description': 'Listing of measurement sets',
    })
class MeasurementSet(FileSet):
    item_type = 'measurement_set'
    schema = load_schema('igvfd:schemas/measurement_set.json')
    embedded_with_frame = FileSet.embedded_with_frame + [
        Path('assay_term', include=['@id', 'term_name', 'assay_slims', 'status']),
        Path('control_file_sets', include=['@id', 'accession', 'aliases', 'status']),
        Path('related_measurement_sets.measurement_sets', include=['@id', 'accession', 'status', 'measurement_sets']),
        Path('auxiliary_sets', include=['@id', 'accession', 'aliases', 'file_set_type', 'status']),
        Path('targeted_genes', include=['@id', 'geneid', 'symbol', 'name', 'synonyms', 'status']),
        Path('functional_assay_mechanisms', include=['@id', 'term_id', 'term_name', 'status']),
        Path('input_for', include=['@id', 'accession', 'aliases', 'status', 'uniform_pipeline_status'])
    ]

    audit_inherit = FileSet.audit_inherit + [
        'auxiliary_sets',
        'assay_term'
    ]

    set_status_up = FileSet.set_status_up + [
        'assay_term',
        'auxiliary_sets',
        'enrichment_designs'
    ]
    set_status_down = FileSet.set_status_down + []

    @calculated_property(
        define=True,
        schema={
            'title': 'Assay Term Names',
            'description': 'Ontology term names from Ontology of Biomedical Investigations (OBI) for assays',
            'type': 'array',
            'minItems': 1,
            'items': {
                'type': 'string'
            },
            'notSubmittable': True
        }
    )
    def assay_titles(self, request, assay_term):
        if assay_term:
            assay_term_obj = request.embed(assay_term, '@@object?skip_calculated=true')
            term_name = assay_term_obj.get('term_name')
            if term_name:
                return [term_name]

    @calculated_property(
        define=True,
        schema={
            'title': 'Assay Slims',
            'description': 'A broad categorization of the assay term.',
            'type': 'array',
            'uniqueItems': True,
            'minItems': 1,
            'items': {
                'type': 'string'
            },
            'notSubmittable': True
        }
    )
    def assay_slims(self, request, assay_term):
        if assay_term:
            assay_term_obj = request.embed(assay_term, '@@object_with_select_calculated_properties?field=assay_slims')
            assay_types = assay_term_obj.get('assay_slims')
            if assay_types:
                return assay_types

    @calculated_property(
        schema={
            'title': 'Related Measurement Sets',
            'description': 'Measurement sets related to this one, grouped by relationship type.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Related Measurement Set Group',
                'description': 'A group of related measurement sets of a given series type.',
                'type': 'object',
                'properties': {
                    'measurement_sets': {
                        'title': 'Measurement Sets',
                        'description': 'Measurement sets related by this relationship.',
                        'type': 'array',
                        'items': {
                            'title': 'Related Measurement Set',
                            'description': 'Related measurement set.',
                            'type': 'string',
                            'linkTo': 'MeasurementSet',
                        },
                        'minItems': 1,
                        'uniqueItems': True,
                    },
                    'series_type': {
                        'title': 'Series Type',
                        'description': 'Type of relationship between this measurement set and the related measurement sets.',
                        'type': 'string',
                        'enum': [
                            'multiome',
                        ],
                    },
                },
                'required': ['measurement_sets', 'series_type'],
                'additionalProperties': False,
            },
            'notSubmittable': True,
        })
    def related_measurement_sets(self, request, samples=None, multiome_size=None):
        object_id = self.jsonld_id(request)
        related_multiome_datasets = set()

        for sample in samples:
            sample_object = request.embed(sample, '@@object_with_select_calculated_properties?field=file_sets')
            for file_set_id in sample_object.get('file_sets', []):
                if (
                    file_set_id.startswith('/measurement-sets/')
                    and file_set_id != object_id
                    and multiome_size
                ):
                    related_multiome_datasets.add(file_set_id)

        result = []

        if related_multiome_datasets:
            result.append({
                'series_type': 'multiome',
                'measurement_sets': sorted(related_multiome_datasets),
            })

        return result or None

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, request, assay_term, assay_titles, preferred_assay_titles=None, samples=None, control_types=None, targeted_genes=None, construct_library_sets=None):
        if construct_library_sets is None:
            construct_library_sets = []
        modality_set = set()
        cls_set = set()
        cls_type_set = set()
        multiplexing_methods = set()
        control_phrase = ''
        cls_phrase = ''
        modality_phrase = ''
        assay_phrase = ''
        target_phrase = ''

        if construct_library_sets:
            for construct_library_set in construct_library_sets:
                construct_library_set_object = request.embed(
                    construct_library_set, '@@object_with_select_calculated_properties?field=summary')
                cls_type_set.add(construct_library_set_object['file_set_type'])
                cls_set.add(construct_library_set_object['summary'])

        any_sample_sorted_from = False
        for sample in samples:
            sample_object = request.embed(sample, '@@object')
            if 'sorted_from' in sample_object:
                any_sample_sorted_from = True
            if sample_object.get('modifications') and 'guide library' in cls_type_set:
                for modification in sample_object.get('modifications'):
                    modality = request.embed(modification).get('modality', '')
                    if modality:
                        modality_set.add(modality)
            if 'multiplexing_methods' in sample_object:
                for method in sample_object['multiplexing_methods']:
                    multiplexing_methods.add(method)

        assay = assay_titles[0] if assay_titles else None
        preferred_assay_title = preferred_assay_titles[0]
        if preferred_assay_title in ['10x multiome', '10x multiome with MULTI-seq', 'SHARE-seq', 'Multiome Perturb-seq']:
            assay = f'{assay} ({preferred_assay_title})'
        else:
            assay = preferred_assay_title

        if targeted_genes:
            # "sorted on expression of" when samples have sorted_from (flow cytometry), else "targeting"
            if any_sample_sorted_from:
                target_phrase = f' sorted on expression of'
            else:
                target_phrase = f' targeting'
            if len(targeted_genes) > 5:
                target_phrase = f'{target_phrase} {len(targeted_genes)} genes'
            elif len(targeted_genes) <= 5:
                genes = []
                for targeted_gene in targeted_genes:
                    gene_object = request.embed(targeted_gene, '@@object?skip_calculated=true')
                    gene_name = (gene_object.get('symbol'))
                    genes.append(gene_name)
                genes = sorted(genes)
                target_phrase = f'{target_phrase} {", ".join(genes)}'

        if 'guide library' in cls_type_set:
            if 'CRISPR' not in assay:
                assay = f'CRISPR {assay}'

        if len(modality_set) > 0:
            modality_set = ', '.join(modality_set)
            if 'CRISPR' in assay:
                assay_phrase = assay.replace('CRISPR', f'CRISPR {modality_set}')
            else:
                modality_phrase = f'{modality_set} '
                assay_phrase = f'{assay}'
        if len(modality_set) == 0:
            assay_phrase = f'{assay}'
        if multiplexing_methods:
            method_phrase_map = {
                'barcode based': 'barcode based',
                'genetic': 'genetically'
            }
            mux_method_list = [method_phrase_map[x] for x in sorted(multiplexing_methods)]
            mux_method_phrase = f'({", ".join(mux_method_list)} multiplexed)'
            assay_phrase = f'{assay_phrase} {mux_method_phrase}'

        if len(cls_set) > 0:
            cls_phrase = f' {get_cls_phrase(cls_set)}'

        if control_types:
            non_redundant_control_types = [control_type for control_type in sorted(
                control_types) if control_type not in cls_phrase]
            if non_redundant_control_types:
                control_phrase = f'{", ".join(non_redundant_control_types)} '
        # Special case for Y2H assays if control_type is not specified.
        if request.embed(assay_term)['term_id'] == 'OBI:0000288' and control_types is None:
            control_phrase = 'post-selection '

        sentence = ''
        sentence_parts = [
            control_phrase,
            modality_phrase,
            assay_phrase,
            target_phrase,
            cls_phrase,
        ]
        for phrase in sentence_parts:
            if phrase != '':
                sentence += phrase
        return sentence

    @calculated_property(
        condition='samples',
        schema={
            'title': 'Donors',
            'description': 'The donors of the samples associated with this measurement set.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Donor',
                'description': 'Donor of a sample associated with this measurement set.',
                'type': 'string',
                'linkTo': 'Donor'
            },
            'notSubmittable': True,
        }
    )
    def donors(self, request, samples=None):
        return get_donors_from_samples(request, samples)

    @calculated_property(
        schema={
            'title': 'Externally Hosted',
            'type': 'boolean',
            'notSubmittable': True,
        }
    )
    def externally_hosted(self, request, files=None, preferred_assay_titles=None):
        externally_hosted_value = False
        external_assays = {
            'Cell painting',
            'Variant painting via fluorescence',
            'Variant painting via immunostaining',
        }
        for title in preferred_assay_titles:
            if title in external_assays:
                externally_hosted_value = True
        if files:
            for current_file_path in files:
                file_object = request.embed(
                    current_file_path,
                    '@@object?skip_calculated=true'
                )
                if file_object.get('externally_hosted'):
                    externally_hosted_value = True

        return externally_hosted_value


@collection(
    name='model-sets',
    unique_key='accession',
    properties={
        'title': 'Model Sets',
        'description': 'Listing of model sets',
    }
)
class ModelSet(FileSet):
    item_type = 'model_set'
    schema = load_schema('igvfd:schemas/model_set.json')
    embedded_with_frame = FileSet.embedded_with_frame + [
        Path('input_file_sets', include=['@id', 'accession', 'aliases', 'status']),
        Path('assay_terms', include=['@id', 'term_name', 'status']),
        Path('assessed_genes', include=['@id', 'geneid', 'symbol', 'name', 'synonyms', 'status']),
        Path('software_versions.software', include=['@id', 'summary',
             'software', 'title', 'source_url', 'status'])
    ]
    audit_inherit = FileSet.audit_inherit
    set_status_up = FileSet.set_status_up + [
        'software_versions'
    ]
    set_status_down = FileSet.set_status_down + []

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, request, file_set_type, model_name, model_version, prediction_objects, assessed_genes=None):
        # Get assessed genes phrase
        assessed_gene_phrase = get_assessed_gene_phrase(request, assessed_genes)
        return ' '.join(filter(None, [
            model_name,
            model_version,
            file_set_type,
            f'for {assessed_gene_phrase}' if assessed_genes else '',
            'predicting',
            ', '.join(prediction_objects)
        ]))

    @calculated_property(
        define=True,
        schema={
            'title': 'Assay Term Names',
            'description': 'Ontology term names from Ontology of Biomedical Investigations (OBI) for assays',
            'type': 'array',
            'minItems': 1,
            'items': {
                'type': 'string'
            },
            'notSubmittable': True
        }
    )
    def assay_titles(self, request, assay_terms=None):
        assay_list = set()
        if assay_terms:
            for assay_term in assay_terms:
                assay_term_obj = request.embed(assay_term, '@@object?skip_calculated=true')
                term_name = assay_term_obj.get('term_name')
                if term_name:
                    assay_list.add(term_name)
        return sorted(assay_list) if assay_list else None

    @calculated_property(
        schema={
            'title': 'Externally Hosted',
            'type': 'boolean',
            'notSubmittable': True,
        }
    )
    def externally_hosted(self, request, files=None):
        externally_hosted_value = False
        if files:
            for current_file_path in files:
                file_object = request.embed(current_file_path, '@@object?skip_calculated=true')
                if file_object.get('externally_hosted'):
                    externally_hosted_value = True
        return externally_hosted_value

    @calculated_property(
        schema={
            'title': 'Software Versions',
            'description': 'The software versions used to produce this predictive model.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Software Version',
                'description': 'A software version used to produce this predictive model.',
                'type': 'string',
                'linkTo': 'SoftwareVersion',
            },
            'notSubmittable': True

        }
    )
    def software_versions(self, request, files=None):
        software_versions = []
        if files:
            for file in files:
                if file.startswith('/model-files/'):
                    file_object = request.embed(file, '@@object?skip_calculated=true')
                    analysis_step_version = file_object.get('analysis_step_version', '')
                    if analysis_step_version:
                        analysis_step_version_object = request.embed(
                            analysis_step_version, '@@object?skip_calculated=true')
                        software_versions = software_versions + \
                            analysis_step_version_object.get('software_versions', [])
        return sorted(set(software_versions)) or None


@collection(
    name='auxiliary-sets',
    unique_key='accession',
    properties={
        'title': 'Auxiliary Sets',
        'description': 'Listing of auxiliary sets',
    })
class AuxiliarySet(FileSet):
    item_type = 'auxiliary_set'
    schema = load_schema('igvfd:schemas/auxiliary_set.json')
    embedded_with_frame = FileSet.embedded_with_frame + [
        Path('measurement_sets', include=['@id', 'accession', 'aliases', 'preferred_assay_titles', 'status']),
        Path('input_for', include=['@id', 'accession', 'aliases', 'status', 'uniform_pipeline_status'])
    ]
    audit_inherit = FileSet.audit_inherit
    rev = FileSet.rev | {'measurement_sets': ('MeasurementSet', 'auxiliary_sets')}
    set_status_up = FileSet.set_status_up + [

    ]
    set_status_down = FileSet.set_status_down + []

    @calculated_property(schema={
        'title': 'Measurement Sets',
        'description': 'The measurement sets that link to this auxiliary set.',
        'type': 'array',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Measurement Set',
            'type': 'string',
            'linkFrom': 'MeasurementSet.auxiliary_sets',
        },
        'notSubmittable': True
    })
    def measurement_sets(self, request, measurement_sets):
        return paths_filtered_by_status(request, measurement_sets)

    @calculated_property(
        condition='measurement_sets',
        define=True,
        schema={
            'title': 'Preferred Assay Titles',
            'description': 'The preferred assay titles of the measurement sets that used this auxiliary set.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Preferred Assay Title',
                'type': 'string'
            },
            'notSubmittable': True
        })
    def preferred_assay_titles(self, request, measurement_sets=None):
        if measurement_sets is None:
            measurement_sets = []
        preferred_assay_titles = set()
        for measurement_set in measurement_sets:
            preferred_assays = request.embed(
                measurement_set, '@@object?skip_calculated=true').get('preferred_assay_titles', [])
            if preferred_assays:
                preferred_assay_titles.update(preferred_assays)
        return sorted(preferred_assay_titles)

    @calculated_property(
        condition='measurement_sets',
        define=True,
        schema={
            'title': 'Assay Term Names',
            'description': 'Ontology term names from Ontology of Biomedical Investigations (OBI) for assays',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Assay Term Names',
                'type': 'string'
            },
            'notSubmittable': True
        })
    def assay_titles(self, request, measurement_sets=None):
        if measurement_sets is None:
            measurement_sets = []
        assay_titles = set()
        for measurement_set in measurement_sets:
            assays = request.embed(
                measurement_set, '@@object_with_select_calculated_properties?field=assay_titles').get('assay_titles', [])
            if assays:
                assay_titles.update(assays)
        return sorted(assay_titles)

    @calculated_property(
        condition='measurement_sets',
        define=True,
        schema={
            'title': 'Assay Slims',
            'description': 'A broad categorization of the assay term.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'type': 'string'
            },
            'notSubmittable': True
        })
    def assay_slims(self, request, measurement_sets=None):
        if measurement_sets is None:
            measurement_sets = []
        assay_types = set()
        for measurement_set in measurement_sets:
            assays = request.embed(
                measurement_set, '@@object_with_select_calculated_properties?field=assay_slims').get('assay_slims', [])
            if assays:
                assay_types.update(assays)
        return sorted(assay_types)

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, request, file_set_type, measurement_sets=None):
        if not measurement_sets:
            return f'{file_set_type}'
        measurement_sets_summaries = sorted(set(
            [request.embed(measurement_set, '@@object_with_select_calculated_properties?field=summary').get('summary') for measurement_set in measurement_sets if measurement_set]))
        return f'{file_set_type} for {", ".join(measurement_sets_summaries)}'

    @calculated_property(
        condition='samples',
        schema={
            'title': 'Donors',
            'description': 'The donors of the samples associated with this auxiliary set.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Donor',
                'description': 'Donor of a sample associated with this auxiliary set.',
                'type': 'string',
                'linkTo': 'Donor'
            },
            'notSubmittable': True,
        }
    )
    def donors(self, request, samples=None):
        return get_donors_from_samples(request, samples)


@collection(
    name='prediction-sets',
    unique_key='accession',
    properties={
        'title': 'Prediction Sets',
        'description': 'Listing of prediction sets',
    })
class PredictionSet(FileSet):
    item_type = 'prediction_set'
    schema = load_schema('igvfd:schemas/prediction_set.json')
    embedded_with_frame = FileSet.embedded_with_frame + [
        Path('samples.construct_library_sets', include=['@id', 'accession', 'summary', 'status']),
        Path('large_scale_gene_list', include=['@id', 'accession', 'aliases', 'status']),
        Path('large_scale_loci_list', include=['@id', 'accession', 'aliases', 'status']),
        Path('small_scale_gene_list', include=['@id', 'geneid', 'symbol', 'name', 'synonyms', 'status']),
        Path('assessed_genes', include=['@id', 'geneid', 'symbol', 'name', 'synonyms', 'status']),
        Path('associated_phenotypes', include=['@id', 'term_id', 'term_name', 'status']),
        Path('software_versions.software', include=['@id', 'summary',
             'software', 'title', 'source_url', 'download_id', 'status'])
    ]
    audit_inherit = FileSet.audit_inherit
    set_status_up = FileSet.set_status_up + []
    set_status_down = FileSet.set_status_down + []

    @calculated_property(
        define=True,
        schema={
            'title': 'Software Versions',
            'description': 'The software versions used to produce this prediction.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Software Version',
                'description': 'A software version used to produce this prediction.',
                'type': 'string',
                'linkTo': 'SoftwareVersion',
            },
            'notSubmittable': True

        }
    )
    def software_versions(self, request, files=None):
        software_versions = []
        files = paths_filtered_by_status(request, files)
        if files:
            for file in files:
                file_object = request.embed(file, '@@object?skip_calculated=true')
                analysis_step_version = file_object.get('analysis_step_version', '')
                if analysis_step_version:
                    analysis_step_version_object = request.embed(
                        analysis_step_version, '@@object?skip_calculated=true')
                    software_versions = software_versions + \
                        analysis_step_version_object.get('software_versions', [])
        return sorted(set(software_versions)) or None

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'description': 'A summary of the prediction set.',
            'notSubmittable': True,
        }
    )
    def summary(self, request, file_set_type, software_versions=None, assessed_genes=None, scope=None, files=None, samples=None, donors=None, associated_phenotypes=None):
        # Get scope info
        scope_phrase = ''
        if scope:
            scope_phrase = f' on scope of {scope}'
        software_version_phrase = None
        software_version_summaries = set()
        if software_versions:
            for software_version in software_versions:
                software_version_object = request.embed(
                    software_version, '@@object_with_select_calculated_properties?field=summary')
                software_version_summaries.add(software_version_object['summary'])
        if software_version_summaries:
            software_version_phrase = f'using {", ".join(sorted(list(software_version_summaries)))}'
        # Get assessed genes info
        assessed_genes_phrase = get_assessed_gene_phrase(request, assessed_genes)
        # Get associated phenotypes info
        phenotypes_phrase = ''
        if associated_phenotypes:
            if len(associated_phenotypes) > 3:
                phenotypes_phrase = f'associated with {len(associated_phenotypes)} phenotypes'
            else:
                phenotype_term_names = sorted([request.embed(phenotype, '@@object?skip_calculated=true').get('term_name')
                                              for phenotype in associated_phenotypes])
                phenotypes_phrase = f'associated with {", ".join(phenotype_term_names)}'
        # Get sample or donor info
        taxa = set()
        samples_phrase = ''
        if donors:  # for generic human/mouse prediction, only add taxa phrase to summary
            virtual_phrase = 'virtual '
            # only put 'virtual' in final summary if all donors are virtual
            for donor in donors:
                donor_object = request.embed(donor, '@@object?skip_calculated=true')
                taxa.add(donor_object.get('taxa', ''))
                if not donor_object.get('virtual'):
                    virtual_phrase = ''
            samples_phrase = f'{virtual_phrase}{", ".join(sorted(taxa))}'
        else:  # for sample-specific predictions, use sample count in summary if the list is long
            if len(samples) > 3:
                virtual_phrase = 'virtual '
                taxa_phrase = ''
                for sample in samples:
                    sample_object = request.embed(sample, '@@object')
                    taxa.add(sample_object.get('taxa', ''))
                    # only put 'virtual' in final summary if all samples are virtual
                    if 'virtual' not in sample_object.get('summary'):
                        virtual_phrase = ''
                if len(taxa) > 1:
                    taxa_phrase = 'mixed species '
                else:
                    taxa_phrase = f'{list(taxa)[0]} '
                samples_phrase = f'{len(samples)} {virtual_phrase}{taxa_phrase}samples'
            else:  # list out the samples explicitly, take unique set of sample summaries
                sample_term_phrases = set()
                for sample in samples:
                    sample_object = request.embed(sample, '@@object')
                    sample_term_phrases.add(sample_object.get('summary', ''))
                samples_phrase = f'{", ".join([t for t in sorted(sample_term_phrases) if t!=""])}'

        # Final summary
        return ' '.join(filter(None, [
            file_set_type,
            f'prediction{scope_phrase}',
            f'for {assessed_genes_phrase}' if assessed_genes else '',
            software_version_phrase,
            phenotypes_phrase,
            f'in {samples_phrase}'
        ]))


@collection(
    name='construct-library-sets',
    unique_key='accession',
    properties={
        'title': 'Construct Library Sets',
        'description': 'Listing of construct library sets',
    })
class ConstructLibrarySet(FileSet):
    item_type = 'construct_library_set'
    schema = load_schema('igvfd:schemas/construct_library_set.json')
    embedded_with_frame = [
        Path('award', include=['@id', 'component']),
        Path('lab', include=['@id', 'title']),
        Path('submitted_by', include=['@id', 'title']),
        Path(
            'files',
            include=EMBEDDED_FILE_FIELDS
        ),
        Path('integrated_content_files', include=['@id', 'accession',
             'aliases', 'content_type', 'file_format', 'upload_status', 'status']),
        Path('control_for', include=['@id', 'accession', 'aliases', 'status']),
        Path('associated_phenotypes', include=['@id', 'term_id', 'term_name', 'status']),
        Path('small_scale_gene_list', include=['@id', 'geneid', 'symbol', 'name', 'synonyms', 'allele', 'status']),
        Path('samples', include=['@id', '@type', 'accession',
             'aliases', 'classifications', 'phenotypic_features', 'donors', 'sample_terms', 'targeted_sample_term', 'status', 'summary', 'modifications', 'treatments', 'construct_delivery_methods']),
        Path('donors', include=['@id', 'accession', 'taxa', 'aliases', 'sex', 'summary', 'status']),
        Path('samples.phenotypic_features', include=['@id', 'feature', 'status', 'summary']),
        Path('samples.phenotypic_features.feature', include=['@id', 'term_name', 'status']),
        Path('samples.sample_terms', include=['@id', 'term_name', 'status']),
        Path('samples.targeted_sample_term', include=['@id', 'term_name', 'status']),
        Path('samples.modifications', include=['@id', 'modality', 'summary', 'status']),
        Path('samples.treatments', include=['@id', 'treatment_term_name', 'summary', 'status']),
        Path('large_scale_gene_list', include=['@id', 'accession', 'aliases', 'status']),
        Path('large_scale_loci_list', include=['@id', 'accession', 'aliases', 'status']),
        Path('orf_list', include=['@id', 'orf_id', 'genes', 'aliases', 'status']),
        Path('orf_list.genes', include=['@id', 'symbol', 'status']),
        Path('publications', include=['@id', 'publication_identifiers', 'status']),
    ]
    audit_inherit = [
        'award',
        'lab',
        'files',
        'documents',
        'integrated_content_files'
    ]

    rev = FileSet.rev | {'samples': ('Sample', 'construct_library_sets')}

    set_status_up = [x for x in FileSet.set_status_up if x != 'samples'] + ['integrated_content_files']
    set_status_down = FileSet.set_status_down + []

    @calculated_property(schema={
        'title': 'Samples',
        'description': 'The samples this construct library set was applied to.',
        'type': 'array',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Sample',
            'type': 'string',
            'linkFrom': 'Sample.construct_library_sets',
        },
        'notSubmittable': True
    })
    def samples(self, request, samples):
        return paths_filtered_by_status(request, samples)

    @calculated_property(
        define=True,
        schema={
            'title': 'File Sets',
            'description': 'The file sets that used this construct library set.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'File Set',
                'type': 'string',
                'linkTo': 'FileSet'
            },
            'notSubmittable': True
        })
    def file_sets(self, request, samples=None):
        if samples is None:
            samples = []
        linked_file_sets = set()
        for sample in samples:
            sample_object = request.embed(sample, '@@object_with_select_calculated_properties?field=file_sets')
            for file_set in sample_object.get('file_sets', []):
                linked_file_sets.add(file_set)
        return sorted(linked_file_sets)

    @calculated_property(
        condition='file_sets',
        define=True,
        schema={
            'title': 'Preferred Assay Titles',
            'description': 'The preferred assay titles of the file sets that used this construct library set.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Preferred Assay Title',
                'type': 'string'
            },
            'notSubmittable': True
        })
    def preferred_assay_titles(self, request, file_sets=None):
        if file_sets is None:
            file_sets = []
        preferred_assay_titles = set()
        for file_set in file_sets:
            if file_set.startswith('/measurement-sets/'):
                preferred_assays = request.embed(
                    file_set, '@@object?skip_calculated=true').get('preferred_assay_titles', [])
                if preferred_assays:
                    preferred_assay_titles.update(preferred_assays)
        return sorted(preferred_assay_titles)

    @calculated_property(
        condition='file_sets',
        define=True,
        schema={
            'title': 'Assay Term Names',
            'description': 'Ontology term names from Ontology of Biomedical Investigations (OBI) for assays.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Assay Term Names',
                'type': 'string'
            },
            'notSubmittable': True
        })
    def assay_titles(self, request, file_sets=None):
        if file_sets is None:
            file_sets = []
        assay_titles = set()
        for file_set in file_sets:
            if file_set.startswith('/measurement-sets/'):
                assays = request.embed(
                    file_set, '@@object_with_select_calculated_properties?field=assay_titles').get('assay_titles', [])
                if assays:
                    assay_titles.update(assays)
        return sorted(assay_titles) or None

    @calculated_property(
        condition='file_sets',
        define=True,
        schema={
            'title': 'Assay Slims',
            'description': 'A broad categorization of the assay term.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'type': 'string'
            },
            'notSubmittable': True
        })
    def assay_slims(self, request, file_sets=None):
        if file_sets is None:
            file_sets = []
        assay_types = set()
        for file_set in file_sets:
            if file_set.startswith('/measurement-sets/'):
                assays = request.embed(
                    file_set, '@@object_with_select_calculated_properties?field=assay_slims').get('assay_slims', [])
                if assays:
                    assay_types.update(assays)
        return sorted(assay_types) or None

    @calculated_property(
        condition='samples',
        schema={
            'title': 'Donors',
            'description': 'The donors of the samples associated with this auxiliary set.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Donor',
                'description': 'Donor of a sample associated with this auxiliary set.',
                'type': 'string',
                'linkTo': 'Donor'
            },
            'notSubmittable': True,
        }
    )
    def donors(self, request, samples=None):
        return get_donors_from_samples(request, samples)

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, request, file_set_type, scope, selection_criteria, small_scale_gene_list=None, large_scale_gene_list=None, guide_type=None,
                small_scale_loci_list=None, large_scale_loci_list=None, exon=None, tile=None, orf_list=None, associated_phenotypes=None,
                control_types=None, targeton=None, preferred_assay_titles=None, integrated_content_files=None):
        if preferred_assay_titles is None:
            preferred_assay_titles = []
        if integrated_content_files is None:
            integrated_content_files = []
        library_type = file_set_type
        target_phrase = ''
        pheno_terms = []
        pheno_phrase = ''
        preposition = ''
        pool_phrase = ''
        criteria = []
        criteria = criteria + selection_criteria

        if library_type == 'guide library':
            if guide_type == 'sgRNA':
                library_type = 'guide (sgRNA) library'
            if guide_type == 'pgRNA':
                library_type = 'guide (pgRNA) library'

        if scope == 'control':
            return f'{", ".join(sorted(control_types))} {library_type}'
        if scope == 'loci':
            if small_scale_loci_list and len(small_scale_loci_list) > 1:
                target_phrase = f' {len(small_scale_loci_list)} genomic loci'
            elif large_scale_loci_list:
                target_phrase = f' many genomic loci'
            else:
                # small scale loci list is only displayed if there is 1 and it has a name
                locus_name = ''
                if small_scale_loci_list and len(small_scale_loci_list) == 1:
                    locus = small_scale_loci_list[0]
                    locus_name = locus.get('name', '')
                if locus_name:
                    target_phrase = f' {locus_name}'
                else:
                    target_phrase = f' a genomic locus'
        if scope == 'genes':
            if small_scale_gene_list and len(small_scale_gene_list) > 1:
                target_phrase = f' {len(small_scale_gene_list)} genes'
            elif small_scale_gene_list and len(small_scale_gene_list) == 1:
                gene_object = request.embed(small_scale_gene_list[0], '@@object?skip_calculated=true')
                gene_name = (gene_object.get('symbol'))
                target_phrase = f' {gene_name}'
            elif large_scale_gene_list:
                target_phrase = f' many genes'
        if scope == 'exon':
            if small_scale_gene_list and len(small_scale_gene_list) > 1:
                target_phrase = f' exon {exon} of multiple genes'
            elif small_scale_gene_list and len(small_scale_gene_list) == 1:
                gene_object = request.embed(small_scale_gene_list[0], '@@object?skip_calculated=true')
                gene_name = (gene_object.get('symbol'))
                target_phrase = f' exon {exon} of {gene_name}'
        if scope == 'interactors':
            if orf_list and len(orf_list) > 1:
                target_phrase = f' {len(orf_list)} open reading frames'
            elif small_scale_gene_list and len(small_scale_gene_list) == 1:
                gene_object = request.embed(small_scale_gene_list[0], '@@object?skip_calculated=true')
                orf_object = request.embed(orf_list[0], '@@object?skip_calculated=true')
                gene_name = (gene_object.get('symbol'))
                orf_id = (orf_object.get('orf_id'))
                target_phrase = f' open reading frame {orf_id} of {gene_name}'
        if scope == 'tile':
            tile_id = tile['tile_id']
            start = tile['tile_start']
            end = tile['tile_end']
            if small_scale_gene_list and len(small_scale_gene_list) > 1:
                target_phrase = f' tile {tile_id} of multiple genes'
            elif small_scale_gene_list and len(small_scale_gene_list) == 1:
                gene_object = request.embed(small_scale_gene_list[0], '@@object?skip_calculated=true')
                gene_name = gene_object.get('symbol', '')
                gene_allele = gene_object.get('allele', '')
                allele_suffix = f' {gene_allele} allele' if gene_allele else ''
                target_phrase = f' tile {tile_id} of {gene_name}{allele_suffix} (AA {start}-{end})'
        if scope == 'genome-wide':
            target_phrase = ' genome-wide'
        if scope == 'targeton':
            gene_object = request.embed(small_scale_gene_list[0], '@@object?skip_calculated=true')
            gene_name = gene_object.get('symbol', '')
            target_phrase = f' {targeton} of {gene_name}'

        if associated_phenotypes:
            for pheno in associated_phenotypes:
                pheno_object = request.embed(pheno, '@@object?skip_calculated=true')
                term_name = (pheno_object.get('term_name'))
                pheno_terms.append(term_name)
            if len(pheno_terms) in [1, 2]:
                phenos = ' and '.join(pheno_terms)
                pheno_phrase = f' associated with {phenos}'
            else:
                pheno_phrase = f' associated with {len(pheno_terms)} phenotypes'

        if preferred_assay_titles and 'STARR-seq' in preferred_assay_titles:
            thousand_genomes_ids = set()
            for integrated_content_file in integrated_content_files:
                integrated_content_file_object = request.embed(integrated_content_file, '@@object?skip_calculated=true')
                file_set_object = request.embed(
                    integrated_content_file_object['file_set'], '@@object_with_select_calculated_properties?field=donors')
                donors = file_set_object.get('donors', [])
                for donor in donors:
                    donor_object = request.embed(donor, '@@object?skip_calculated=true')
                    dbxrefs = donor_object.get('dbxrefs', [])
                    for dbxref in dbxrefs:
                        if dbxref.startswith('IGSR'):
                            thousand_genomes_id = dbxref.split(':')[1]
                            thousand_genomes_ids.add(thousand_genomes_id)
            if thousand_genomes_ids:
                thousand_genomes_ids = ', '.join(sorted(thousand_genomes_ids))
                pool_phrase = f' pooled from 1000 Genomes donors: {thousand_genomes_ids}'

        if file_set_type in ['expression vector library', 'overexpression vector library']:
            if 'genes' in criteria:
                criteria.remove('genes')
            selections = ', '.join(criteria)
            if selections:
                selections = f' ({selections})'
            preposition = ' of'
            return f'{library_type}{preposition}{target_phrase}{selections}{pheno_phrase}'
        else:
            selections = ', '.join(criteria)
            if scope == 'genome-wide':
                preposition = ''
            else:
                preposition = ' in'
            return f'{library_type} targeting {selections}{preposition}{target_phrase}{pheno_phrase}{pool_phrase}'


@collection(
    name='pseudobulk-sets',
    unique_key='accession',
    properties={
        'title': 'Pseudobulk Sets',
        'description': 'Listing of pseudobulk sets',
    }
)
class PseudobulkSet(FileSet):
    item_type = 'pseudobulk_set'
    schema = load_schema('igvfd:schemas/pseudobulk_set.json')
    embedded_with_frame = FileSet.embedded_with_frame + [
        Path('input_file_sets', include=['@id', 'accession', 'aliases', 'file_set_type', 'status']),
        Path('workflows', include=['@id', 'accession', 'name', 'uniform_pipeline', 'status', 'workflow_version']),
        Path('cell_type', include=['@id', 'term_name', 'term_id', 'status', 'definition']),
        Path(
            'samples.sample_terms',
            include=[
                '@id',
                '@type',
                'accession',
                'aliases',
                'treatments',
                'cellular_sub_pool',
                'classifications',
                'phenotypic_features',
                'growth_medium',
                'modifications',
                'sample_terms',
                'status',
                'summary',
                'targeted_sample_term',
                'taxa',
                'term_name',
                'treatments',
                'institutional_certificates',
            ]
        ),
        Path('samples.phenotypic_features', include=['@id', 'feature', 'status', 'summary']),
        Path('samples.phenotypic_features.feature', include=['@id', 'term_name', 'status']),
        Path('samples.targeted_sample_term', include=['@id', 'term_name', 'status']),
        Path('samples.modifications', include=['@id', 'modality', 'status']),
        Path('samples.treatments', include=['@id', 'treatment_term_name',
             'purpose', 'treatment_type', 'summary', 'status']),
    ]
    audit_inherit = FileSet.audit_inherit
    set_status_up = FileSet.set_status_up + []
    set_status_down = FileSet.set_status_down + []

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, request, cell_type, samples, cell_qualifier=None):
        source_biosample_classifications = set()
        source_biosample_terms = set()
        cell_qualifier_string = ''
        if cell_qualifier:
            cell_qualifier_string = cell_qualifier
        cell_type_object = request.embed(cell_type, '@@object')
        for sample in samples:
            sample_object = request.embed(sample, '@@object')
            sample_term_object = request.embed(sample_object['sample_terms'][0], '@@object')
            classifications = sample_object.get('classifications', [])
            for classification in classifications:
                source_biosample_classifications.add(classification)
            source_biosample_terms.add(sample_term_object.get('term_name', ''))
        summary_phrase = (
            f'{cell_qualifier_string} {cell_type_object.get("term_name", "")} '
            f'derived from {", ".join(source_biosample_terms)}'
        ).strip()
        return f'Pseudobulk of {summary_phrase}'

    @calculated_property(
        schema={
            'title': 'Workflows',
            'description': 'A workflow for computational analysis of genomic data. A workflow is made up of analysis steps.',
            'type': 'array',
            'notSubmittable': True,
            'uniqueItem': True,
            'minItems': 1,
            'items': {
                'title': 'Workflow',
                'type': 'string',
                'linkTo': 'Workflow'
            }
        }
    )
    def workflows(self, request, files=None):
        if files is None:
            files = []
        unique_workflows = set()
        for file_ in files:
            file_workflows = request.embed(
                file_,
                '@@object_with_select_calculated_properties?field=workflows',
            ).get('workflows', [])
            unique_workflows.update(file_workflows)
        return sorted(unique_workflows)

    @calculated_property(
        define=True,
        schema={
            'title': 'Preferred Assay Titles',
            'description': 'Preferred Assay Title(s) of assays that produced data analyzed in the pseudobulk set.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Preferred Assay Titles',
                'description': 'Title of assay that produced data analyzed in the pseudobulk set.',
                'type': 'string'
            },
            'notSubmittable': True,
        }
    )
    def preferred_assay_titles(self, request, input_file_sets=None):
        if input_file_sets is None:
            input_file_sets = []
        preferred_assay_list = set()
        for fileset in input_file_sets:
            file_set_object = request.embed(
                fileset,
                '@@object_with_select_calculated_properties?field=preferred_assay_titles'
            )
            preferred_assay_list.update(
                file_set_object.get(
                    'preferred_assay_titles',
                    []
                )
            )
        return sorted(preferred_assay_list)

    @calculated_property(
        define=True,
        schema={
            'title': 'Assay Term Names',
            'description': 'Ontology term names from Ontology of Biomedical Investigations (OBI) for assays.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Assay Term Names',
                'description': 'Title of assay that produced data analyzed in the pseudobulk set.',
                'type': 'string'
            },
            'notSubmittable': True,
        }
    )
    def assay_titles(self, request, input_file_sets=None):
        if input_file_sets is None:
            input_file_sets = []
        assay_list = set()
        for fileset in input_file_sets:
            file_set_object = request.embed(
                fileset,
                '@@object_with_select_calculated_properties?field=assay_titles'
            )
            assay_list.update(
                file_set_object.get(
                    'assay_titles',
                    []
                )
            )
        return sorted(assay_list) or None

    @calculated_property(
        define=True,
        schema={
            'title': 'Assay Slims',
            'description': 'A broad categorization of the assay term.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'type': 'string'
            },
            'notSubmittable': True,
        }
    )
    def assay_slims(self, request, input_file_sets=None):
        if input_file_sets is None:
            input_file_sets = []
        assay_types = set()
        for fileset in input_file_sets:
            file_set_object = request.embed(
                fileset,
                '@@object_with_select_calculated_properties?field=assay_slims'
            )
            assay_types.update(
                file_set_object.get(
                    'assay_slims',
                    []
                )
            )
        return sorted(assay_types) or None
