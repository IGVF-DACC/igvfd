import pytest
from igvfd.tests.test_permissions import _remote_user_testapp


def test_samples_link(testapp, tissue, base_expression_construct_library_set):
    testapp.patch_json(
        tissue['@id'],
        {
            'construct_library_sets': [base_expression_construct_library_set['@id']]
        }
    )
    res = testapp.get(base_expression_construct_library_set['@id'])
    assert set([sample_id['@id'] for sample_id in res.json.get('applied_to_samples')]) == {tissue['@id']}


def test_summary(testapp, construct_library_set_genome_wide, base_expression_construct_library_set,
                 construct_library_set_reporter, phenotype_term_alzheimers, phenotype_term_myocardial_infarction,
                 gene_zscan10_mm, gene_myc_hs, construct_library_set_y2h, construct_library_set_orf, orf_foxp, orf_zscan10, construct_library_set_reference_transduction, construct_library_set_editing_template_library):
    res = testapp.get(construct_library_set_genome_wide['@id'])
    assert res.json.get('summary') == 'guide (sgRNA) library targeting TF binding sites genome-wide'
    testapp.patch_json(
        construct_library_set_reporter['@id'],
        {
            'scope': 'loci',
            'selection_criteria': ['accessible genome regions', 'phenotype-associated variants'],
            'associated_phenotypes': [phenotype_term_alzheimers['@id']],
            'small_scale_loci_list': [{
                'assembly': 'GRCh38',
                'chromosome': 'chr1',
                'start': 1,
                'end': 100
            }
            ]
        }
    )
    res = testapp.get(construct_library_set_reporter['@id'])
    assert res.json.get(
        'summary') == 'reporter library targeting accessible genome regions, phenotype-associated variants in a genomic locus associated with Alzheimer\'s disease'
    testapp.patch_json(
        construct_library_set_reporter['@id'],
        {
            'small_scale_loci_list': [
                {
                    'assembly': 'GRCh38',
                    'chromosome': 'chr1',
                    'start': 1,
                    'end': 100
                },
                {
                    'assembly': 'GRCh38',
                    'chromosome': 'chr2',
                    'start': 1,
                    'end': 100
                },
                {
                    'assembly': 'GRCh38',
                    'chromosome': 'chr3',
                    'start': 1,
                    'end': 100
                }
            ],
            'associated_phenotypes': [phenotype_term_alzheimers['@id'], phenotype_term_myocardial_infarction['@id']]
        }
    )
    res = testapp.get(construct_library_set_reporter['@id'])
    assert res.json.get(
        'summary') == 'reporter library targeting accessible genome regions, phenotype-associated variants in 3 genomic loci associated with Alzheimer\'s disease and Myocardial infarction'
    # An exon-scope object should only have 1 gene specified; the first gene symbol is used in the summary
    # The selection_criteria of 'genes' is redundant for an expression vector library, but actual selection_criteria property should not be altered
    testapp.patch_json(
        base_expression_construct_library_set['@id'],
        {
            'selection_criteria': ['genes'],
            'small_scale_gene_list': [gene_myc_hs['@id']]
        }
    )
    res = testapp.get(base_expression_construct_library_set['@id'])
    assert res.json.get('summary') == 'expression vector library of exon E3 of MYC'
    testapp.patch_json(
        base_expression_construct_library_set['@id'],
        {
            'selection_criteria': ['genes'],
            'small_scale_gene_list': [gene_myc_hs['@id'], gene_zscan10_mm['@id']]
        }
    )
    res = testapp.get(base_expression_construct_library_set['@id'])
    assert res.json.get('selection_criteria') == ['genes']
    assert res.json.get('summary') == 'expression vector library of exon E3 of multiple genes'
    res = testapp.get(construct_library_set_y2h['@id'])
    assert res.json.get('summary') == 'expression vector library of 2 genes (protein interactors)'
    testapp.patch_json(
        construct_library_set_y2h['@id'],
        {
            'selection_criteria': ['protein interactors', 'genes', 'phenotype-associated variants'],
            'small_scale_gene_list': [gene_myc_hs['@id']],
            'associated_phenotypes': [phenotype_term_myocardial_infarction['@id']]
        }
    )
    res = testapp.get(construct_library_set_y2h['@id'])
    assert res.json.get(
        'summary') == 'expression vector library of MYC (protein interactors, phenotype-associated variants) associated with Myocardial infarction'
    testapp.patch_json(
        construct_library_set_y2h['@id'],
        {
            'selection_criteria': ['protein interactors', 'genes', 'phenotype-associated variants'],
            'small_scale_gene_list': [gene_myc_hs['@id']],
            'scope': 'tile',
            'tile': {'tile_id': 'tile1', 'tile_start': 1, 'tile_end': 96
                     },
            'associated_phenotypes': [phenotype_term_myocardial_infarction['@id']]
        }
    )
    res = testapp.get(construct_library_set_y2h['@id'])
    assert res.json.get(
        'summary') == 'expression vector library of tile tile1 of MYC (AA 1-96) (protein interactors, phenotype-associated variants) associated with Myocardial infarction'
    res = testapp.get(construct_library_set_orf['@id'])
    assert res.json.get(
        'summary') == 'expression vector library of open reading frame CCSBORF1234 of MYC (protein interactors)'
    testapp.patch_json(
        construct_library_set_orf['@id'],
        {
            'small_scale_gene_list': [gene_myc_hs['@id'], gene_zscan10_mm['@id']],
            'orf_list': [orf_foxp['@id'], orf_zscan10['@id']]
        }
    )
    res = testapp.get(construct_library_set_orf['@id'])
    assert res.json.get(
        'summary') == 'expression vector library of 2 open reading frames (protein interactors)'
    # control library summaries
    testapp.patch_json(
        construct_library_set_genome_wide['@id'],
        {
            'scope': 'control',
            'control_type': 'non-targeting'
        }
    )
    res = testapp.get(construct_library_set_genome_wide['@id'])
    assert res.json.get('summary') == 'non-targeting guide (sgRNA) library'
    res = testapp.get(construct_library_set_reference_transduction['@id'])
    assert res.json.get('summary') == 'reference transduction expression vector library'
    res = testapp.get(construct_library_set_editing_template_library['@id'])
    assert res.json.get('summary') == 'editing template library targeting histone modifications in targeton1 of MYC'


