import pytest


def test_analysis_step_upgrade_1_2(upgrader, analysis_step_v1):
    value = upgrader.upgrade('analysis_step', analysis_step_v1, current_version='1', target_version='2')
    assert 'parents' not in value
    assert value['analysis_step_types'] == ['alignment']
    assert value['input_content_types'] == ['reads']
    assert value['output_content_types'] == ['reads']
    assert value['schema_version'] == '2'


def test_analysis_step_upgrade_2_3(upgrader, analysis_step_v2):
    value = upgrader.upgrade('analysis_step', analysis_step_v2, current_version='2', target_version='3')
    assert value['lab'] == '/labs/j-michael-cherry/'
    assert value['award'] == '/awards/HG012012/'


def test_analysis_step_upgrade_5_6(upgrader, analysis_step_v5):
    value = upgrader.upgrade('analysis_step', analysis_step_v5, current_version='5', target_version='6')
    assert sorted(value['input_content_types']) == sorted(['reads', 'barcode onlist'])
    assert sorted(value['output_content_types']) == sorted(['alignments'])
    assert value['schema_version'] == '6'


def test_analysis_step_upgrade_6_7(upgrader, analysis_step_v6):
    value = upgrader.upgrade('analysis_step', analysis_step_v6, current_version='6', target_version='7')
    assert sorted(value['input_content_types']) == sorted(['reads', 'kallisto single cell RNAseq output'])
    assert sorted(value['output_content_types']) == sorted(['alignments', 'kallisto single cell RNAseq output'])
    assert value['schema_version'] == '7'


def test_analysis_step_upgrade_8_9(upgrader, analysis_step_v8):
    assert 'workflow' in analysis_step_v8
    assert analysis_step_v8['schema_version'] == '8'
    value = upgrader.upgrade('analysis_step', analysis_step_v8, current_version='8', target_version='9')
    assert 'workflow' not in value
    assert value['schema_version'] == '9'


def test_analysis_step_upgrade_9_10(upgrader, analysis_step_v9):
    value = upgrader.upgrade('analysis_step', analysis_step_v9, current_version='9', target_version='10')
    assert sorted(value['input_content_types']) == sorted(['elements reference'])
    assert sorted(value['output_content_types']) == sorted(['elements reference'])
    assert value['schema_version'] == '10'


def test_analysis_step_upgrade_10_11(upgrader, analysis_step_v10):
    value = upgrader.upgrade('analysis_step', analysis_step_v10, current_version='10', target_version='11')
    assert len(value['input_content_types']) == 2
    assert set(value['input_content_types']) == {'global differential expression', 'local differential expression'}
    assert len(value['output_content_types']) == 2
    assert set(value['output_content_types']) == {'global differential expression', 'local differential expression'}
    assert value['schema_version'] == '11'


def test_analysis_step_upgrade_11_12(upgrader, analysis_step_v11):
    value = upgrader.upgrade('analysis_step', analysis_step_v11, current_version='11', target_version='12')
    assert len(value['input_content_types']) == 2
    assert set(value['input_content_types']) == {'cell by gene matrix', 'kallisto cell by gene matrix'}
    assert len(value['output_content_types']) == 3
    assert set(value['output_content_types']) == {'annotated cell by peak matrix',
                                                  'cell by gene matrix', 'mitochondrial variants by cell heteroplasmy matrix'}
    assert ('This analysis step\'s input_content_types included annotated multimodal CRISPR matrix, '
            'but has been upgraded to cell by gene matrix.') in value['notes']
    assert ('This analysis step\'s input_content_types included kallisto single cell RNAseq output, '
            'but has been upgraded to kallisto cell by gene matrix.') in value['notes']
    assert ('This analysis step\'s input_content_types included raw feature barcode matrix, '
            'but has been upgraded to cell by gene matrix.') in value['notes']
    assert ('This analysis step\'s output_content_types included mitochondrial DNA heteroplasmy, '
            'but has been upgraded to mitochondrial variants by cell heteroplasmy matrix.') in value['notes']
    assert ('This analysis step\'s output_content_types included annotated sparse peak count matrix, '
            'but has been upgraded to annotated cell by peak matrix.') in value['notes']
    assert ('This analysis step\'s output_content_types included sparse transcript count matrix, '
            'but has been upgraded to cell by gene matrix.') in value['notes']
    assert ('This analysis step\'s output_content_types included filtered feature barcode matrix, '
            'but has been upgraded to cell by gene matrix.') in value['notes']
    assert value['schema_version'] == '12'


def test_analysis_step_upgrade_12_13(upgrader, analysis_step_v12):
    value = upgrader.upgrade('analysis_step', analysis_step_v12, current_version='12', target_version='13')
<<<<<<< HEAD
    assert set(value['input_content_types']) == {'loci', 'peaks'}
    assert set(value['output_content_types']) == {'loci'}
    assert 'exclusion list regions was removed from input_content_types, and has been defaulted to loci.' in value[
        'notes']
    assert 'exclusion list regions was removed from output_content_types, and has been defaulted to loci.' in value[
        'notes']
    assert value['schema_version'] == '13'
=======
    assert value['schema_version'] == '13'
    assert value['input_content_types'] == ['differential open reading frame quantifications']
    assert set(value['output_content_types']) == {
        'differential open reading frame quantifications',
        'peaks',
    }
    assert (
        'This analysis step\'s input_content_types included differential TF enrichment quantifications, '
        'but has been upgraded to differential open reading frame quantifications.'
    ) in value['notes']
    assert (
        'This analysis step\'s output_content_types included differential TF enrichment quantifications, '
        'but has been upgraded to differential open reading frame quantifications.'
    ) in value['notes']
>>>>>>> 1ffd91bf (upgrades added)
