## Infrastructure

Install CDK toolkit:

```
$ npm install -g aws-cdk@2.21.0
```

Create virtual Python 3.9 environment and install requirements:

```
$ pip install -r requirements.txt -r requirements-dev.txt
```

Make sure Docker is running.

## Deploy demo stacks

### Overview

Demo applications are not deployed directly. Instead you deploy an `AWS CodePipeline` pipeline once, tied to your Github branch, that deploys the actual application. Once the pipeline is deployed every new commit to your branch will trigger a pipeline execution that updates the application with the new commit. You can watch your pipeline in the `AWS CodePipeline` console to see the commit moving through the deployment steps.

### Command

Configure AWS credentials for dev account (e.g. in `igvf-dev` profile).

```bash
$ cdk deploy -c branch=IGVF-1234-my-feature-branch --profile igvf-dev
```

This deploys a pipeline stack tied to the `IGVF-1234-my-feature-branch` branch (make sure to push all of your changes to Github before deploying).

### Monitoring deployment and resources

You should see a notification in the `aws-chatbot` Slack channel that your pipeline has `STARTED`. You can click on that link or find your pipeline in the `AWS CodePipeline` console to watch your pipeline execute the steps to deploy the actual application. It takes about twenty minutes for the pipeline to run tests, build Docker image assets, and spin up the infrastructure. After that you should have three stacks in `AWS CloudFormation`, one for the pipeline, one for Postgres, and one for the backend.

In the `AWS CloudFormation` console the URL of your demo is listed in the output tab of your backend stack. You can see all of the actual resources (RDS instance, Fargate cluster, IAM roles, Route53 record, etc.) associated with your application in the resources tab of the stacks.

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

## Run type checking with mypy
```
# In cdk folder.
$ pip install -r requirements.txt -r requirements-dev.txt
$ mypy .
```
Runs in strict mode, excluding `test` folder.
