from snovault.elasticsearch.searches.configs import search_config


@search_config(
    name='ConstructLibrarySet'
)
def construct_library_set():
    return {
        'facets': {
            'award.component': {
                'title': 'Award'
            },
            'lab.title': {
                'title': 'Lab'
            },
            'file_set_type': {
                'title': 'File Set Type'
            },
            'scope': {
                'title': 'Scope'
            },
            'selection_criteria': {
                'title': 'Selection Criteria'
            },
            'collections': {
                'title': 'Collections',
            },
            'status': {
                'title': 'Status'
            }
        },
        'facet_groups': [
            {
                'title': 'File Set',
                'facet_fields': [
                    'file_set_type',
                    'selection_criteria',
                    'scope',
                ],
            },
            {
                'title': 'Provenance',
                'facet_fields': [
                    'collections',
                    'lab.title',
                    'award.component',
                ],
            },
            {
                'title': 'Quality',
                'facet_fields': [
                    'status',
                ],
            },
        ],
        'columns': {
            'accession': {
                'title': 'Accession'
            },
            'aliases': {
                'title': 'Aliases'
            },
            'status': {
                'title': 'Status'
            },
            'lab': {
                'title': 'Lab'
            },
            'file_set_type': {
                'title': 'File Set Type'
            },
            'scope': {
                'title': 'Scope'
            },
            'selection_criteria': {
                'title': 'Selection Criteria'
            },
            'alternate_accessions': {
                'title': 'Alternate Accessions'
            }
        }
    }