def test_summary_starr_seq_1000_genomes(testapp, construct_library_set_reporter, human_donor, human_donor_orphan, curated_set_genome, tabular_file):
    testapp.patch_json(
        human_donor['@id'],
        {
            'dbxrefs': ['IGSR:NA18910']
        }
    )
    testapp.patch_json(
        human_donor_orphan['@id'],
        {
            'dbxrefs': ['IGSR:NA18912']
        }
    )
    testapp.patch_json(
        curated_set_genome['@id'],
        {
            'donors': [human_donor['@id'], human_donor_orphan['@id']]
        }
    )
    testapp.patch_json(
        tabular_file['@id'],
        {
            'file_set': curated_set_genome['@id']
        }
    )
    testapp.patch_json(
        construct_library_set_reporter['@id'],
        {
            'integrated_content_files': [tabular_file['@id']]
        }
    )
    res = testapp.get(construct_library_set_reporter['@id'])
    assert res.json.get(
        'summary') == 'reporter library targeting accessible genome regions genome-wide pooled from 1000 Genomes donors: NA18912, NA18910'


def test_integrated_content_files_dependency(testapp, app, submitter, lab, award, tabular_file, signal_file):
    testapp.patch_json(submitter['@id'], {'groups': ['verified']})
    test_user = _remote_user_testapp(app, submitter['uuid'])

    item = {
        'lab': lab['@id'],
        'award': award['@id'],
        'file_set_type': 'reporter library',
        'scope': 'genome-wide',
        'selection_criteria': ['accessible genome regions'],
        'integrated_content_files': [tabular_file['@id']]
    }
    cls = test_user.post_json('/construct_library_set', item, status=201).json['@graph'][0]

    res = test_user.patch_json(
        cls['@id'],
        {'integrated_content_files': [signal_file['@id']]}, expect_errors=True)
    assert res.status_code == 422
    res = test_user.patch_json(
        cls['@id'],
        {'integrated_content_files': [signal_file['@id'], tabular_file['@id']]}, expect_errors=True)
    assert res.status_code == 422
