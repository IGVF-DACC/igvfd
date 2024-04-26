## Changelog for *`document.json`*

### Minor changes since schema version 4

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
