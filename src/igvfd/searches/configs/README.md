# Facet type examples

## Terms

Shows count of values in a field.

Input:
```python
{
    'facets': {
        'status': {
	     'title': 'Status'
	     'type': 'terms' # Default, optional.
	}
    }
}
```

Output:
```json
{
    "field": "status",
    "title": "Status",
    "terms": [
        {
            "key": "released",
            "doc_count": 13037
        },
        {
            "key": "preview",
            "doc_count": 4832
        },
        {
            "key": "archived",
            "doc_count": 8
        },
        {
            "key": "revoked",
            "doc_count": 5
        }
  ],
  "total": 17882,
  "type": "terms",
  "appended": false,
  "open_on_load": false
}
```

## Exists

Shows count of documents where field exists or not.

Input:
```python
{
    'facets': {
        'nih_institutional_certification': {
	    'title':  'Has NIH institutional certification',
	    'type': 'exists'
	}
    }
}
```

Output:
```json
{
    "field": "nih_institutional_certification",
    "title": "Has NIH institutional certification",
    "terms": [
        {
            "key": "no",
            "doc_count": 19243
        },
        {
            "key": "yes",
            "doc_count": 7524
        }
    ],
    "total": 26767,
    "type": "exists",
    "appended": false,
    "open_on_load": false
}
```

## Stats

Shows summary statistics for numerical field.

Input:
```python
{
    'facets': {
        'file_size', {
	    'title': 'File size statistics',
	    'type': 'stats'
	}
    }
}
```

Output:
```json
{
    "field": "file_size",
    "title": "File size statistics",
    "terms": {
        "count": 161,
        "min": 1,
        "max": 473944998854,
        "avg": 3642979032.757764,
        "sum": 586519624274
     },
    "total": 161,
    "type": "stats",
    "appended": false,
    "open_on_load": false
}
```

## Hierarchical

Shows nested terms facets. Can have as many subfacets as you want.

Input:
```python
{
    'facets': {
        'samples.classifications', {
            'title': 'Sample classifications',
            'type': 'hierarchical',
            'subfacets': [
                {
                    'field': 'samples.sample_terms.term_name',
                    'title': 'Sample term name',
                }
            ]
        }
    }
}
```

Output:
```json
{
    "field": "samples.classifications",
    "title": "Sample classifications",
    "terms": [
        {
            "key": "primary cell",
            "doc_count": 14,
            "subfacet": {
                "field": "samples.sample_terms.term_name",
                "title": "Sample term name",
                "terms": [
                    {"key": "motor neuron", "doc_count": 14}
                ]
            }
        },
        {
            "key": "multiplexed sample",
            "doc_count": 6,
            "subfacet": {
                "field": "samples.sample_terms.term_name",
                "title": "Sample term name",
                "terms": [
                    {"key": "motor neuron", "doc_count": 6}
                ]
            }
        },
        {
            "key": "cell line",
            "doc_count": 3,
            "subfacet": {
                "field": "samples.sample_terms.term_name",
                "title": "Sample term name",
                "terms": [
                    {"key": "motor neuron", "doc_count": 3}
                ]
            }
        },
        {
            "key": "whole organism",
            "doc_count": 2,
            "subfacet": {
                "field": "samples.sample_terms.term_name",
                "title": "Sample term name",
                "terms": [
                    {"key": "whole organism", "doc_count": 2}
                ]
            }
        },
        {
            "key": "technical sample",
            "doc_count": 1,
            "subfacet": {
                "field": "samples.sample_terms.term_name",
                "title": "Sample term name",
                "terms": [
                    {"key": "technical sample", "doc_count": 1}
                ]
            }
        },
        {
            "key": "tissue",
            "doc_count": 1,
            "subfacet": {
                "field": "samples.sample_terms.term_name",
                "title": "Sample term name",
                "terms": [
                    {"key": "lung", "doc_count": 1}
                ]
            }
        }
    ],
    "total": 27,
    "type": "hierarchical",
    "appended": false,
    "open_on_load": false
}
```

## Date histogram

Shows count by date field. Can customize calendar interval (i.e. day/month/year) and date format (i.e. yyyy-MM-dd).

Input:
```python
{
    'facets': {
        'release_timestamp': {
            'title': 'Release timestamp',
            'type': 'date_histogram',
            'calendar_interval': 'month',
            'format': 'yyyy-MM-dd',
        }
    }
}

```

