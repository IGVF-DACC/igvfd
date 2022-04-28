import aws_cdk as cdk


from infrastructure.constructs.ci import ContinuousIntegration


def get_build_spec():
    return {
        'version': '0.2',
        'env': {
            'secrets-manager': {
                'DOCKER_USER': 'docker-hub-credentials:DOCKER_USER',
                'DOCKER_SECRET': 'docker-hub-credentials:DOCKER_SECRET',
            },
        },
        'phases': {
            'install': {
                'runtime-versions': {
                    'python': '3.9',
                },
                'commands': [
                    'echo $CODEBUILD_WEBHOOK_TRIGGER',
                    'echo $(git log -1 --pretty="%s (%h) - %an")',
                    'echo Logging into Docker',
                    'echo $DOCKER_SECRET | docker login --username $DOCKER_USER --password-stdin',
                    'echo Building images',
                    'docker-compose -f docker-compose.test.yml build',
                    'echo Setting permission to share mounted volume between users',
                    'sudo useradd -u 1444 igvfd',
                    'sudo usermod -a -G igvfd root',
                    'sudo chown -R root:igvfd ./',
                    'sudo chmod -R g+rwX ./',
                ]
            },
            'build': {
                'commands': [
                    'docker-compose -f docker-compose.test.yml up --exit-code-from pyramid',
                ]
            }
        },
    }


class ContinuousIntegrationStack(cdk.Stack):

    def __init__(self, scope, construct_id, *, existing_resources, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        self.existing_resources = existing_resources(
            self,
            'ExistingResources',
        )
        self.ci = ContinuousIntegration(
            self,
            'ContinuousIntegration',
            github_owner='igvf-dacc',
            github_repo='igvfd',
            build_spec=get_build_spec(),
            docker_hub_credentials=self.existing_resources.docker_hub_credentials,
        )
