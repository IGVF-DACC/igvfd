import gzip
import json
import pickle
import sqlite3
import zlib

from pathlib import Path

from sqlitedict import SqliteDict


ONTOLOGY_FILE_NAME = 'ontology.json.gz'

REFERENCE_DATABASE_FILE_NAME = '/srv/sqlite/reference.sqlite'

REFERENCE_ONTOLOGY_TABLE_NAME = 'ontology'


def includeme(config):
    config.scan(__name__)
    config.registry['ontology'] = get_connection_to_reference_database(
        REFERENCE_ONTOLOGY_TABLE_NAME
    )


def load_local_gz_json(path):
    with gzip.open(path, 'rt', encoding='utf-8') as local_file:
        data = json.load(local_file)
    return data


def get_ontology_gz_json_path():
    return Path(__file__).resolve().parents[2] / 'assets' / ONTOLOGY_FILE_NAME


def ontology_or_empty_dict(path):
    if path.exists():
        return load_local_gz_json(path)
    return {}


def load_ontology():
    path = get_ontology_gz_json_path()
    return ontology_or_empty_dict(path)


def item_compress(item):
    return zlib.compress(
        pickle.dumps(
            item,
            pickle.HIGHEST_PROTOCOL
        )
    )


def item_decompress(item):
    return pickle.loads(
        zlib.decompress(
            item
        )
    )


def item_encode(item):
    return sqlite3.Binary(
        item_compress(
            item
        )
    )


def item_decode(item):
    return item_decompress(
        bytes(
            item
        )
    )


def write_data_to_reference_database(
        data,
        tablename,
        encode=item_encode,
        decode=item_decode,
        flag='w',
        filename=REFERENCE_DATABASE_FILE_NAME,
):
    with SqliteDict(
            filename=filename,
            tablename=tablename,
            encode=encode,
            decode=decode,
            flag=flag,
            outer_stack=False,
    ) as db:
        db.update(data)
        db.commit()


def get_connection_to_reference_database(
        tablename,
        encode=item_encode,
        decode=item_decode,
        flag='r',
        filename=REFERENCE_DATABASE_FILE_NAME,
):
    return SqliteDict(
        filename=filename,
        tablename=tablename,
        encode=encode,
        decode=decode,
        flag=flag,
        outer_stack=False,
    )
