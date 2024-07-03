import pytest

from pyramid.exceptions import HTTPBadRequest


def experiment():
    return {
        'assay_term_name': 'ChIP-seq',
        'biosample_ontology': '/biosample-types/cell_line_EFO_0002067/',
        'documents': [
            '/documents/efac5344-6834-4e12-b971-94994d992e86/',
            '/documents/d00ffce2-e72c-44d7-a71f-73fd163c2426/',
            '/documents/73c95206-fc02-41ea-93e0-a929a6939aaf/'
        ],
        'references': [],
        'schema_version': '30',
        'accession': 'ENCSR153HNT',
        'alternate_accessions': [],
        'description': 'ChIP-Seq on K562',
        'dbxrefs': [],
        'date_released': '2020-07-15',
        'internal_tags': [],
        'status': 'released',
        'date_created': '2020-03-26T19:57:31.454124+00:00',
        'submitted_by': '/users/5e189705-c6ca-4849-ab5c-e6d679dc96ae/',
        'lab': '/labs/richard-myers/',
        'award': '/awards/UM1HG009411/',
        'aliases': ['richard-myers:SL414442-SL414443'],
        'date_submitted': '2020-04-17',
        'target': '/targets/STAG1-human/',
        'possible_controls': [
            '/experiments/ENCSR516XLO/'
        ],
        'supersedes': [],
        'related_files': [],
        'internal_status': 'release ready',
        'analyses': [
            '/analyses/ENCAN823NHJ/'
        ],
        'replication_type': 'isogenic',
        'objective_slims': [],
        'type_slims': [],
        'category_slims': [],
        'assay_title': 'TF ChIP-seq',
        'assay_slims': [
            'DNA binding'
        ],
        'replicates': [
            '/replicates/3b653ab4-7773-45b1-90f6-003aa9d0881f/',
            '/replicates/3210b1a4-a0c0-44c2-b3e4-796b0cfb8fcb/'
        ],
        'biosample_summary': 'K562 genetically modified using CRISPR',
        'assay_term_id': 'OBI:0000716',
        '@id': '/experiments/ENCSR153HNT/',
        '@type': [
            'Experiment',
            'Dataset',
            'Item'
        ],
        'uuid': 'd5167d89-b29f-4d83-900d-d7276ec3adec',
        'original_files': [
            '/files/ENCFF901WEB/',
            '/files/ENCFF766UOD/',
            '/files/ENCFF304IDX/',
            '/files/ENCFF881NAX/'
        ],
        'contributing_files': [
            '/files/ENCFF089RYQ/',
            '/files/ENCFF356LFX/',
            '/files/ENCFF110MCL/'
        ],
        'files': [
            '/files/ENCFF901WEB/',
            '/files/ENCFF766UOD/',
            '/files/ENCFF304IDX/',
            '/files/ENCFF895UWM/',
            '/files/ENCFF744MWW/'
        ],
        'revoked_files': [],
        'assembly': [
            'GRCh38'
        ],
        'hub': '/experiments/ENCSR153HNT/@@hub/hub.txt',
        'related_series': [],
        'superseded_by': [],
        'protein_tags': [
            {'location': 'C-terminal', 'name': '3xFLAG', 'target': '/targets/STAG1-human/'},
            {'location': 'C-terminal', 'name': '3xFLAG', 'target': '/targets/STAG2-human/'}
        ],
        'perturbed': False
    }


def embedded_experiment():
    return {
        '@id': '/experiments/ENCSR434TGY/',
        '@type': ['Experiment', 'Dataset', 'Item'],
        'accession': 'ENCSR434TGY',
        'assay_title': 'DNase-seq',
        'award': {'project': 'ENCODE'},
        'biosample_ontology': {
            'term_name': 'ZHBTc4',
            'term_id': 'EFO:0005914',
            'classification': 'cell line'
        },
        'date_released': '2020-07-28',
        'files': [
            {
                'dbxrefs': [],
                'file_format_type': 'bed3+',
                'output_type': 'DHS peaks',
                'technical_replicates': ['1_1'],
                'lab': {'title': 'John Stamatoyannopoulos, UW'},
                'title': 'ENCFF237ENG',
                'file_size': 642625,
                's3_uri': 's3://encode-public/2020/07/28/d24b3680-9453-403e-94b8-2393ed02ccb6/ENCFF237ENG.bed.gz',
                'md5sum': 'c954093c70a9c0f2067dc480a5135936',
                'file_type': 'bed bed3+',
                'no_file_available': False,
                'assembly': 'mm10',
                'biological_replicates': [1],
                'href': '/files/ENCFF237ENG/@@download/ENCFF237ENG.bed.gz',
                'read_length': 36,
                'file_format': 'bed',
                'status': 'released'
            },
            {
                'dbxrefs': [],
                'output_type': 'reads',
                'run_type': 'single-ended',
                'technical_replicates': ['1_1'],
                'lab': {
                    'title': 'John Stamatoyannopoulos, UW'
                },
                'title': 'ENCFF001QIF',
                'platform': {
                    'title': 'Illumina HiSeq 2000'
                },
                'file_size': 237982153,
                's3_uri': 's3://encode-public/2011/05/06/7c35d915-aea2-4f20-9f52-b2af18991cab/ENCFF001QIF.fastq.gz',
                'md5sum': 'cfb4e7dd7dbb0add6efbe0e52ae5618a',
                'file_type': 'fastq',
                'no_file_available': False,
                'biological_replicates': [1],
                'href': '/files/ENCFF001QIF/@@download/ENCFF001QIF.fastq.gz',
                'read_length': 36,
                'file_format': 'fastq',
                'status': 'released'
            },
            {
                'dbxrefs': [],
                'output_type': 'reads',
                'run_type': 'single-ended',
                'technical_replicates': ['1_1'],
                'lab': {
                    'title': 'John Stamatoyannopoulos, UW'
                },
                'title': 'ENCFF001QIE',
                'platform': {
                    'title': 'Illumina Genome Analyzer'
                },
                'file_size': 1338237475,
                's3_uri': 's3://encode-public/2011/05/06/11f63cfc-6da6-4f23-a9a0-1b1b04744dbd/ENCFF001QIE.fastq.gz',
                'md5sum': '315ebbab452358fe188024e3637fd965',
                'file_type': 'fastq',
                'no_file_available': False,
                'biological_replicates': [1],
                'href': '/files/ENCFF001QIE/@@download/ENCFF001QIE.fastq.gz',
                'read_length': 36,
                'file_format': 'fastq',
                'status': 'released'}
        ],
        'replicates': [
            {
                'library': {
                    'nucleic_acid_term_name': 'DNA',
                    'biosample': {
                        'organism': {
                            'scientific_name': 'Mus musculus'
                        },
                        'treatments': [
                            {
                                'duration': 96,
                                'treatment_term_name': 'doxycycline hyclate',
                                'amount': 100,
                                'duration_units': 'hour',
                                'amount_units': 'ng/mL'
                            }
                        ]
                    }
                }
            }
        ]
    }


