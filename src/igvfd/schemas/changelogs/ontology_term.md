## Changelog for *`ontology_term.json`*

* Objects with released or archived status without `release_timestamp` are now automatically updated to have `release_timestamp` `2024-03-06T12:34:56Z`. (03/06/2024)
* Add `archived` to `status`. (03/05/2024)
* Add `release_timestamp`. (01/31/2024)
* Add calculated property `ontology`. (06/07/2023)
* Add `description`. (02/08/2023)
* Restrict `aliases` to be a non-empty array with at least one item. (02/08/2023)
* Add calculated properties `assay_slims` and `objective_slims`. (02/08/2023)
* Rename schema `term.json` to `ontology_term.json`. (02/08/2023)
* Rename schema `ontology_term.json` to `term.json`. (02/08/2023)
* Add `submitter_comment`, `submitted_by` and `creation_timestamp`. (02/08/2023)
