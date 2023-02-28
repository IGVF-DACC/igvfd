import hashlib

import json

import os

from pathlib import Path

from pyramid.paster import get_app

from snovault.elasticsearch.create_mapping import generate_indices_and_mappings


def generate_mappings(app):
    indices, mappings = generate_indices_and_mappings(app)
    print(indices, mappings.keys())
    current_directory = os.path.dirname(__file__)
    relative_path_to_output_directory = '../mappings'
    output_directory = Path(current_directory, relative_path_to_output_directory)
    for index in indices:
        filename = f'{index}.json'
        with open(Path(output_directory, filename), 'w') as f:
            print(f'Writing {filename}')
            mapping = mappings[index]
            mapping_hash = hashlib.md5(
                json.dumps(
                    mapping,
                    sort_keys=True
                ).encode('utf-8')
            ).hexdigest()
            json.dump(
                {
                    'name': index,
                    'hash': mapping_hash,
                    'index_name': f'{index}_{mapping_hash[:8]}',
                    'mapping': mapping,
                },
                f,
                sort_keys=True,
                indent=4,
            )
            # Always add newline at EOF.
            f.write('\n')


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
        '--out-directory',
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
    generate_mappings(app)


if __name__ == '__main__':
    main()
