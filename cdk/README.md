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

### Configure

Configure your AWS credentials for the `igvf-dev` account (e.g. in `igvf-dev` profile). This is the account where your demo will be deployed.

```
# In ~/.aws/credentials
[igvf-dev]
aws_secret_access_key = XYZ123
aws_access_key_id = ABC321
```

```
# In ~/.aws/config
[profile igvf-dev]
region = us-west-2
```

This sets the access key and region used when you specify `--profile igvf-dev` on the command line.

Ask to be invited to the `aws-chatbot` Slack channel, where you can monitor the status transitions of your deployment pipeline.

### Command

Make sure your Python virtual environment is activated, the Node and Python requirements above are installed, and Docker is running.

Push all of your changes to your Github branch (e.g. `IGVF-1234-my-feature-branch`) before deploying. Pick a branch name that doesn't conflict with anyone else's pipeline.

```bash
$ git push origin IGVF-1234-my-feature-branch
```

Make sure you are in the `cdk` folder of the repo and deploy the pipeline.

```bash
$ cdk deploy -c branch=IGVF-1234-my-feature-branch --profile igvf-dev
```

This passes the branch name as a context variable, and tells the CDK to use your credentials for the `igvf-dev` account. It's important to exactly match the branch name that you've pushed to Github, as this is where the pipeline listens for code changes. The branch name is also used for generating a URL for the demo.

If this is the first time you've run the command the underlying Docker image used for bundling could take some time to download. You can monitor what's happening by passing the `-v` verbose flag.

![synth output](images/synth_demo.png)

Eventually you should see a list of proposed security policy changes.

![iam changes](images/iam_changes.png)

Confirm that you want to make these changes.

![deploy changes](images/deploy_changes.png)

### Monitoring deployment and resources

You should see a notification in the `aws-chatbot` Slack channel that your pipeline has `STARTED`. You can click on that link or find your pipeline in the `AWS CodePipeline` console to watch your pipeline execute the steps to deploy the actual application. It takes about twenty minutes for the pipeline to run tests, build Docker image assets, and spin up the infrastructure. After that you should have three `AWS CloudFormation` stacks, one for the pipeline, one for Postgres, and one for the backend.

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
