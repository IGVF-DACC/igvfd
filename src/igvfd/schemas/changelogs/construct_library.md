## Changelog for *`construct_library.json`*

### Schema version 4
<<<<<<< HEAD
* Rename `origins` to `selection_criteria`.
=======

* Rename `references` to `publication_identifiers`.
>>>>>>> 08990ced (replacement upgrade)

### Schema version 3

* Require `origins` and one of the three library details sub-objects: `expression_vector_library_details`, `guide_library_details`, `reporter_library_details`.

### Minor changes since schema version 2

* Add `files`.
* Add `integrated_content_files`.
* Add `expression_vector_library_details`.
* Add `control_for`.

### Schema version 2

* Remove `plasmid_map`. Use `documents` instead.

### Minor changes since schema version 1

* Add `disease-associated variants` to `origins`, to be used with additional property `associated_diseases`.
