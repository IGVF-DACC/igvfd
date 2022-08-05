## Changelog for *`document.json`*

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
