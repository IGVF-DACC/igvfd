import pytest


def test_metadata_csv_csv_generator():
    from igvfd.metadata.csv import CSVGenerator
    csv = CSVGenerator()
    row = csv.writerow(['a', 'b', '123'])
    assert row == b'a\tb\t123\n'
