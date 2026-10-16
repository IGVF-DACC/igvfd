import pytest

N_FILES = 6


@pytest.fixture
def many_sequence_files(testapp, lab, award, principal_analysis_set, platform_term_HiSeq):
    files = []
    for i in range(N_FILES):
        item = {
            'award': award['@id'],
            'lab': lab['@id'],
            'md5sum': f'{i + 1:032x}',
            'file_format': 'fastq',
            'file_set': principal_analysis_set['@id'],
            'minimum_read_length': 99,
            'maximum_read_length': 101,
            'mean_read_length': 100,
            'read_count': 23040138 + i,
            'file_size': 5495803 + i,
            'content_type': 'reads',
            'sequencing_run': i + 1,
            'sequencing_platform': platform_term_HiSeq['@id'],
            'controlled_access': False,
        }
        files.append(testapp.post_json('/sequence_file', item, status=201).json['@graph'][0])
    return files


def get_json(testapp, url, batch_embed):
    separator = '&' if '?' in url else '?'
    query = f'datastore=database&batch_embed={str(batch_embed).lower()}'
    return testapp.get(f'{url}{separator}{query}').json


@pytest.mark.parametrize('frame', ['object', 'embedded', 'page'])
def test_analysis_set_rendering_identical_with_and_without_batch_embed(
    testapp, principal_analysis_set, many_sequence_files, frame
):
    url = f'{principal_analysis_set["@id"]}?frame={frame}'
    batched = get_json(testapp, url, True)
    unbatched = get_json(testapp, url, False)
    assert len(batched['files']) == N_FILES
    assert batched == unbatched


@pytest.mark.parametrize('frame', ['object', 'embedded', 'page'])
def test_measurement_set_rendering_identical_with_and_without_batch_embed(
    testapp, measurement_set, many_sequence_files, frame
):
    url = f'{measurement_set["@id"]}?frame={frame}'
    assert get_json(testapp, url, True) == get_json(testapp, url, False)


def test_file_rendering_identical_with_and_without_batch_embed(
    testapp, many_sequence_files
):
    for sequence_file in many_sequence_files:
        for frame in ('object', 'embedded'):
            url = f'{sequence_file["@id"]}?frame={frame}'
            assert get_json(testapp, url, True) == get_json(testapp, url, False)


def test_audit_identical_with_and_without_batch_embed(
    testapp, principal_analysis_set, measurement_set, many_sequence_files
):
    for item in (principal_analysis_set, measurement_set):
        url = f'{item["@id"]}@@audit'
        assert get_json(testapp, url, True) == get_json(testapp, url, False)
