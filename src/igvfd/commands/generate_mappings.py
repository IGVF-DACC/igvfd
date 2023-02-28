import hashlib

import json

import os

from pathlib import Path

from pyramid.paster import get_app

from snovault.elasticsearch.create_mapping import generate_indices_and_mappings


class UnexpectedMappingError(Exception):
    pass


def maybe_raise_on_diff(output_directory, filename, annotated_mapping, raise_on_diff):
    if not raise_on_diff:
        return
    filepath = Path(output_directory, filename).resolve()
    if not filepath.is_file():
        raise UnexpectedMappingError(
            f'{filepath} not found. Have you generated latest mappings?'
        )
    with open(filepath) as f:
        existing_mapping = json.load(f)
    for k, v in annotated_mapping.items():
        actual = existing_mapping.get(k)
        expected = v
        if actual != expected:
            raise UnexpectedMappingError(
                f'Found {k} {actual} in {filepath}, expected {expected}. Have you generated latest mappings?'
            )


def write_annotated_mappings(annotated_mappings, relative_output_directory, raise_on_diff):
    current_directory = os.path.dirname(__file__)
    output_directory = Path(current_directory, relative_output_directory)
    for annotated_mapping in annotated_mappings:
        filename = f'{annotated_mapping["item_type"]}.json'
        maybe_raise_on_diff(
            output_directory=output_directory,
            filename=filename,
            annotated_mapping=annotated_mapping,
            raise_on_diff=raise_on_diff
        )
        with open(Path(output_directory, filename), 'w') as f:
            print(f'Writing {filename}')
            json.dump(
                annotated_mapping,
                f,
                sort_keys=True,
                indent=4,
            )
            # Always add newline at EOF.
            f.write('\n')


def annotate_mappings(indices, mappings):
    annotated_mappings = []
    for index in indices:
        mapping = mappings[index]
        mapping_hash = hashlib.md5(
            json.dumps(
                mapping,
                sort_keys=True
            ).encode('utf-8')
        ).hexdigest()
        annotated_mappings.append(
            {
                'item_type': index,
                'hash': mapping_hash,
                'index_name': f'{index}_{mapping_hash[:8]}',
                'mapping': mapping,
            }
        )
    return annotated_mappings


def generate_and_write_mappings(app, relative_output_directory, raise_on_diff=False):
    indices, mappings = generate_indices_and_mappings(app)
    annotated_mappings = annotate_mappings(indices, mappings)
    write_annotated_mappings(
        annotated_mappings=annotated_mappings,
        relative_output_directory=relative_output_directory,
        raise_on_diff=raise_on_diff
    )


def get_args():
    import argparse
    parser = argparse.ArgumentParser(
        description='Generate Opensearch Mappings'
    )
    parser.add_argument(
        '--app-name',
        help='Pyramid app name in configfile'
    )
    parser.add_argument(
        '--relative-output-directory',
        help='Directory to write mappings'
    )
    parser.add_argument(
        'config_uri',
        help='path to configfile'
    )
    parser.add_argument(
        '--raise-on-diff',
        action='store_true'
    )
    return parser.parse_args()


def main():
    args = get_args()
    app = get_app(
        args.config_uri,
        args.app_name
    )
    generate_and_write_mappings(
        app=app,
        relative_output_directory=args.relative_output_directory,
        raise_on_diff=args.raise_on_diff,
    )


if __name__ == '__main__':
    main()
