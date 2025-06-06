## Changelog for *`platform_term.json`*

### Minor changes since schema version 5

* Add `preview_timestamp`.

### Schema version 5

* Add calculated `comment`.
* Add calculated `definition`.
* Remove `comment`.
* Remove `definition`.

### Minor changes since schema version 4

* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.
* Add `comment`.
* Add `definition`.
* Extend `company` enum list to include `Element Biosciences`.
* Extend `sequencing_kits` enum list to include `AVITI 2x75 Sequencing Kit Cloudbreak High Output`.
* Extend `sequencing_kits` enum list to include `AVITI 2x150 Sequencing Kit Cloudbreak High Output`.
* Extend `status` enum list to include `preview`.
* Extend `company` enum list to include `Singular Genomics`.
* Extend `sequencing_kits` enum list to include `Singular G4 F2 Reagent Kit`.
* Extend `sequencing_kits` enum list to include `NovaSeq X Series 1.5B Reagent Kit`.
* Extend `sequencing_kits` enum list to include `NovaSeq X Series 25B Reagent Kit`.
* Update calculation of `summary`.

### Schema version 4

* Adjust `sequencing_kits` enum list to replace `NovaSeq 6000 S4 Reagent Kit V1.5` with `NovaSeq 6000 S4 Reagent Kit v1.5`.

### Minor changes since schema version 3

* Add `sequencing_kits`.

### Schema version 3

* Require `release_timestamp` for any objects with `released` or `archived` status

### Minor changes since schema version 2

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `release_timestamp`.
* Add `archived` to `status`.

### Schema version 2

* Disallow empty strings in `description`.

### Minor changes since schema version 1

* Add calculated property `ontology`.
* Add `company`.
