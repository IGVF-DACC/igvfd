import hashlib

import json

import os

from pathlib import Path

from pyramid.paster import get_app

from snovault.elasticsearch.create_mapping import generate_indices_and_mappings


def write_annotated_mappings(annotated_mappings, relative_output_directory):
    current_directory = os.path.dirname(__file__)
    output_directory = Path(current_directory, relative_output_directory)
    for annotated_mapping in annotated_mappings:
        filename = f'{annotated_mapping["item_type"]}.json'
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


def generate_and_write_mappings(app, output_directory):
    indices, mappings = generate_indices_and_mappings(app)
    annotated_mappings = annotate_mappings(indices, mappings)
    write_annotated_mappings(annotated_mappings, output_directory)


def main():
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
    args = parser.parse_args()
    app = get_app(
        args.config_uri,
        args.app_name
    )
    generate_and_write_mappings(
        app=app,
        output_directory=args.relative_output_directory
    )


if __name__ == '__main__':
    main()
