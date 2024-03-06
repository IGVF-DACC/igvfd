## Changelog for *`model.json`*

### Schema version 4

* Objects with released, archived or revoked status without `release_timestamp` are now automatically updated to have `release_timestamp` `2024-03-06T12:34:56Z`.

### Minor changes since schema version 3

* Restrict `lab` and `award` to submittable by admins only. No further submission of models are accepted, please submit model sets instead.
* Deprecate `model` schema.
* Add `release_timestamp`.

### Schema version 3

* Rename `model_type` to `file_set_type`.

### Schema version 2

* Rename `references` to `publication_identifiers`.
