import pytest


pytestmark = [pytest.mark.indexing]


def test_batch_download_report_download(workbook, testapp):
    res = testapp.get('/report.tsv?type=File&sort=accession')
    assert res.headers['content-type'] == 'text/tsv; charset=UTF-8'
    disposition = res.headers['content-disposition']
    assert disposition.startswith('attachment;filename="file_report') and disposition.endswith('.tsv"')
    lines = res.body.splitlines()
    assert b'/report/' in lines[0]
    assert lines[1].split(b'\t') == [
        b'ID', b'Description', b'Accession', b'Aliases'
    ]
    assert len(lines) == 7


def test_batch_download_human_donor_report_download(workbook, testapp):
    res = testapp.get('/report.tsv?type=HumanDonor&sort=accession')
    disposition = res.headers['content-disposition']
    assert disposition.startswith('attachment;filename="human_donor_report') and disposition.endswith('.tsv"')
    res = testapp.get('/report.tsv?type=human_donor&sort=accession')
    disposition = res.headers['content-disposition']
    assert disposition.startswith('attachment;filename="human_donor_report') and disposition.endswith('.tsv"')
