## Changelog for document.json

### Minor changes since schema version 1

* *document_type* property enum list was expanded to include:
    "enum": [
        "characterization",
        "computational protocol",
        "experimental protocol",
        "file format specification",
        "image",
        "plasmid map",
        "standards"
    ]
* *characterization_method* property was added:
    "enum": [
        "FACS",
        "immunoblot",
        "immunofluorescence",
        "immunoprecipitation",
        "mass spectrometry",
        "PCR",
        "restriction digest",
        "RT-qPCR",
        "sequencing"
    ]
* document has aliases mixin and submitted mixin removed, but still has properties for aliases and submitted due to change of basic_item mixin.  The actual properties have not changed.