def file_():
    return {
        'dbxrefs': [],
        'file_format_type': 'idr_ranked_peak',
        'output_type': 'IDR ranked peaks',
        'technical_replicates': ['2_1'],
        'lab': {
            'title': 'ENCODE Processing Pipeline'
        },
        'title': 'ENCFF244PJU',
        'file_size': 3356650,
        's3_uri': 's3://encode-public/2020/07/09/dc068c0a-d1c8-461a-a208-418d35121f3b/ENCFF244PJU.bed.gz',
        'md5sum': '335b6066a184f30f225aec79b376c7e8',
        'file_type': 'bed idr_ranked_peak',
        'no_file_available': False,
        'derived_from': [
            '/files/ENCFF895UWM/',
            '/files/ENCFF089RYQ/'
        ],
        'assembly': 'GRCh38',
        'biological_replicates': [
            2
        ],
        'href': '/files/ENCFF244PJU/@@download/ENCFF244PJU.bed.gz',
        'file_format': 'bed',
        'status': 'released',
        'replicate': {
            'rbns_protein_concentration': 20,
            'rbns_protein_concentration_units': 'nM'
        },
        'preferred_default': True
    }


def abstract_file():
    return {
        'nested': {
            'boolean': True,
            'list': ['a', 'b', 'c'],
            'int': 2,
            'str': 'xyz',
            'empty_list': []
        },
        'empty_list': []
    }


