OPTIONAL_PARAMS = [
    'datastore',
    'debug',
    'field',
    'format',
    'frame',
    'from',
    'limit',
    'mode',
    'sort',
    'type',
    'config',
]

FREE_TEXT_QUERIES = [
    'advancedQuery',
    'searchTerm',
]

RESERVED_KEYS = NOT_FILTERS = OPTIONAL_PARAMS + FREE_TEXT_QUERIES

TOP_HITS_ITEM_TYPES = [
    'HumanDonor',
    'RodentDonor',
    'AlignmentFile',
    'ReferenceFile',
    'SequenceFile',
    'SignalFile',
    'AnalysisSet',
    'CuratedSet',
    'MeasurementSet',
    'Gene',
    'Lab',
    'AssayTerm',
    'PhenotypeTerm',
    'PlatformTerm',
    'SampleTerm',
    'Page',
    'Publication',
    'InVitroSystem',
    'PrimaryCell',
    'TechnicalSample',
    'Tissue',
    'WholeOrganism',
    'Source',
    'Treatment',
    'User'
]

DEFAULT_ITEM_TYPES = TOP_HITS_ITEM_TYPES + [
    'Award',
    'Biomarker',
    'Document',
    'ConstructLibrary',
    'Image',
    'PhenotypicFeature',
    'HumanGenomicVariant'
]
