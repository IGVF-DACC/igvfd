## Changelog for rodent_donor.json

### Minor changes since version 1

* *taxon_id* now restricted to NCBI taxonomy ids that start with NCBI:txid followed by numbers. Example NCBI:txid10090 for *Mus musculus*
* *taxon_id* replaced by organism
* defined *sex* as required property and defaulted it to *unspecified*
* rodent_donor has aliases mixin and submitted mixin removed, but still has properties for aliases and submitted due to change of basic_item mixin.  The actual properties have not changed.
* organism property renamed to taxa
* Rodent donors now have a property *traits* to specify known phenotypic traits.
