## Infrastructure

Create virtual Python 3.9 environment and install requirements:

```
$ pip install -r requirements.txt -r requirements-dev.txt
```

Install CDK toolkit:

```
$ npm install -g aws-cdk@2.21.0
```

## Deploy demo stacks

Configure AWS credentials for dev account (e.g. in `igvf-dev` profile).

```bash
$ cdk deploy -c branch=IGVF-1234-my-feature-branch --profile igvf-dev
```

This deploys a CodePipeline stack tied to the `IGVF-1234-my-feature-branch` branch (make sure to push all of your changes to Github before deploying). The pipeline deploys the actual application and runs on every new commit to the branch. You can look at the deployed stacks for your branch in the CloudFormation console.

## Clean up demo stacks

```bash
$ cdk destroy -c branch=IGVF-1234-my-feature-branch --profile igvf-dev
```

This only cleans up the CodePipeline stack, not the application stacks deployed by the pipeline.

In most cases you probably want to clean up everything:

```bash
$ python commands/cdk_destroy_all_stacks.py -c branch=IGVF-1234-my-feature-branch --profile igvf-dev
# Follow (y/n) prompts...
```

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation


## Continuous deployment pipeline

Deploy CodePipeline to main branch:

```bash
$ cdk deploy -c branch=main
```

Destroy:

```bash
$ cdk destroy -c branch=main
```

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation


## Run type checking with mypy
```
# In cdk folder.
$ pip install -r requirements.txt -r requirements-dev.txt
$ mypy .
```
Runs in strict mode, excluding `test` folder.