def audits_():
    return {
        'WARNING': [
            {
                'category': 'inconsistent control read length',
                'detail': 'File {ENCFF783ZRQ|/files/ENCFF783ZRQ/} is 36 but its control file {ENCFF454ZHO|/files/ENCFF454ZHO/} is 30.',
                'level': 40,
                'level_name': 'WARNING',
                'path': '/files/ENCFF783ZRQ/',
                'name': 'audit_file'
            },
            {
                'category': 'inconsistent platforms',
                'detail': 'possible_controls is a list of experiment(s) that can serve as analytical controls for a given experiment. Experiment {ENCSR814EAU|/experiments/ENCSR814EAU/} found in possible_controls list of this experiment contains data produced on platform Illumina Genome Analyzer II/e/x which is not compatible with platform Illumina HiSeq 2000/2500 used in this experiment.',
                'level': 40,
                'level_name': 'WARNING',
                'path': '/experiments/ENCSR891KGZ/',
                'name': 'audit_experiment'
            }, {
                'category': 'low read length',
                'detail': 'Fastq file {ENCFF557LZC|/files/ENCFF557LZC/} has read length of 36bp. For mapping accuracy ENCODE standards recommend that sequencing reads should be at least 50bp long. (See {ENCODE ChIP-seq data standards|/data-standards/chip-seq/} )',
                'level': 40,
                'level_name': 'WARNING',
                'path': '/experiments/ENCSR891KGZ/',
                'name': 'audit_experiment'
            },
            {
                'category': 'low read length',
                'detail': 'Fastq file {ENCFF783ZRQ|/files/ENCFF783ZRQ/} has read length of 36bp. For mapping accuracy ENCODE standards recommend that sequencing reads should be at least 50bp long. (See {ENCODE ChIP-seq data standards|/data-standards/chip-seq/} )',
                'level': 40,
                'level_name': 'WARNING',
                'path': '/experiments/ENCSR891KGZ/',
                'name': 'audit_experiment'
            },
            {
                'category': 'moderate library complexity',
                'detail': 'NRF (Non Redundant Fraction) is equal to the result of the division of the number of reads after duplicates removal by the total number of reads. An NRF value in the range 0 - 0.5 is poor complexity, 0.5 - 0.8 is moderate complexity, and > 0.8 high complexity. NRF value > 0.8 is recommended, but > 0.5 is acceptable.  ENCODE processed alignments file {ENCFF553TUY|/files/ENCFF553TUY/} was generated from a library with NRF value of 0.64.',
                'level': 40,
                'level_name': 'WARNING',
                'path': '/experiments/ENCSR891KGZ/',
                'name': 'audit_experiment'
            },
            {
                'category': 'mild to moderate bottlenecking',
                'detail': 'PBC1 (PCR Bottlenecking Coefficient 1, M1/M_distinct) is the ratio of the number of genomic locations where exactly one read maps uniquely (M1) to the number of genomic locations where some reads map (M_distinct). A PBC1 value in the range 0 - 0.5 is severe bottlenecking, 0.5 - 0.8 is moderate bottlenecking, 0.8 - 0.9 is mild bottlenecking, and > 0.9 is no bottlenecking. PBC1 value > 0.9 is recommended, but > 0.8 is acceptable.  ENCODE processed alignments file {ENCFF553TUY|/files/ENCFF553TUY/} was generated from a library with PBC1 value of 0.73.',
                'level': 40,
                'level_name': 'WARNING',
                'path': '/experiments/ENCSR891KGZ/',
                'name': 'audit_experiment'
            },
            {
                'category': 'mild to moderate bottlenecking',
                'detail': 'PBC2 (PCR Bottlenecking Coefficient 2, M1/M2) is the ratio of the number of genomic locations where exactly one read maps uniquely (M1) to the number of genomic locations where two reads map uniquely (M2). A PBC2 value in the range 0 - 1 is severe bottlenecking, 1 - 3 is moderate bottlenecking, 3 - 10 is mild bottlenecking, > 10 is no bottlenecking. PBC2 value > 10 is recommended, but > 3 is acceptable.  ENCODE processed alignments file {ENCFF553TUY|/files/ENCFF553TUY/} was generated from a library with PBC2 value of 4.26.',
                'level': 40,
                'level_name': 'WARNING',
                'path': '/experiments/ENCSR891KGZ/',
                'name': 'audit_experiment'
            }, {
                'category': 'moderate library complexity',
                'detail': 'NRF (Non Redundant Fraction) is equal to the result of the division of the number of reads after duplicates removal by the total number of reads. An NRF value in the range 0 - 0.5 is poor complexity, 0.5 - 0.8 is moderate complexity, and > 0.8 high complexity. NRF value > 0.8 is recommended, but > 0.5 is acceptable.  ENCODE processed alignments file {ENCFF349SRS|/files/ENCFF349SRS/} was generated from a library with NRF value of 0.64.',
                'level': 40,
                'level_name': 'WARNING',
                'path': '/experiments/ENCSR891KGZ/',
                'name': 'audit_experiment'
            },
            {
                'category': 'mild to moderate bottlenecking',
                'detail': 'PBC1 (PCR Bottlenecking Coefficient 1, M1/M_distinct) is the ratio of the number of genomic locations where exactly one read maps uniquely (M1) to the number of genomic locations where some reads map (M_distinct). A PBC1 value in the range 0 - 0.5 is severe bottlenecking, 0.5 - 0.8 is moderate bottlenecking, 0.8 - 0.9 is mild bottlenecking, and > 0.9 is no bottlenecking. PBC1 value > 0.9 is recommended, but > 0.8 is acceptable.  ENCODE processed alignments file {ENCFF349SRS|/files/ENCFF349SRS/} was generated from a library with PBC1 value of 0.73.',
                'level': 40,
                'level_name': 'WARNING',
                'path': '/experiments/ENCSR891KGZ/',
                'name': 'audit_experiment'
            },
            {
                'category': 'mild to moderate bottlenecking',
                'detail': 'PBC2 (PCR Bottlenecking Coefficient 2, M1/M2) is the ratio of the number of genomic locations where exactly one read maps uniquely (M1) to the number of genomic locations where two reads map uniquely (M2). A PBC2 value in the range 0 - 1 is severe bottlenecking, 1 - 3 is moderate bottlenecking, 3 - 10 is mild bottlenecking, > 10 is no bottlenecking. PBC2 value > 10 is recommended, but > 3 is acceptable.  ENCODE processed alignments file {ENCFF349SRS|/files/ENCFF349SRS/} was generated from a library with PBC2 value of 4.26.',
                'level': 40,
                'level_name': 'WARNING', 'path': '/experiments/ENCSR891KGZ/', 'name': 'audit_experiment'
            },
            {
                'category': 'moderate library complexity', 'detail': 'NRF (Non Redundant Fraction) is equal to the result of the division of the number of reads after duplicates removal by the total number of reads. An NRF value in the range 0 - 0.5 is poor complexity, 0.5 - 0.8 is moderate complexity, and > 0.8 high complexity. NRF value > 0.8 is recommended, but > 0.5 is acceptable.  ENCODE processed alignments file {ENCFF293PPG|/files/ENCFF293PPG/} was generated from a library with NRF value of 0.80.',
                'level': 40,
                'level_name': 'WARNING', 'path': '/experiments/ENCSR891KGZ/',
                'name': 'audit_experiment'
            },
            {
                'category': 'mild to moderate bottlenecking', 'detail': 'PBC1 (PCR Bottlenecking Coefficient 1, M1/M_distinct) is the ratio of the number of genomic locations where exactly one read maps uniquely (M1) to the number of genomic locations where some reads map (M_distinct). A PBC1 value in the range 0 - 0.5 is severe bottlenecking, 0.5 - 0.8 is moderate bottlenecking, 0.8 - 0.9 is mild bottlenecking, and > 0.9 is no bottlenecking. PBC1 value > 0.9 is recommended, but > 0.8 is acceptable.  ENCODE processed alignments file {ENCFF293PPG|/files/ENCFF293PPG/} was generated from a library with PBC1 value of 0.88.',
                'level': 40,
                'level_name': 'WARNING',
                'path': '/experiments/ENCSR891KGZ/',
                'name': 'audit_experiment'
            },
            {
                'category': 'mild to moderate bottlenecking',
                'detail': 'PBC1 (PCR Bottlenecking Coefficient 1, M1/M_distinct) is the ratio of the number of genomic locations where exactly one read maps uniquely (M1) to the number of genomic locations where some reads map (M_distinct). A PBC1 value in the range 0 - 0.5 is severe bottlenecking, 0.5 - 0.8 is moderate bottlenecking, 0.8 - 0.9 is mild bottlenecking, and > 0.9 is no bottlenecking. PBC1 value > 0.9 is recommended, but > 0.8 is acceptable.  ENCODE processed alignments file {ENCFF610NUD|/files/ENCFF610NUD/} was generated from a library with PBC1 value of 0.88.',
                'level': 40,
                'level_name': 'WARNING', 'path': '/experiments/ENCSR891KGZ/',
                'name': 'audit_experiment'
            }
        ],
        'NOT_COMPLIANT': [
            {
                'category': 'insufficient read depth',
                'detail': 'Processed alignments file {ENCFF553TUY|/files/ENCFF553TUY/} produced by ChIP-seq read mapping pipeline ( {ENCPL220NBH|/pipelines/ENCPL220NBH/} ) using the hg19 assembly has 8345584 usable fragments. The minimum ENCODE standard for each replicate in a ChIP-seq experiment targeting H4K8ac-human and investigated as a transcription factor is 10 million usable fragments. The recommended value is > 20 million, but > 10 million is acceptable. (See {ENCODE ChIP-seq data standards|/data-standards/chip-seq/} )',
                'level': 50,
                'level_name': 'NOT_COMPLIANT',
                'path': '/experiments/ENCSR891KGZ/',
                'name': 'audit_experiment'
            },
            {
                'category': 'insufficient read depth',
                'detail': 'Processed alignments file {ENCFF349SRS|/files/ENCFF349SRS/} produced by ChIP-seq read mapping pipeline ( {ENCPL220NBH|/pipelines/ENCPL220NBH/} ) using the GRCh38 assembly has 8338604 usable fragments. The minimum ENCODE standard for each replicate in a ChIP-seq experiment targeting H4K8ac-human and investigated as a transcription factor is 10 million usable fragments. The recommended value is > 20 million, but > 10 million is acceptable. (See {ENCODE ChIP-seq data standards|/data-standards/chip-seq/} )',
                'level': 50,
                'level_name': 'NOT_COMPLIANT',
                'path': '/experiments/ENCSR891KGZ/',
                'name': 'audit_experiment'
            }
        ],
        'ERROR': [
            {
                'category': 'extremely low read depth',
                'detail': 'Processed alignments file {ENCFF293PPG|/files/ENCFF293PPG/} produced by ChIP-seq read mapping pipeline ( {ENCPL220NBH|/pipelines/ENCPL220NBH/} ) using the GRCh38 assembly has 1372444 usable fragments. The minimum ENCODE standard for each replicate in a ChIP-seq experiment targeting H4K8ac-human and investigated as a transcription factor is 10 million usable fragments. The recommended value is > 20 million, but > 10 million is acceptable. (See {ENCODE ChIP-seq data standards|/data-standards/chip-seq/} )',
                'level': 60,
                'level_name': 'ERROR',
                'path': '/experiments/ENCSR891KGZ/',
                'name': 'audit_experiment'
            },
            {
                'category': 'extremely low read depth',
                'detail': 'Processed alignments file {ENCFF610NUD|/files/ENCFF610NUD/} produced by ChIP-seq read mapping pipeline ( {ENCPL220NBH|/pipelines/ENCPL220NBH/} ) using the hg19 assembly has 1374194 usable fragments. The minimum ENCODE standard for each replicate in a ChIP-seq experiment targeting H4K8ac-human and investigated as a transcription factor is 10 million usable fragments. The recommended value is > 20 million, but > 10 million is acceptable. (See {ENCODE ChIP-seq data standards|/data-standards/chip-seq/} )',
                'level': 60,
                'level_name': 'ERROR',
                'path': '/experiments/ENCSR891KGZ/',
                'name': 'audit_experiment'
            }
        ]
    }


