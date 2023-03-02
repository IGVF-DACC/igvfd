from opensearchpy import OpenSearch


def mabye_migrate_from_old_to_new_opensearch_indices(opensearch_url):
    os = OpenSearch(opensearch_url)
    if not os.indices.exists_alias('award'):
        # Old-style index award was not an alias.
        os.indices.delete('*')


def get_args():
    parser = argparse.ArgumentParser(
        description='Maybe migrate from old-style to new-style Opensearch indices.'
    )
    parser.add_argument(
        '--opensearch-url',
        help='Opensearch URL'
    )
    return parser.parse_args()


def main():
    args = get_args()
    maybe_migrate_from_old_to_new_opensearch_indices(args.opensearch_url)


if __name__ == '__main__':
    main()
