## Infrastructure

Create virtual Python environment for the CDK and install requirements:

```
$ pip install -r requirements.txt
```

Install CDK toolkit (`npm install -g aws-cdk`).

To generate CloudFormation:

```
$ cdk synth
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