def test_metadata_file_matches_file_params():
    from igvfd.metadata.metadata import file_matches_file_params
    file_param_list = {}
    assert file_matches_file_params(file_(), file_param_list)
    file_param_list = {'assembly': set(['GRCh38'])}
    assert file_matches_file_params(file_(), file_param_list)
    file_param_list = {'assembly': set(['hg19'])}
    assert not file_matches_file_params(file_(), file_param_list)
    file_param_list = {'no_such_thing': set(['abc'])}
    assert not file_matches_file_params(file_(), file_param_list)
    file_param_list = {'missing_field': set(['missing_value'])}
    assert not file_matches_file_params(file_(), file_param_list)
    file_param_list = {'derived_from': set(['/files/ENCFF089RYQ/'])}
    assert file_matches_file_params(file_(), file_param_list)
    file_param_list = {'derived_from': set(['/files/ENCFF089RYQ/', '/files/ENCFFABC123/'])}
    assert file_matches_file_params(file_(), file_param_list)
    file_param_list = {'derived_from': set(['/files/ENCFF895UWM/', '/files/ENCFF089RYQ/'])}
    assert file_matches_file_params(file_(), file_param_list)
    file_param_list = {'technical_replicates': set(['2_1'])}
    assert file_matches_file_params(file_(), file_param_list)
    file_param_list = {'biological_replicates': set([2])}
    assert file_matches_file_params(file_(), file_param_list)
    file_param_list = {'file_size': set([3356650])}
    assert file_matches_file_params(file_(), file_param_list)
    file_param_list = {'replicate.rbns_protein_concentration': set([20])}
    assert file_matches_file_params(file_(), file_param_list)
    file_param_list = {'replicate.rbns_protein_concentration_units': set(['nM'])}
    assert file_matches_file_params(file_(), file_param_list)
    file_param_list = {'preferred_default': set([True])}
    assert file_matches_file_params(file_(), file_param_list)
    file_param_list = {'no_file_available': set([False])}
    assert file_matches_file_params(file_(), file_param_list)
    file_param_list = {'restricted': set([True])}
    assert not file_matches_file_params(file_(), file_param_list)
    file_param_list = {'assembly': set(['*'])}
    assert file_matches_file_params(file_(), file_param_list)
    file_param_list = {'no_such_thing': set(['*'])}
    assert not file_matches_file_params(file_(), file_param_list)
    file_param_list = {'preferred_default': set(['*'])}
    assert file_matches_file_params(file_(), file_param_list)
    file_param_list = {
        'derived_from': set(['*'])
    }
    assert file_matches_file_params(file_(), file_param_list)
    file_param_list = {
        'derived_from': set(['*']),
        'title': set(['ENCFF244PJU'])
    }
    assert file_matches_file_params(file_(), file_param_list)
    file_param_list = {
        'derived_from': set(['/files/ENCFF895UWM/', '/files/ENCFF089RYQ/']),
        'title': set(['ENCFF244PJU'])
    }
    assert file_matches_file_params(file_(), file_param_list)
    file_param_list = {
        'preferred_default': set(['*']),
        'assembly': set(['GRCh38']),
        'replicate.rbns_protein_concentration': set([20]),
        'derived_from': set(['/files/ENCFF895UWM/', '/files/ENCFF089RYQ/']),
        'file_size': set([3356650]),
        'no_file_available': set([False])
    }
    assert file_matches_file_params(file_(), file_param_list)
    file_param_list = {
        'preferred_default': set(['*']),
        'assembly': set(['GRCh38']),
        'replicate.rbns_protein_concentration': set([20]),
        'derived_from': set(['/files/ENCFF895UWM/', '/files/ENCFF089RYQ/']),
        'file_size': set([3356650]),
        'no_file_available': set([False]),
        'restricted': set([True])
    }
    assert not file_matches_file_params(file_(), file_param_list)
    file_param_list = {'nested.empty_list': set(['*'])}
    assert not file_matches_file_params(abstract_file(), file_param_list)
    file_param_list = {'nested.empty_list': set([])}
    assert not file_matches_file_params(abstract_file(), file_param_list)
    file_param_list = {'nested.list': set(['a'])}
    assert file_matches_file_params(abstract_file(), file_param_list)
    file_param_list = {'nested.list': set(['a', 'b'])}
    assert file_matches_file_params(abstract_file(), file_param_list)
    file_param_list = {'empty_list': set([])}
    assert not file_matches_file_params(abstract_file(), file_param_list)
    file_param_list = {'nested.str': set(['xyz'])}
    assert file_matches_file_params(abstract_file(), file_param_list)
    file_param_list = {'nested.str': set(['zxyz'])}
    assert not file_matches_file_params(abstract_file(), file_param_list)
    file_param_list = {'nested.int': set([2])}
    assert file_matches_file_params(abstract_file(), file_param_list)
    file_param_list = {'nested.int': set([2, 3])}
    assert file_matches_file_params(abstract_file(), file_param_list)
    file_param_list = {'nested.int': set([3])}
    assert not file_matches_file_params(abstract_file(), file_param_list)
    file_param_list = {'nested.boolean': set([True])}
    assert file_matches_file_params(abstract_file(), file_param_list)
    file_param_list = {'nested.boolean': set([True, False])}
    assert file_matches_file_params(abstract_file(), file_param_list)
    file_param_list = {'nested.boolean': set([False])}
    assert not file_matches_file_params(abstract_file(), file_param_list)


