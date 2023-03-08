import pytest
import json
from igvfd.audit.compare_dict_values import (
    compare_dictionary
)


def test_compare_dictionary(testapp):
    test_value_one_json = """
    {
        "accession": "IGVFSM0366ILTA",
        "aliases": [
            "hyejung-won:muscle_sample1"
        ],
        "award": "/awards/HG012003/",
        "biosample_term": "/sample-terms/UBERON_0001630/",
        "creation_timestamp": "2022-07-28T01:58:59.897673+00:00",
        "donors": [
            "/rodent-donors/IGVFDO0930TRKA/"
        ],
        "lab": "/labs/hyejung-won/",
        "schema_version": "9",
        "source": "/sources/hyejung-won/",
        "status": "released",
        "submitted_by": "/users/6bae687f-b77a-46b9-af0e-a02c135cf42e/",
        "taxa": "Mus musculus",
        "disease_terms": "Alzheimer disease"
    }
    """
    test_value_two_json = """
    {
        "accession": "IGVFSM0834IWLA",
        "aliases": [
            "hyejung-won:brain_sample1_treated"
        ],
        "award": "/awards/HG012003/",
        "biosample_term": "/sample-terms/UBERON_0000955/",
        "creation_timestamp": "2022-07-28T01:59:00.635826+00:00",
        "donors": [
            "/rodent-donors/IGVFDO0930TRKA/"
        ],
        "lab": "/labs/hyejung-won/",
        "schema_version": "9",
        "source": "/sources/hyejung-won/",
        "status": "released",
        "submitted_by": "/users/6bae687f-b77a-46b9-af0e-a02c135cf42e/",
        "treatments": [
            "/treatments/bc321be7-9c85-4b0c-b5dc-3e870fbd6b3c/"
        ],
        "disease_terms": [
            "/disease_terms/ba321be7-9c85-4b0c-b5dc-3e870fbd6b3c/"
        ]
    }
    """
    # parse json string to data
    test_value_one = json.loads(test_value_one_json)
    test_value_two = json.loads(test_value_two_json)
    # item list to not compare in dictionaries
    items_to_not_compare = [
        '@context',
        '@id',
        '@type',
        'accession',
        'aliases',
        'audit',
        'creation_timestamp',
        'date_obtained',
        'schema_version',
        'starting_amount',
        'starting_amount_units',
        'status',
        'submitted_by',
        'summary',
        'uuid']
    # call to compare dictionaries
    differences = compare_dictionary(
        test_value_one,
        test_value_two,
        items_to_not_compare)

    assert len(differences) == 4
    assert differences[0] == 'biosample_term'
    assert differences[1] == 'taxa'
    assert differences[2] == 'disease_terms'
    assert differences[3] == 'treatments'
