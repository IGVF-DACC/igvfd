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
    'query',
]

RESERVED_KEYS = NOT_FILTERS = OPTIONAL_PARAMS + FREE_TEXT_QUERIES

TOP_HITS_ITEM_TYPES = [
    'Award',
    'Biomarker',
    'Document',
    'HumanDonor',
    'RodentDonor',
    'AlignmentFile',
    'ConfigurationFile',
    'ReferenceFile',
    'SequenceFile',
    'SignalFile',
    'MatrixFile',
    'AnalysisSet',
    'ConstructLibrarySet',
    'CuratedSet',
    'MeasurementSet',
    'Model',
    'ModelSet',
    'AuxiliarySet',
    'Prediction',
    'PredictionSet',
    'Gene',
    'Image',
    'Lab',
    'Modification',
    'AssayTerm',
    'PhenotypeTerm',
    'PlatformTerm',
    'SampleTerm',
    'Page',
    'Workflow',
    'AnalysisStep',
    'PhenotypicFeature',
    'Publication',
    'InVitroSystem',
    'PrimaryCell',
    'Tissue',
    'WholeOrganism',
    'TechnicalSample',
    'MultiplexedSample',
    'Software',
    'SoftwareVersion',
    'Source',
    'Treatment',
    'User',
    'HumanGenomicVariant'
]

DEFAULT_ITEM_TYPES = TOP_HITS_ITEM_TYPES

# Top_hits_item_types interact with the search box
# Default item types would be searchable using ?searchTerm=ABC format in the url without having to use &type=Item