def test_metadata_some_value_satisfies_inequalities():
    from igvfd.metadata.metadata import some_value_satisfies_inequalities
    from igvfd.metadata.inequalities import map_param_values_to_inequalities
    inequalities = map_param_values_to_inequalities(
        [
            'gt:1',
            'lte:2',
            'lt:3000',
        ]
    )
    assert some_value_satisfies_inequalities([2], inequalities)
    assert not some_value_satisfies_inequalities([1], inequalities)
    assert not some_value_satisfies_inequalities([0, 1, -2], inequalities)
    assert some_value_satisfies_inequalities([0, 1, -2, 2], inequalities)
    inequalities = map_param_values_to_inequalities(
        [
            'lte:ENCSR000AAB',
        ]
    )
    assert some_value_satisfies_inequalities(['ENCSR000AAA'], inequalities)
    assert not some_value_satisfies_inequalities(['ENCSR000AAC'], inequalities)
    assert not some_value_satisfies_inequalities(['ENCSR000AAC', 'ENCSR000ZZZ'], inequalities)
    assert some_value_satisfies_inequalities(['ENCSR000AAC', 'ENCSR000ZZZ', 'ENCSR000AAA'], inequalities)
    assert not some_value_satisfies_inequalities([6000, 3000], inequalities)
    inequalities = map_param_values_to_inequalities(
        [
            'gte:97.32',
        ]
    )
    assert some_value_satisfies_inequalities(['97.32'], inequalities)
    assert not some_value_satisfies_inequalities(['96.32'], inequalities)
    assert not some_value_satisfies_inequalities([0], inequalities)


def test_metadata_file_satisfies_inequality_constraints():
    from igvfd.metadata.metadata import file_satisfies_inequality_constraints
    from igvfd.metadata.inequalities import map_param_values_to_inequalities
    positive_file_inequalities = {
        'file_size':  map_param_values_to_inequalities(['gt:500'])
    }
    assert file_satisfies_inequality_constraints(file_(), positive_file_inequalities)
    positive_file_inequalities = {
        'file_size':  map_param_values_to_inequalities(['gt:500', 'gte:3356650', 'lt: 8356650'])
    }
    assert file_satisfies_inequality_constraints(file_(), positive_file_inequalities)
    positive_file_inequalities = {
        'file_size':  map_param_values_to_inequalities(['gt:500', 'gte:3356650', 'lt: 8356650']),
        'missing_field':  map_param_values_to_inequalities(['gt:500']),
    }
    assert not file_satisfies_inequality_constraints(file_(), positive_file_inequalities)
    positive_file_inequalities = {
        'missing_field':  map_param_values_to_inequalities(['gt:500']),
    }
    assert not file_satisfies_inequality_constraints(file_(), positive_file_inequalities)
    positive_file_inequalities = {
        'file_size':  map_param_values_to_inequalities(['gte:50000']),
        'title':  map_param_values_to_inequalities(['lte:ENCFF244PJU', 'lte:ENCFF300PJU']),
        'biological_replicates': map_param_values_to_inequalities(['gt:1']),
        'replicate.rbns_protein_concentration': map_param_values_to_inequalities(['gt:10', 'lt:30']),
    }
    assert file_satisfies_inequality_constraints(file_(), positive_file_inequalities)
    positive_file_inequalities = {
        'file_size':  map_param_values_to_inequalities(['gte:50000']),
        'title':  map_param_values_to_inequalities(['lte:ENCFF244PJU', 'lte:ENCFF300PJU']),
        'biological_replicates': map_param_values_to_inequalities(['gt:1']),
        'replicate.rbns_protein_concentration': map_param_values_to_inequalities(['gt:10', 'lt:15']),
    }
    assert not file_satisfies_inequality_constraints(file_(), positive_file_inequalities)


def test_metadata_group_audits_by_files_and_type():
    from igvfd.metadata.metadata import group_audits_by_files_and_type
    grouped_file_audits, grouped_other_audits = group_audits_by_files_and_type(audits_())
    expected_grouped_file_audits = {
        '/files/ENCFF783ZRQ/': {
            'WARNING': (
                'inconsistent control read length',
            )
        }
    }
    expected_grouped_other_audits = {
        'WARNING': (
            'inconsistent platforms',
            'low read length',
            'mild to moderate bottlenecking',
            'moderate library complexity'
        ),
        'NOT_COMPLIANT': (
            'insufficient read depth',
        ),
        'ERROR': (
            'extremely low read depth',
        )
    }
    for file_id, audits in grouped_file_audits.items():
        for audit, audit_value in expected_grouped_file_audits[file_id].items():
            assert tuple(sorted(set(audits[audit]))) == audit_value
    for audit, audit_value in grouped_other_audits.items():
        assert tuple(sorted(set(audit_value))) == expected_grouped_other_audits[audit]


def test_metadata_metadata_report_init(dummy_request):
    from igvfd.metadata.metadata import MetadataReport
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment'
    )
    mr = MetadataReport(dummy_request)
    assert isinstance(mr, MetadataReport)


def test_metadata_metadata_report_query_string_init_and_param_list(dummy_request):
    from igvfd.metadata.metadata import MetadataReport
    from snosearch.parsers import QueryString
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment'
    )
    mr = MetadataReport(dummy_request)
    assert isinstance(mr.query_string, QueryString)
    expected_param_list = {'type': ['Experiment']}
    assert mr.param_list['type'] == expected_param_list['type']


def test_metadata_metadata_report_get_column_to_fields_mapping(dummy_request):
    from igvfd.metadata.metadata import MetadataReport
    from igvfd.metadata.constants import METADATA_COLUMN_TO_FIELDS_MAPPING
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment'
    )
    mr = MetadataReport(dummy_request)
    assert mr._get_column_to_fields_mapping() == METADATA_COLUMN_TO_FIELDS_MAPPING


