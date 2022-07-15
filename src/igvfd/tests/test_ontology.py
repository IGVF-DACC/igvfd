import pytest


def test_ontology_exists_in_registry(registry):
    assert registry.get('ontology') is not None


def test_ontology_get_ontology_gz_json_path():
    from igvfd.ontology import get_ontology_gz_json_path
    path = get_ontology_gz_json_path()
    assert str(path) == '/igvfd/assets/ontology.json.gz'


def test_ontology_file_exists():
    from igvfd.ontology import get_ontology_gz_json_path
    path = get_ontology_gz_json_path()
    assert path.exists(), 'Ontology JSON not found'


def test_ontology_load_ontology_or_empty_dict():
    from pathlib import Path
    from igvfd.ontology import ontology_or_empty_dict
    from igvfd.ontology import get_ontology_gz_json_path
    path = Path('/igvfd/assets/badpath.json.gz')
    assert ontology_or_empty_dict(path) == {}
    path = get_ontology_gz_json_path()
    assert len(ontology_or_empty_dict(path).keys()) > 150000


def test_ontology_load_ontology():
    from igvfd.ontology import load_ontology
    data = load_ontology()
    assert len(data.keys()) > 150000


def test_ontology_item_compress():
    from igvfd.ontology import item_compress
    item = {
        'a': 'b',
        'c': ['d', 'e', 'f', {'x': False}, 'y', 1, 'z'],
        1: True
    }
    actual = item_compress(item)
    expected = (
        b'x\x9ck`\x9dj\xc6\x00\x01'
        b'\xb5S4z\x18\x13\xa7\xf40&'
        b'\x01q\xf2\x94X\x107\x05'
        b'\xc8L\x05\xe2\xb4)\xb5@'
        b'\xb2bJgq\x0fc\xe5\x14o'
        b'\xc6\x1e\xc6\xaa)\xa9\xde'
        b'\x8c\x1d\xa5z\x00\x90R'
        b'\x15\xc1'
    )
    assert actual == expected


def test_ontology_item_decompress():
    from igvfd.ontology import item_decompress
    compressed_item = (
        b'x\x9ck`\x9dj\xc6\x00\x01'
        b'\xb5S4z\x18\x13\xa7\xf40&'
        b'\x01q\xf2\x94X\x107\x05'
        b'\xc8L\x05\xe2\xb4)\xb5@'
        b'\xb2bJgq\x0fc\xe5\x14o'
        b'\xc6\x1e\xc6\xaa)\xa9\xde'
        b'\x8c\x1d\xa5z\x00\x90R'
        b'\x15\xc1'
    )
    actual = item_decompress(compressed_item)
    expected = {
        'a': 'b',
        'c': ['d', 'e', 'f', {'x': False}, 'y', 1, 'z'],
        1: True
    }
    assert actual == expected


def test_ontology_item_compress_and_decompress():
    from igvfd.ontology import item_compress
    from igvfd.ontology import item_decompress
    item = {
        'abcdefg': 'hijk',
        't': ['z'],
        5: False,
    }
    multiitem = [item, item]
    assert item_decompress(item_compress(item)) == item
    assert item_decompress(item_compress(multiitem)) == multiitem


def test_ontology_item_encode():
    from igvfd.ontology import item_encode
    item = {
        'a': 'b',
        'c': ['d', 'e', 'f', {'x': False}, 'y', 1, 'z'],
        1: True
    }
    encoded_item = item_encode(item)
    assert isinstance(encoded_item, memoryview)


def test_ontology_item_decode():
    from igvfd.ontology import item_decode
    encoded_item = (
        b'x\x9ck`\x9dj\xc6\x00\x01'
        b'\xb5S4z\x18\x13\xa7\xf40&'
        b'\x01q\xf2\x94X\x107\x05'
        b'\xc8L\x05\xe2\xb4)\xb5@'
        b'\xb2bJgq\x0fc\xe5\x14o'
        b'\xc6\x1e\xc6\xaa)\xa9\xde'
        b'\x8c\x1d\xa5z\x00\x90R'
        b'\x15\xc1'
    )
    actual = item_decode(encoded_item)
    expected = {
        'a': 'b',
        'c': ['d', 'e', 'f', {'x': False}, 'y', 1, 'z'],
        1: True
    }
    assert actual == expected


def test_ontology_item_encode_and_decode():
    from igvfd.ontology import item_encode
    from igvfd.ontology import item_decode
    item = {
        'a': 'b',
        'c': ['d', 'e', 'f', {'x': False}, 'y', 1, 'z'],
        1: True
    }
    decoded_item = item_decode(item_encode(item))
    assert decoded_item == item


def test_ontology_write_data_to_reference_database():
    import os
    from igvfd.ontology import write_data_to_reference_database
    data = {
        'a': 'b',
        'c': ['d', 'e', 'f', {'x': False}, 'y', 1, 'z'],
        1: True
    }
    filename = 'test.sqlite'
    tablename = 'testdata'
    write_data_to_reference_database(
        data,
        tablename,
        filename=filename,
    )
    assert os.path.isfile(filename)
    # Clean up.
    os.remove(filename)
    assert not os.path.isfile(filename)


def test_ontology_get_connection_to_reference_database():
    import os
    from igvfd.ontology import write_data_to_reference_database
    from igvfd.ontology import get_connection_to_reference_database
    from sqlitedict import SqliteDict
    data = {
        'a': 'b',
        'c': ['d', 'e', 'f', {'x': False}, 'y', 1, 'z'],
        1: True
    }
    filename = 'test.sqlite'
    tablename = 'testdata'
    write_data_to_reference_database(
        data,
        tablename,
        filename=filename,
    )
    db = get_connection_to_reference_database(
        tablename,
        filename=filename,
    )
    assert isinstance(db, SqliteDict)
    assert 1 in db
    assert db[1] == True
    assert 'c' in db
    assert 'd' not in db
    for k, v in data.items():
        assert db[k] == v
    # Clean up.
    os.remove(filename)
    assert not os.path.isfile(filename)