Output:
```json
{
    "field": "release_timestamp",
    "title": "Release timestamp",
    "terms": [
        {"key_as_string": "04-03-2024", "key": 1709510400000, "doc_count": 19},
        {"key_as_string": "11-03-2024", "key": 1710115200000, "doc_count": 0},
        {"key_as_string": "18-03-2024", "key": 1710720000000, "doc_count": 0},
        {"key_as_string": "25-03-2024", "key": 1711324800000, "doc_count": 0},
        {"key_as_string": "01-04-2024", "key": 1711929600000, "doc_count": 0},
        {"key_as_string": "08-04-2024", "key": 1712534400000, "doc_count": 0},
        {"key_as_string": "15-04-2024", "key": 1713139200000, "doc_count": 0},
        {"key_as_string": "22-04-2024", "key": 1713744000000, "doc_count": 0},
        {"key_as_string": "29-04-2024", "key": 1714348800000, "doc_count": 0},
        {"key_as_string": "06-05-2024", "key": 1714953600000, "doc_count": 0},
        {"key_as_string": "13-05-2024", "key": 1715558400000, "doc_count": 0},
        {"key_as_string": "20-05-2024", "key": 1716163200000, "doc_count": 0},
        {"key_as_string": "27-05-2024", "key": 1716768000000, "doc_count": 0},
        {"key_as_string": "03-06-2024", "key": 1717372800000, "doc_count": 1},
        {"key_as_string": "10-06-2024", "key": 1717977600000, "doc_count": 0},
        {"key_as_string": "17-06-2024", "key": 1718582400000, "doc_count": 0},
        {"key_as_string": "24-06-2024", "key": 1719187200000, "doc_count": 0},
        {"key_as_string": "01-07-2024", "key": 1719792000000, "doc_count": 4},
        {"key_as_string": "08-07-2024", "key": 1720396800000, "doc_count": 0},
        {"key_as_string": "15-07-2024", "key": 1721001600000, "doc_count": 0},
        {"key_as_string": "22-07-2024", "key": 1721606400000, "doc_count": 0},
        {"key_as_string": "29-07-2024", "key": 1722211200000, "doc_count": 0},
        {"key_as_string": "05-08-2024", "key": 1722816000000, "doc_count": 0},
        {"key_as_string": "12-08-2024", "key": 1723420800000, "doc_count": 0},
        {"key_as_string": "19-08-2024", "key": 1724025600000, "doc_count": 0},
        {"key_as_string": "26-08-2024", "key": 1724630400000, "doc_count": 0},
        {"key_as_string": "02-09-2024", "key": 1725235200000, "doc_count": 0},
        {"key_as_string": "09-09-2024", "key": 1725840000000, "doc_count": 0},
        {"key_as_string": "16-09-2024", "key": 1726444800000, "doc_count": 0},
        {"key_as_string": "23-09-2024", "key": 1727049600000, "doc_count": 0},
        {"key_as_string": "30-09-2024", "key": 1727654400000, "doc_count": 0},
        {"key_as_string": "07-10-2024", "key": 1728259200000, "doc_count": 3}
    ],
    "total": 27,
    "type": "date_histogram",
    "appended": false,
    "open_on_load": false
}
```

## Range

Shows count by custom ranges on numercial fields.

Input:
```python
{
    'facets': {
        'lower_bound_age_in_hours', {
             'title': 'Lower bound age in hours',
             'type': 'range',
             'ranges': [
                 {'to': 1000.0},
                 {'from': 1000.0, 'to': 10000.0},
                 {'from': 10000.0}
             ]
        }
    }
}
```

Output:
```json
{
    "field": "lower_bound_age_in_hours",
    "title": "Lower bound age in hours",
    "terms": [
        {"key": "*-1000.0", "to": 1000.0, "doc_count": 3},
        {"key": "1000.0-10000.0", "from": 1000.0, "to": 10000.0, "doc_count": 2},
        {"key": "10000.0-*", "from": 10000.0, "doc_count": 1}
    ],
    "total": 7,
    "type": "range",
    "appended": false,
    "open_on_load": false
}
```

Note that you can also put named keys in the range specification:

```python
{
    'facets': {
        'file_size': {
            'title': 'File size',
            'type': 'range',
            'ranges': [
                {'key': 'small', 'to': 30000000},
                {'key': 'medium', 'from': 30000000, 'to': 50000000},
                {'key': 'large', 'from': 50000000},
            ]
        }
    },
}
