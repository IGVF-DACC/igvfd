import pytest


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
                 gene_zscan10_mm, gene_myc_hs, construct_library_set_y2h):
    res = testapp.get(construct_library_set_genome_wide['@id'])
    assert res.json.get('summary') == 'Guide (sgRNA) library targeting TF binding sites genome-wide'
    testapp.patch_json(
        construct_library_set_reporter['@id'],
        {
            'scope': 'loci',
            'selection_criteria': ['accessible genome regions', 'phenotype-associated variants'],
            'associated_phenotypes': [phenotype_term_alzheimers['@id']],
            'loci': [{
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
        'summary') == 'Reporter library targeting accessible genome regions, phenotype-associated variants in a genomic locus associated with Alzheimer\'s disease'
    testapp.patch_json(
        construct_library_set_reporter['@id'],
        {
            'loci': [
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
        'summary') == 'Reporter library targeting accessible genome regions, phenotype-associated variants in 3 genomic loci associated with Alzheimer\'s disease, Myocardial infarction'
    # An exon-scope object should only have 1 gene specified; the first gene symbol is used in the summary
    # The selection_criteria of 'genes' is redundant for an expression vector library, but actual selection_criteria property should not be altered
    testapp.patch_json(
        base_expression_construct_library_set['@id'],
        {
            'selection_criteria': ['genes'],
            'genes': [gene_myc_hs['@id']]
        }
    )
    res = testapp.get(base_expression_construct_library_set['@id'])
    assert res.json.get('summary') == 'Expression vector library of exon E3 of MYC'
    testapp.patch_json(
        base_expression_construct_library_set['@id'],
        {
            'selection_criteria': ['genes'],
            'genes': [gene_myc_hs['@id'], gene_zscan10_mm['@id']]
        }
    )
    res = testapp.get(base_expression_construct_library_set['@id'])
    assert res.json.get('selection_criteria') == ['genes']
    assert res.json.get('summary') == 'Expression vector library of exon E3 of multiple genes'
    res = testapp.get(construct_library_set_y2h['@id'])
    assert res.json.get('summary') == 'Expression vector library of 2 genes (protein interactors)'
    testapp.patch_json(
        construct_library_set_y2h['@id'],
        {
            'selection_criteria': ['protein interactors', 'genes', 'phenotype-associated variants'],
            'genes': [gene_myc_hs['@id']],
            'associated_phenotypes': [phenotype_term_myocardial_infarction['@id']]
        }
    )
    res = testapp.get(construct_library_set_y2h['@id'])
    assert res.json.get(
        'summary') == 'Expression vector library of MYC (protein interactors, phenotype-associated variants) associated with Myocardial infarction'
