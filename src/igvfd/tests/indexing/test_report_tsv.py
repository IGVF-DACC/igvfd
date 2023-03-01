import pytest


pytestmark = [pytest.mark.indexing]


def test_batch_download_report_download(workbook, testapp):
    res = testapp.get('/report.tsv?type=Award&sort=accession')
    assert res.headers['content-type'] == 'text/tsv; charset=UTF-8'
    disposition = res.headers['content-disposition']
    assert disposition.startswith('attachment;filename="award_report') and disposition.endswith('.tsv"')
    lines = res.body.splitlines()
    assert b'/report/' in lines[0]
    assert lines[1].split(b'\t') == [
        b'ID', b'UUID', b'Title', b'Name', b'Project', b'Component', b'Status'
    ]
    assert len(lines) == 27

    res = testapp.get('/report.tsv?type=Award&field=contact_pi&field=title')
    assert res.headers['content-type'] == 'text/tsv; charset=UTF-8'
    disposition = res.headers['content-disposition']
    assert disposition.startswith('attachment;filename="award_report') and disposition.endswith('.tsv"')
    lines = res.body.splitlines()
    assert b'/report/' in lines[0]
    assert lines[1].split(b'\t') == [
        b'Contact P.I.', b'Title'
    ]


def test_batch_download_human_donor_report_download(workbook, testapp):
    res = testapp.get('/report.tsv?type=HumanDonor&sort=accession')
    disposition = res.headers['content-disposition']
    assert disposition.startswith('attachment;filename="human_donor_report') and disposition.endswith('.tsv"')
