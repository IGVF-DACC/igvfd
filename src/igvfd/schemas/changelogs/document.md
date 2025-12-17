## Changelog for *`document.json`*

### Minor changes since schema version 4

* Extend `document_type` enum list to include `cell marker file`.
* Extend `document_type` enum list to include `tile coordinates`.
* Extend `document_type` enum list to include `ontology term reference`.
* Extend `document_type` enum list to include `pipeline log`.
* Extend `document_type` enum list to include `pipeline parameters`.
* Add `preview_timestamp`.
* Add `standardized_file_format`.
* Extend `document_type` enum list to include `library structure seqspec`.
* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.
* Extend `status` enum list to include `preview`.
* Extend `document_type` enum list to include `quality control report`.
* Extend `document_type` enum list to include `model source data`.
* Extend `document_type` enum list to include `plate map`.

### Schema version 4

* Require `release_timestamp` for any objects with `released` or `archived` status.

### Minor changes since schema version 3

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `release_timestamp`.
* Add `plasmid sequence` as `document_type`.
* Add `archived` to `status`.

### Schema version 3

* Disallow empty strings in `description`.

### Minor changes since schema version 2

* Expand `document_type` enum list to include `cell fate change protocol`.

### Schema version 2

* Restrict `aliases` and `urls` to be a non-empty array with at least one item.

### Minor changes since schema version 1

* Add `characterization_method`.
* Remove from `document_type` enums:
    ```json
    "general protocol"
    ```
* Expand `document_type` enum list to include:
    ```json
    "enum": [
        "characterization",
        "computational protocol",
        "experimental protocol",
        "file format specification",
        "image",
        "plasmid map",
        "standards"
    ]
    ```
