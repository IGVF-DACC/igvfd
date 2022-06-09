## Changelog for mixins.json

### Changes since schema version 1

* 3/24/22 Added product_id, lot_id, source mixins
* 4/5/22 Added additional_description mixin
* 4/7/22 Added product_id, lot_id, source mixins to a set called product_info
* 4/27/22 Added collections
* changed the property *date_created* into *creation_timestamp* and restricted the format to be date-time
* removed mixins for aliases and submitted.  All properies for aliases and submitted have been moved under the basic_item mixin.  All schema objects that include the basic_item mixin will also have the properties previously in aliases and submitted.