def test_metadata_metadata_report_build_header(dummy_request):
    from igvfd.metadata.metadata import MetadataReport
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment'
    )
    mr = MetadataReport(dummy_request)
    mr._build_header()
    expected_header = [
        'File accession',
        'File format',
        'File content',
        'Accession',
        'Assay',
        'Donor(s)',
        'Sample(s)',
        'Creation timestamp',
        'Size',
        'Lab',
        'File download URL',
        'Audit WARNING',
        'Audit NOT_COMPLIANT',
        'Audit ERROR',
    ]
    assert mr.header == expected_header


def test_metadata_metadata_report_split_column_and_fields_by_experiment_and_file(dummy_request):
    from igvfd.metadata.metadata import MetadataReport
    dummy_request.environ['QUERY_STRING'] = (
        'type=FileSet'
    )
    mr = MetadataReport(dummy_request)
    mr._split_column_and_fields_by_experiment_and_file()
    expected_file_column_to_fields_mapping = {
        'File accession': ['accession'],
        'File format': ['file_format'],
        'File content': ['content_type'],
        'Size': ['file_size'],
        'File download URL': ['href'],
    }
    expected_experiment_column_to_fields_mapping = {
        'Accession': ['accession'],
        'Assay': ['assay_term.term_name'],
        'Donor(s)': ['donors.accession'],
        'Sample(s)': ['samples.accession'],
        'Creation timestamp': ['creation_timestamp'],
        'Lab': ['lab.title']
    }
    for k, v in mr.file_column_to_fields_mapping.items():
        assert tuple(expected_file_column_to_fields_mapping[k]) == tuple(v), f'{k, v} not in expected'
    for k, v in mr.experiment_column_to_fields_mapping.items():
        assert tuple(expected_experiment_column_to_fields_mapping[k]) == tuple(v), f'{k, v} not in expected'


def test_metadata_metadata_report_set_positive_file_param_set(dummy_request):
    from igvfd.metadata.metadata import MetadataReport
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_type=bigWig&files.file_type=bam'
        '&files.replicate.library.size_range=50-100'
        '&files.status!=archived&files.biological_replicates=2'
        '&files.file_size=gt:3000&files.file_size=lte:5000000&files.read_count=lt:26'
        '&files.accession=gte:ENCFF000AAA'
    )
    mr = MetadataReport(dummy_request)
    mr._set_split_file_filters()
    mr._set_positive_file_param_set()
    expected_positive_file_param_set = {
        'file_type': set(['bigWig', 'bam']),
        'replicate.library.size_range': set(['50-100']),
        'biological_replicates': set([2])
    }
    for k, v in mr.positive_file_param_set.items():
        assert tuple(sorted(expected_positive_file_param_set[k])) == tuple(sorted(v))


def test_metadata_metadata_report_set_positive_file_inequalities(dummy_request):
    from igvfd.metadata.metadata import MetadataReport
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_type=bigWig&files.file_type=bam'
        '&files.replicate.library.size_range=50-100'
        '&files.status!=archived&files.biological_replicates=2'
        '&files.file_size=gt:3000&files.file_size=lte:5000000&files.read_count=lt:26'
        '&files.accession=gte:ENCFF000AAA'
    )
    mr = MetadataReport(dummy_request)
    mr._set_split_file_filters()
    mr._set_positive_file_inequalities()
    assert len(mr.positive_file_inequalities) == 3
    assert len(mr.positive_file_inequalities['accession']) == 1
    assert len(mr.positive_file_inequalities['file_size']) == 2
    assert len(mr.positive_file_inequalities['read_count']) == 1
    assert all(
        inequality(5000)
        for inequality
        in mr.positive_file_inequalities['file_size']
    )


def test_metadata_metadata_report_add_positive_file_filters_as_fields_to_param_list(dummy_request):
    from igvfd.metadata.metadata import MetadataReport
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_type=bigWig&files.file_type=bam'
        '&files.replicate.library.size_range=50-100'
        '&files.status!=archived&files.biological_replicates=2'
        '&files.read_count=123'
    )
    mr = MetadataReport(dummy_request)
    assert mr.param_list.get('field', []) == []
    mr._add_positive_file_filters_as_fields_to_param_list()
    assert mr.param_list.get('field') == [
        'files.file_type',
        'files.file_type',
        'files.replicate.library.size_range',
        'files.biological_replicates',
        'files.read_count',
    ]


def test_metadata_metadata_report_add_fields_to_param_list(dummy_request):
    from igvfd.metadata.metadata import MetadataReport
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_type=bigWig&files.file_type=bam'
        '&replicates.library.size_range=50-100'
        '&files.status!=archived&files.biological_replicates=2'
        '&files.read_count=123'
    )
    mr = MetadataReport(dummy_request)
    mr._add_fields_to_param_list()
    expected_fields = [
        'files.accession',
        'files.file_format',
        'files.content_type',
        'accession',
        'assay_term.term_name',
        'donors.accession',
        'samples.accession',
        'creation_timestamp',
        'files.file_size',
        'lab.title',
        'files.href',
        'files.file_type',
        'files.file_type',
        'files.biological_replicates',
        'files.read_count'
    ]
    assert set(mr.param_list['field']) == set(expected_fields), f"{set(mr.param_list['field']) - set(expected_fields)}"


def test_metadata_metadata_report_initialize_at_id_param(dummy_request):
    from igvfd.metadata.metadata import MetadataReport
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_type=bigWig&files.file_type=bam'
        '&replicates.library.size_range=50-100'
        '&files.status!=archived&files.biological_replicates=2'
    )
    mr = MetadataReport(dummy_request)
    mr._initialize_at_id_param()
    assert mr.param_list['@id'] == []
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_type=bigWig&files.file_type=bam'
        '&replicates.library.size_range=50-100'
        '&files.status!=archived&files.biological_replicates=2'
        '&@id=/experiments/ENCSR123ABC/'
    )
    mr = MetadataReport(dummy_request)
    mr._initialize_at_id_param()
    assert mr.param_list['@id'] == ['/experiments/ENCSR123ABC/']


def test_metadata_metadata_report_get_json_elements_or_empty_list(dummy_request):
    from igvfd.metadata.metadata import MetadataReport
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_type=bigWig&files.file_type=bam'
        '&replicates.library.size_range=50-100'
        '&files.status!=archived&files.biological_replicates=2'
    )
    mr = MetadataReport(dummy_request)
    mr._initialize_at_id_param()
    at_ids = mr._get_json_elements_or_empty_list()
    assert at_ids == []
    dummy_request.json = {'elements': ['/experiments/ENCSR123ABC/']}
    mr = MetadataReport(dummy_request)
    mr._initialize_at_id_param()
    at_ids = mr._get_json_elements_or_empty_list()
    assert at_ids == [
        '/experiments/ENCSR123ABC/'
    ]
    dummy_request.json = {'elements': []}
    mr = MetadataReport(dummy_request)
    mr._initialize_at_id_param()
    at_ids = mr._get_json_elements_or_empty_list()
    assert at_ids == []


