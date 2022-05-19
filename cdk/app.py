import aws_cdk as cdk

from infrastructure.constructs.existing import igvf_dev

from infrastructure.config import build_config_from_name
from infrastructure.config import get_config_name_from_branch
from infrastructure.naming import prepend_project_name
from infrastructure.naming import prepend_branch_name

from infrastructure.stacks.pipeline import pipeline_stack_factory


app = cdk.App()

branch = app.node.try_get_context('branch')

if branch is None:
    raise ValueError('Must specify branch context: `-c branch=$BRANCH`')

config_name = (
    app.node.try_get_context('config-name')
    or get_config_name_from_branch(branch)
)

config = build_config_from_name(
    config_name,
    branch=branch,
)

pipeline_class = pipeline_stack_factory(
    config.pipeline
)

pipeline = pipeline_class(
    app,
    prepend_project_name(
        prepend_branch_name(
            branch,
            pipeline_class.__name__,
        )
    ),
    existing_resources_class=igvf_dev.Resources,
    config=config,
    env=igvf_dev.US_WEST_2,
)

app.synth()
