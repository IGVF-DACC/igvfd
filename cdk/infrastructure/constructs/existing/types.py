from infrastructure.constructs.existing.igvf_dev import Resources as IGVFDevResources
from infrastructure.constructs.existing.igvf_staging import Resources as IGVFStagingResources
from infrastructure.constructs.existing.igvf_sandbox import Resources as IGVFSandboxResources
from infrastructure.constructs.existing.igvf_prod import Resources as IGVFProdResources

from typing import Union

from typing import Type


ExistingResources = Union[
    IGVFDevResources,
    IGVFStagingResources,
    IGVFSandboxResources,
    IGVFProdResources,
]

ExistingResourcesClass = Union[
    Type[IGVFDevResources],
    Type[IGVFStagingResources],
    Type[IGVFSandboxResources],
    Type[IGVFProdResources],
]
