## Changelog for *`page.json`*

### Schema version 4

* Disallow empty strings in `description`.

### Schema version 3

* Remove `news`, `news_keywords`, and `news_excerpt` properties.
* Remove the `rows` property from the `layout` dictionary.
* Remove any `layout.block` elements that don't have an `@type` of `richtextblock`.
* Change all remaining `layout.block` elements to an `@type` of `markdown`.
* Add a `direction` property to each `layout.block`.
* Enforce only defined schema properties allowed to be posted to the database in the `layout` and `layout.blocks` properties.

### Minor changes since schema version 2

* Add `description`.
* Add `aliases` to `identifyingProperties`.

### Schema version 2

* Restrict `aliases` and `news_keywords` to be a non-empty array with at least one item.

### Minor changes since schema version 1

* Add `aliases`.
