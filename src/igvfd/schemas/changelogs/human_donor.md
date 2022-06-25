## Changelog for human_donor.json

### Minor changes since version 1

* *taxon_id* now restricted to NCBI taxonomy ids that start with NCBI:txid followed by numbers. Example NCBI:txid9606 for *Homo sapiens*
* *taxon_id* replaced by organism
* Defined *sex* as required property and defaulted it to *unspecified*
* *human_donor* has *aliases* mixin and *submitted* mixin removed, but still has properties for *aliases* and *submitted* due to change of basic_item mixin.  The actual properties have not changed.
* *organism* property renamed to *taxa*
* Donors now have a property *traits* to specify known phenotypic traits
