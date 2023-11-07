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
        b'ID', b'UUID', b'Title', b'Name', b'Project', b'Component', b'Contact P.I.', b'Status'
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


def test_multitype_report_download_no_href(workbook, testapp):

    res = testapp.get('/multireport.tsv?institute_label=Stanford')
    assert res.headers['content-type'] == 'text/tsv; charset=UTF-8'
    disposition = res.headers['content-disposition']
    assert disposition.startswith('attachment;filename="igvf_lab') and disposition.endswith('.tsv"')
    lines = res.body.splitlines()
    assert b'/multireport/' in lines[0]
    assert lines[1].split(b'\t') == [
        b'ID', b'UUID', b'Title', b'Aliases', b'Awards', b'Name', b'Status', b'Principle Investigator', b'Institute Label'
    ]

    res = testapp.get('/multireport.tsv?type=Award&field=contact_pi&field=title&config=Award')
    assert res.headers['content-type'] == 'text/tsv; charset=UTF-8'
    disposition = res.headers['content-disposition']
    assert disposition.startswith('attachment;filename="igvf_award') and disposition.endswith('.tsv"')
    lines = res.body.splitlines()
    assert b'/multireport/' in lines[0]
    assert lines[1].split(b'\t') == [
        b'Contact P.I.', b'Title'
    ]

    res = testapp.get('/multireport.tsv?type=Award&config=AccessKey')
    assert res.headers['content-type'] == 'text/tsv; charset=UTF-8'
    disposition = res.headers['content-disposition']
    assert disposition.startswith('attachment;filename="igvf_award') and disposition.endswith('.tsv"')
    lines = res.body.splitlines()
    assert b'/multireport/' in lines[0]
    assert lines[1].split(b'\t') == [
        b'ID', b'UUID', b'Status', b'Access Key ID'
    ]

    res = testapp.get('/multireport.tsv?type=File&status=released')
    assert res.headers['content-type'] == 'text/tsv; charset=UTF-8'
    disposition = res.headers['content-disposition']
    assert disposition.startswith('attachment;filename="igvf_mixed') and disposition.endswith('.tsv"')
    lines = res.body.splitlines()
    assert b'/multireport/' in lines[0]
    assert lines[1].split(b'\t') == [
        b'ID', b'UUID', b'Accession', b'Alternate Accessions', b'Content Type', b'File Format', b'Lab', b'Status', b'File Set', b'Illumina Read Type', b'External Identifiers', b'Upload Status', b'Reference Files', b'Content Summary', b'Assembly', b'Transcriptome Annotation', b'Seqspec Of'
    ]

    res = testapp.get('/multireport.tsv?type=SequenceFile&type=AlignmentFile&status=released')
    assert res.headers['content-type'] == 'text/tsv; charset=UTF-8'
    disposition = res.headers['content-disposition']
    assert disposition.startswith('attachment;filename="igvf_mixed') and disposition.endswith('.tsv"')
    lines = res.body.splitlines()
    assert b'/multireport/' in lines[0]
    assert lines[1].split(b'\t') == [
        b'ID', b'UUID', b'Accession', b'Alternate Accessions', b'Content Type', b'File Format', b'Lab', b'Status', b'File Set', b'Illumina Read Type', b'External Identifiers', b'Upload Status', b'Reference Files', b'Content Summary'
    ]


def test_multitype_report_download_href(workbook, testapp):

    res = testapp.get('/multireport.tsv?type=File&field=href')
    lines = res.text.splitlines()
    server_url = res.headers['X-Request-URL'].split('/multireport.tsv?')[0]
    assert lines[2].startswith(server_url)

    res = testapp.get('/multireport.tsv?type=Image&field=%40id&field=attachment')
    lines = res.text.splitlines()
    server_url = res.headers['X-Request-URL'].split('/multireport.tsv?')[0]
    id = lines[2].split('\t')[1]
    full_href = server_url + id + '@@download/attachment/h3k4me3_millipore_07-473_lot_DAM1651667_WB.png'
    assert lines[2][1] == full_href

    res = testapp.get('/multireport.tsv?type=Image&field=%40id&field=attachment.href')
    lines = res.text.splitlines()
    server_url = res.headers['X-Request-URL'].split('/multireport.tsv?')[0]
    id = lines[2].split('\t')[1]
    full_href = server_url + id + '@@download/attachment/h3k4me3_millipore_07-473_lot_DAM1651667_WB.png'
    assert lines[2][1] == full_href