def test_metadata_metadata_report_maybe_add_json_elements_to_param_list(dummy_request):
    from igvfd.metadata.metadata import MetadataReport
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_type=bigWig&files.file_type=bam'
        '&replicates.library.size_range=50-100'
        '&files.status!=archived&files.biological_replicates=2'
    )
    mr = MetadataReport(dummy_request)
    mr._initialize_at_id_param()
    mr._maybe_add_json_elements_to_param_list()
    assert mr.param_list['@id'] == []
    dummy_request.json = {'elements': ['/experiments/ENCSR123ABC/']}
    mr = MetadataReport(dummy_request)
    mr._initialize_at_id_param()
    mr._maybe_add_json_elements_to_param_list()
    assert mr.param_list['@id'] == [
        '/experiments/ENCSR123ABC/'
    ]
    dummy_request.json = {'elements': []}
    mr = MetadataReport(dummy_request)
    mr._initialize_at_id_param()
    mr._maybe_add_json_elements_to_param_list()
    assert mr.param_list['@id'] == []


def test_metadata_metadata_report_get_field_params(dummy_request):
    from igvfd.metadata.metadata import MetadataReport
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_type=bigWig&files.file_type=bam'
        '&replicates.library.size_range=50-100'
        '&files.status!=archived&files.biological_replicates=2'
    )
    mr = MetadataReport(dummy_request)
    mr._add_fields_to_param_list()
    expected_field_params = [
        ('field', 'files.accession'),
        ('field', 'files.file_format'),
        ('field', 'files.content_type'),
        ('field', 'accession'),
        ('field', 'assay_term.term_name'),
        ('field', 'donors.accession'),
        ('field', 'samples.accession'),
        ('field', 'creation_timestamp'),
        ('field', 'files.file_size'),
        ('field', 'lab.title'),
        ('field', 'files.href'),
        ('field', 'files.file_type'),
        ('field', 'files.file_type'),
        ('field', 'files.biological_replicates'),
    ]
    for param in mr._get_field_params():
        assert param in expected_field_params, f'{param}'


def test_metadata_metadata_report_get_at_id_params(dummy_request):
    from igvfd.metadata.metadata import MetadataReport
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_type=bigWig&files.file_type=bam'
        '&replicates.library.size_range=50-100'
        '&files.status!=archived&files.biological_replicates=2'
    )
    dummy_request.json = {'elements': ['/experiments/ENCSR123ABC/']}
    mr = MetadataReport(dummy_request)
    mr._initialize_at_id_param()
    mr._maybe_add_json_elements_to_param_list()
    assert mr._get_at_id_params() == [('@id', '/experiments/ENCSR123ABC/')]


def test_metadata_metadata_report_get_default_params(dummy_request):
    from igvfd.metadata.metadata import MetadataReport
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_type=bigWig&files.file_type=bam'
        '&replicates.library.size_range=50-100'
        '&files.status!=archived&files.biological_replicates=2'
    )
    dummy_request.json = {'elements': ['/experiments/ENCSR123ABC/']}
    mr = MetadataReport(dummy_request)
    assert mr._get_default_params() == [
        ('field', 'audit'),
        ('field', 'files.@id'),
        ('field', 'files.href'),
        ('field', 'files.file_format'),
        ('field', 'files.file_format_type'),
        ('field', 'files.status'),
        ('limit', 'all')
    ]


def test_metadata_metadata_report_build_query_string(dummy_request):
    from igvfd.metadata.metadata import MetadataReport
    dummy_request.environ['QUERY_STRING'] = (
        'type=MeasurementSet&files.file_type=bigWig&files.file_type=bam'
        '&replicates.library.size_range=50-100'
        '&files.status!=archived&files.biological_replicates=2'
    )
    mr = MetadataReport(dummy_request)
    mr._build_query_string()
    assert str(mr.query_string) == (
        'type=MeasurementSet&files.file_type=bigWig'
        '&files.file_type=bam&replicates.library.size_range=50-100'
        '&files.status%21=archived&files.biological_replicates=2'
        '&field=audit&field=files.%40id&field=files.href&field=files.file_format'
        '&field=files.file_format_type&field=files.status&limit=all'
    )


def test_metadata_metadata_report_get_search_path(dummy_request):
    from igvfd.metadata.metadata import MetadataReport
    dummy_request.environ['QUERY_STRING'] = (
        'type=MeasurementSet&files.file_type=bigWig&files.file_type=bam'
        '&replicates.library.size_range=50-100'
        '&files.status!=archived&files.biological_replicates=2'
    )
    mr = MetadataReport(dummy_request)
    assert mr._get_search_path() == '/search/'


def test_metadata_metadata_report_initialize_report(dummy_request):
    from igvfd.metadata.metadata import MetadataReport
    dummy_request.environ['QUERY_STRING'] = (
        'type=MeasurementSet&files.file_type=bigWig&files.file_type=bam'
        '&replicates.library.size_range=50-100'
        '&files.status!=archived&files.biological_replicates=2'
    )
    mr = MetadataReport(dummy_request)
    mr._initialize_report()
    assert len(mr.header) == 14
    assert len(mr.experiment_column_to_fields_mapping.keys()
               ) == 6, f'{len(mr.experiment_column_to_fields_mapping.keys())}'
    assert len(mr.file_column_to_fields_mapping.keys()) == 5, f'{len(mr.file_column_to_fields_mapping.keys())}'
    dummy_request.environ['QUERY_STRING'] = (
        'type=MeasurementSet&files.file_type=bigWig&files.file_type=bam'
        '&replicates.library.size_range=50-100'
        '&files.status!=archived&files.biological_replicates=2'
        '&files.file_size=gte:3000&files.read_count=lt:500000'
        '&files.file_size!=lt:9999'
    )
    mr = MetadataReport(dummy_request)
    mr._initialize_report()
    assert len(mr.positive_file_param_set) == 2
    assert len(mr.positive_file_inequalities) == 2


