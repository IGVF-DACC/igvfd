## Infrastructure

Install Node.js 16 using `nvm` (Node Version Manager):

```
# Install nvm.
$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
```

Then in new terminal:

```
# Install and use node 16.
$ nvm install 16
$ nvm use 16
# Check version.
$ node --version
```

Install CDK toolkit (requires Node.js 16.x):

```
$ npm install -g aws-cdk@2.42.1
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

This passes the branch name as a context variable, and tells the CDK to use your credentials for the `igvf-dev` account. It's important to match the branch name that you've pushed to Github exactly, as this is where the pipeline listens for code changes. The branch name is also used for generating a URL for the demo.

If this is the first time you've run the command the underlying Docker image used for bundling could take some time to download. You can monitor what's happening by passing the `-v` verbose flag.

![synth output](images/synth_demo.png)

Eventually you should see a list of proposed security policy changes.

![iam changes](images/iam_changes.png)

Confirm that you want to make these changes.

![deploy changes](images/deploy_changes.png)

### Monitoring deployment and resources

You should see a notification in the `aws-chatbot` Slack channel that your pipeline has `STARTED`.

![slack notification](images/pipeline_started.png)

You can click on that link or find your pipeline in the `AWS CodePipeline` console to watch your pipeline execute the steps to deploy the actual application.

![pipelines](images/pipelines.png)

It takes about twenty minutes for the pipeline to run tests, build Docker image assets, and spin up the infrastructure. Here you can see the first two steps in the pipeline: listening to your Github branch and synthesizing a CloudFormation template.

![pipeline steps](images/pipeline_steps.png)

After the pipeline completes you should see a success notification in Slack:

![slack success](images/pipeline_succeeded.png)

And have three `AWS CloudFormation` stacks, one for the pipeline, one for Postgres, and one for the backend.

![demo stacks](images/demo_stacks.png)

In the `AWS CloudFormation` console the URL of your demo is listed in the output tab of your backend stack.

![stack output](images/stack_output.png)

You can see all of the actual resources (RDS instance, Fargate cluster, IAM roles, Route53 record, etc.) associated with your application in the resources tab of the stacks.

![stack resources](images/stack_resources.png)

The deployed resources should have metadata tags. For example the RDS instance shows its associated branch and source snapshot.

![rds tags](images/rds_tags.png)

Browse using the demo URL (e.g. `https://igvfd-igvf-1234-my-feature-branch.demo.igvf.org`):

![home](images/home.png)

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

Pass the `--force` flag to bypass the confirmation prompts.

### Automatic clean up

By default demo stacks have a lifetime of 72 hours, after which they get destroyed. Additionally, by default the demo stacks will be deleted during the Friday night (Friday night means 0000-0659 hours on Saturday, US/Pacific timezone). This behavior is configured in `cdk/infrastructure/config.py`. Altering the default behavior can be done by editing and committing changes to values in
```
'tags': [
    ('time-to-live-hours', '72'),
    ('turn-off-on-friday-night', 'yes'),
],
```
In `turn-off-on-friday-night` tag, any value other than `yes` is interpreted as a negative (as well as the absence of the tag).

## Notes on demos

Avoid deploying a demo stack to our primary/shared branches (e.g. `dev` or `main`) as these already have their own pipelines associated with them. If you want to deploy your own demo that matches `dev`, for example, first checkout `dev`, pull all of the changes, and then copy them to your own branch with a special name:

```bash
$ git checkout dev
$ git pull
$ git checkout -b dev-keenan
```

Then use this new branch to deploy your pipeline.

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
