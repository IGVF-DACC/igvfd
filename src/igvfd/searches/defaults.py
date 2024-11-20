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
    'ModelFile',
    'TabularFile',
    'GenomeBrowserAnnotationFile',
    'ImageFile',
    'IndexFile',
    'InstitutionalCertificate',
    'AnalysisSet',
    'ConstructLibrarySet',
    'CuratedSet',
    'MeasurementSet',
    'ModelSet',
    'AuxiliarySet',
    'PredictionSet',
    'Gene',
    'OpenReadingFrame',
    'Image',
    'Lab',
    'CrisprModification',
    'DegronModification',
    'Modification',
    'AssayTerm',
    'PhenotypeTerm',
    'PlatformTerm',
    'SampleTerm',
    'Page',
    'Workflow',
    'AnalysisStep',
    'AnalysisStepVersion',
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
    'User'
]

DEFAULT_ITEM_TYPES = TOP_HITS_ITEM_TYPES

# Top_hits_item_types interact with the search box
# Default item types would be searchable using ?searchTerm=ABC format in the url without having to use &type=Item
