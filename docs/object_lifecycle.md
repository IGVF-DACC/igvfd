# The object lifecycle

# GET

Data can be retrieved from the database in one of a few `frames` which specify how much data is in the returned object.

* `frame=raw`

Objects are stored in the DB raw, with only submitted properties and `UUIDs` as links.

* `frame=object`

This is the raw object with `UUIDs` converted to `@ids` and calculated properties.

* `frame=edit`

This is the frame=object without calculated properties.

* `frame=embedded`

This is the `frame=object` object with all the embedded properties.

* `frame=page`

This is the default object returned if frame is not specified. It is the `frame=embedded` object with several form properties added including @context, audit, and actions.

# POST

POST /biosample:

```json
{
    "biosample_type": "DNA",
    "biosample_term_id": "UBERON:349829",
    "aliases": ["my-lab:sample1"],
    "award": "my-award",
    "lab": "my-lab",
    "source": "some-source",
    "organism": "human"
}
```

## Validation

* Structural conformance
* Link resolution
* Value format validation
* Permission checking


## Link resolution

Links are resolved relative to their configured base URL, normally their collection.
Absolute paths and UUIDs are also valid, as are aliases and other uniquely identifying properties:

```json
{
    "award": "fae1bd8b-0d90-4ada-b51f-0ecc413e904d",
    "lab": "b635b4ed-dba3-4672-ace9-11d76a8d03af",
    "source": "1d5be796-8f80-4fd4-b6c7-6674318657eb",
    "organism": "7745b647-ff15-4ff3-9ced-b897d4e2983c"
}
```

## Default values

Static and calculated defaults:

```json
{
    "uuid": "7c245cea-7d59-45fb-9ebe-f0454c5fe950"
    "accession": "ENCBS000TST",
    "date_created": "2014-01-20T10:30:00-0800",
    "status": "in progress",
    "submitted_by": "bb319896-3f78-4e24-b6e1-e4961822bc9b"
}
```

## Storage

Resource record created for UUID with item_type:

```
uuid: "7c245cea-7d59-45fb-9ebe-f0454c5fe950"
item_type: "biosample"
```

`raw` properties:

```json
{
    "biosample_type": "DNA",
    "biosample_term_id": "UBERON:349829",
    "aliases": ["my-lab:sample1"],
    "award": "fae1bd8b-0d90-4ada-b51f-0ecc413e904d",
    "lab": "b635b4ed-dba3-4672-ace9-11d76a8d03af",
    "source": "1d5be796-8f80-4fd4-b6c7-6674318657eb",
    "organism": "7745b647-ff15-4ff3-9ced-b897d4e2983c",
    "accession": "ENCBS000TST",
    "date_created": "2014-01-20T10:30:00-0800",
    "status": "in progress",
    "submitted_by": "bb319896-3f78-4e24-b6e1-e4961822bc9b"
}
```

Rows are inserted to enforce unique constraints:

```
keys: [
    ("accession", "ENCBS000TST"),
    ("alias", "my-lab:sample1"),
]
```

And to maintain referential integrity:

```
links: [
    ("award", "fae1bd8b-0d90-4ada-b51f-0ecc413e904d"),
    ("lab", "b635b4ed-dba3-4672-ace9-11d76a8d03af"),
    ("source", "1d5be796-8f80-4fd4-b6c7-6674318657eb"),
    ("organism", "7745b647-ff15-4ff3-9ced-b897d4e2983c"),
    ("submitted_by", "bb319896-3f78-4e24-b6e1-e4961822bc9b"),
]
```

# Rendering

```
* raw properties
  -> link canonicalization
    -> calculated properties
      -> embedding
        -> page expansion
```


# Link canonicalization

Specified in the schema. UUIDs are converted to resource paths.

```json
{
    "award": "/awards/my-award/",
    "lab": "/labs/my-lab",
    "source": "/sources/some-source/",
    "organism": "/organisms/human/",
    "submitted_by": "/users/me/",
}
````

# Calculated properties

These include the JSON-LD boilerplate along with other dynamically calculated properties such as a consistently formatted titles and reverse links pulled from the links table.
```json
{
    "@id": "/biosamples/ENCBS000TST/",
    "@type": ["biosample", "item"],
    "uuid": "7c245cea-7d59-45fb-9ebe-f0454c5fe950"
    "name": "ENCBS000TST",
    "title": "Biosample ENCBS000TST (human)",
    "characterizations": [],
}
```

# JSON result

Combining gives us:
```json
{
    "biosample_type": "DNA",
    "biosample_term_id": "UBERON:349829",
    "aliases": ["my-lab:sample1"],
    "accession": "ENCBS000TST",
    "date_created": "2014-01-20T10:30:00-0800",
    "status": "in progress",
    "award": "/awards/my-award/",
    "lab": "/labs/my-lab",
    "source": "/sources/some-source/",
    "organism": "/organisms/human/",
    "submitted_by": "/users/me/",
    "@id": "/biosamples/ENCBS000TST/",
    "@type": ["biosample", "item"],
    "uuid": "7c245cea-7d59-45fb-9ebe-f0454c5fe950"
    "name": "ENCBS000TST",
    "title": "Biosample ENCBS000TST (human)",
    "characterizations": [],
}
```

This is the representation returned within the POST/PUT/PATCH result when specifying `frame=object`.


# Embedding

Each object type specifies its embedded properties. The specified links are then replaced with objects when using `frame=embedded`.


# Page expansion

The final step in the rendering pipeline is applied only to single items, not to search results. It provides the opportunity to add properties that are restricted or tailored to certain users, such as the actions and audit results.
