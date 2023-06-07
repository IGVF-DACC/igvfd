## Search FAQ

### Fuzzy and exact search values:

**Q: Why do we define 'fuzzy_searchable_fields' and 'exact_searchable_fields' in an item's schema?**

A: Opensearch takes the document we give it and copies some values into a field called `_fuzzy` and some values into a field called `_exact`. When you search with a `searchTerm=` or `query=` parameter, the value is compared to values in the `_fuzzy` or `_exact` fields to find documents that contain your query. The main difference between these fields is that Opensearch tokenizes the values copied into the `_fuzzy` field with `ngram` and `English stemming` analyzers, while the `_exact` field stores the exact (lowercase) value:

* `_fuzzy`: a value like `User` will get transformed and stored into something like `[u, us, use, user]`
* `_exact`: a value like `User` will get transformed and stored as `[user]`

 Both `?query=us` and `?query=Users` would fuzzy match the document, while only `?query=User` or `?query=user` would exact match the document.

**Q: Which fields should be fuzzy and which fields should be exact?**

A: Consider if partial matches of the value would be useful. Adding values to '_fuzzy' can create a lot of nonspecific tokens which could make search results less relevant. Things like UUID, @id, accessions, and unique identifiers probably make sense in our system. For example you probably either have a full UUID or nothing, so the overhead of fuzzy matching wouldn't be especially useful.

**Q: Can I still search for the exact value if it's not included in `exact_searchable_fields`?**

A: Yes, you can always search for exact values if you know the field that you want to use, even on fields that aren't included in either 'fuzzy_searchable_fields' or 'exact_searchable_fields':

* `?uuid=1e75d989-a438-4d77-a451-8a297fd3636e`
* `?status=released`

**Q: Why are certain terms, like `UUID`, searchable by default?**

A: Certain high-level document values, such as UUIDs and unique keys, are copied by default into the `_exact` field in Opensearch. You can look at the mapping for a type to see if a specific field is copied into `_exact` or `_fuzzy` fields.

### Search configs:

**Q: What are search configs?**

A: Search configs are collections of values that our search system can use at search time to dynamically render search results. These values include the columns (or fields) that should be returned and the facets that should be calculated. By default the search config for a type is used implicitly, but you can also specify explicit configs in the query string like `?type=Award&config=CustomConfig`. This is especially useful for creating dynamic views of different combinations of item types, with varying facets, aggregations, return fields, etc.

**Q: How do you mix and match search configs?**

A: You can mix and match search configs explicitly by specifying one or more search config names in your query string: `?type=Award&config=CustomConfig&config=CustomConfig2`. Usually all of the values from specified configs are combined to determine the final value.

### Search defaults:

**Q: What are DEFAULT_ITEM_TYPES?**

A: Usually a search will have an explicit `type` defined in the query string (e.g. '?type=Award`). [`DEFAULT_ITEM_TYPES`](https://github.com/IGVF-DACC/igvfd/blob/b3714678fb6695a97a544eecb0afe403cdf149c9/src/igvfd/searches/defaults.py#L22-L60) is a list of item types (and corresponding Opensearch indices) that the system will search over when none are specified in the query string. These are particularly useful in queries where a `searchTerm` or `query` is specified without any types.