def test_metadata_metadata_report_build_params(dummy_request):
    from igvfd.metadata.metadata import MetadataReport
    dummy_request.environ['QUERY_STRING'] = (
        'type=MeasurementSet&files.file_type=bigWig&files.file_type=bam'
        '&replicates.library.size_range=50-100'
        '&files.status!=archived&files.biological_replicates=2'
    )
    dummy_request.json = {'elements': ['/experiments/ENCSR123ABC/']}
    mr = MetadataReport(dummy_request)
    mr._build_params()
    assert len(mr.param_list['field']) == 14, f'{len(mr.param_list["field"])} not expected'
    assert len(mr.param_list['@id']) == 1


def test_metadata_metadata_report_build_new_request(dummy_request):
    from igvfd.metadata.metadata import MetadataReport
    dummy_request.environ['QUERY_STRING'] = (
        'type=MeasurementSet&files.file_type=bigWig&files.file_type=bam'
        '&replicates.library.size_range=50-100'
        '&files.status!=archived&files.biological_replicates=2'
        '&files.derived_from=/experiments/ENCSR123ABC/'
        '&files.replicate.library=*'
    )
    dummy_request.json = {'elements': ['/experiments/ENCSR123ABC/']}
    mr = MetadataReport(dummy_request)
    mr._build_params()
    new_request = mr._build_new_request()
    assert new_request.path_info == '/search/'
    assert new_request.registry
    assert str(new_request.query_string) == (
        'type=MeasurementSet&files.file_type=bigWig&files.file_type=bam&replicates.library.size_range=50-100'
        '&files.status%21=archived&files.biological_replicates=2&files.derived_from=%2Fexperiments%2FENCSR123ABC%2F'
        '&files.replicate.library=%2A&field=audit&field=files.%40id&field=files.href&field=files.file_format'
        '&field=files.file_format_type&field=files.status&limit=all&field=files.accession&field=files.content_type'
        '&field=accession&field=assay_term.term_name&field=donors.accession&field=samples.accession&field=creation_timestamp'
        '&field=files.file_size&field=lab.title&field=files.file_type&field=files.biological_replicates'
        '&field=files.derived_from&field=files.replicate.library&%40id=%2Fexperiments%2FENCSR123ABC%2F'
    )
    assert new_request.effective_principals == ['system.Everyone']


def test_metadata_metadata_report_should_not_report_file(dummy_request):
    from igvfd.metadata.metadata import MetadataReport
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_type=bigWig&files.file_type=bam'
        '&replicates.library.size_range=50-100'
        '&files.status!=archived&files.biological_replicates=2'
    )
    mr = MetadataReport(dummy_request)
    mr._initialize_report()
    mr._build_params()
    # File attribute mismatch.
    assert mr._should_not_report_file(file_())
    from igvfd.metadata.metadata import MetadataReport
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_format=bed'
    )
    mr = MetadataReport(dummy_request)
    mr._initialize_report()
    mr._build_params()
    # File attribute match.
    modified_file = file_()
    assert not mr._should_not_report_file(modified_file)
    del modified_file['href']
    # File missing href.
    assert mr._should_not_report_file(modified_file)
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_format=bed&files.file_size=gt:50000'
        '&files.file_size=lte:99999999999&files.biological_replicates=gte:2'
    )
    mr = MetadataReport(dummy_request)
    mr._initialize_report()
    mr._build_params()
    assert not mr._should_not_report_file(file_())
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_format=bed&files.file_size=gt:3356650'
        '&files.file_size=lte:99999999999'
    )
    mr = MetadataReport(dummy_request)
    mr._initialize_report()
    mr._build_params()
    assert mr._should_not_report_file(file_())
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.replicates.rbns_protein_concentration=gt:30'
    )
    mr = MetadataReport(dummy_request)
    mr._initialize_report()
    mr._build_params()
    assert mr._should_not_report_file(file_())
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.title=lt:ENCFF244PJU'
    )
    mr = MetadataReport(dummy_request)
    mr._initialize_report()
    mr._build_params()
    assert mr._should_not_report_file(file_())


def test_metadata_metadata_report_get_experiment_data(dummy_request):
    from igvfd.metadata.metadata import MetadataReport
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_type=bigWig&files.file_type=bam'
        '&replicates.library.size_range=50-100'
        '&files.status!=archived&files.biological_replicates=2'
    )
    mr = MetadataReport(dummy_request)
    mr._initialize_report()
    mr._build_params()
    expected_experiment_data = {
        'Accession': 'ENCSR434TGY',
        'Assay': '',
        'Donor(s)': '',
        'Sample(s)': '',
        'Creation timestamp': '',
        'Lab': ''
    }
    experiment_data = mr._get_experiment_data(embedded_experiment())
    for k, v in expected_experiment_data.items():
        assert experiment_data[k] == v, f'{experiment_data[k]} not equal to {v}'


def test_metadata_metadata_report_get_file_data(dummy_request):
    from igvfd.metadata.metadata import MetadataReport
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment'
    )
    mr = MetadataReport(dummy_request)
    mr._initialize_report()
    mr._build_params()
    expected_file_data = {
        'File accession': '',
        'File format': 'bed',
        'File content': '',
        'Size': 3356650,
        'File download URL': 'http://localhost/files/ENCFF244PJU/@@download/ENCFF244PJU.bed.gz'
    }
    file_data = mr._get_file_data(file_())
    for k, v in expected_file_data.items():
        assert file_data[k] == v


def test_metadata_metadata_report_get_audit_data(dummy_request):
    from igvfd.metadata.metadata import MetadataReport
    from igvfd.metadata.metadata import group_audits_by_files_and_type
    grouped_file_audits, grouped_other_audits = group_audits_by_files_and_type(audits_())
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment'
    )
    mr = MetadataReport(dummy_request)
    mr._initialize_report()
    mr._build_params()
    audit_data = mr._get_audit_data(
        grouped_file_audits.get('/files/ENCFF783ZRQ/'),
        grouped_other_audits
    )
    expected_audit_data = {
        'Audit WARNING': [
            'inconsistent control read length',
            'inconsistent platforms',
            'low read length',
            'mild to moderate bottlenecking',
            'moderate library complexity'
        ],
        'Audit NOT_COMPLIANT': ['insufficient read depth'],
        'Audit ERROR': ['extremely low read depth']
    }
    for k, v in expected_audit_data.items():
        assert sorted(audit_data[k].split(', ')) == v, f'{sorted(audit_data[k].split(", "))} does not match {v}'
