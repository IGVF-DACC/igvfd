'''
Usually `$cdk destroy` just deletes the CodePipeline stack
and not the stacks deployed by the CodePipeline.

See: https://github.com/aws/aws-cdk/issues/10190

Until there's official support for cleaning up all the stacks in an application
we can generate all the stacks in an application and iterate through them in
reverse-dependency order to destroy them one at a time.

You can also manually destroy dangling stacks in the CloudFormation console.

Usage:

Include all arguments from original deploy command. All argmuments get passed to underlying `cdk` command.

$ python commands/cdk_destroy_all_stacks.py -c branch=IGVF-1234-xyz --profile igvf-dev

Follow (y/n) destroy prompt...

Note removing stacks can take some time.
'''
import logging

import sys

from subprocess import check_output
from subprocess import check_call


logging.basicConfig(level=logging.DEBUG)


CDK_LS = ['cdk', 'ls']

CDK_DESTROY = ['cdk', 'destroy']


def get_all_stacks_in_app(args):
    command = CDK_LS + args
    logging.info(f'Getting all stacks with {command}')
    return check_output(
        command,
        encoding='UTF-8',
    )


def parse_ls_output(output):
    parsed_output = [
        value
        for value in output.split('\n')
        if value
    ]
    return parsed_output


def reverse_stacks(stacks):
    return list(reversed(stacks))


def destroy_stack(args, stack):
    command = CDK_DESTROY + args + [stack]
    logging.info(f'Destroying {stack} with {command}')
    return check_call(command)


def destroy_all_stacks(args):
    stacks = reverse_stacks(
        parse_ls_output(
            get_all_stacks_in_app(
                args
            )
        )
    )
    logging.info(f'Found {len(stacks)} stacks')
    for stack in stacks:
        destroy_stack(args, stack)


if __name__ == '__main__':
    args = sys.argv[1:]
    destroy_all_stacks(args)
