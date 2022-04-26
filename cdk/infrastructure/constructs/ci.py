import aws_cdk as cdk

from constructs import Construct

from aws_cdk.aws_codebuild import BuildSpec
from aws_cdk.aws_codebuild import BuildEnvironment
from aws_cdk.aws_codebuild import Cache
from aws_cdk.aws_codebuild import LinuxBuildImage
from aws_cdk.aws_codebuild import LocalCacheMode
from aws_cdk.aws_codebuild import Project
from aws_cdk.aws_codebuild import Source

from aws_cdk.aws_iam import PolicyStatement
from aws_cdk.aws_iam import Role
from aws_cdk.aws_iam import ServicePrincipal

from aws_cdk.aws_secretsmanager import Secret

from infrastructure.naming import prepend_project_name


class PublicContinuousIntegrationForGithub(Construct):

    def __init__(self, scope, construct_id, github_owner, github_repo, build_spec, docker_credentials, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        self._github_owner = github_owner
        self._github_repo = github_repo
        self._build_spec = build_spec
        self._docker_credentials = docker_credentials
        self._define_github_source()
        self._make_continuous_integration_project()
        self._give_project_permission_to_read_docker_login_secret()
        self._add_public_url()
        self._make_logs_public()

    def _define_github_source(self):
        self._github = Source.git_hub(
            owner=self._github_owner,
            repo=self._github_repo,
            webhook=True,
        )

    def _make_continuous_integration_project(self):
        self._continuous_integration_project = Project(
            self,
            prepend_project_name(
                'ContinuousIntegration'
            ),
            source=self._github,
            environment=BuildEnvironment(
                build_image=LinuxBuildImage.STANDARD_5_0,
                privileged=True,
            ),
            build_spec=Buildspec.from_object(
                self._build_spec
            ),
            badge=True,
            cache=Cache.local(
                LocalCacheMode.DOCKER_LAYER
            ),
        )

    def _give_project_permission_to_read_docker_login_secret(self):
        self._docker_credentials.grant_read(
            self._continuous_integration_project.role
        )

    def _get_underlying_cfn_project(self):
        if getattr(self, '_cfn_project', None) is None:
            self._cfn_project = self._continuous_integration_project.node.default_child
        return self._cfn_project

    def _add_public_url(self):
        self._get_underlying_cfn_project().visibility = 'PUBLIC_READ'

    def _get_log_group_arn(self):
        project_name = self._continuous_integration_project.project_name
        log_group_arn = cdk.Stack.of(self).format_arn(
            service='logs',
            resource='log-group',
            arn_format=cdk.ArnFormat.COLON_RESOURCE_NAME,
            resource_name=f'/aws/codebuild/{project_name}',
        )
        return log_group_arn

    def _get_log_group_star_arn(self):
        log_group_star_arn = f'{self._get_log_group_arn()}:*'
        return log_group_star_arn

    def _make_logs_public(self):
        resource_access_role = Role(
            self,
            'ResourceAccessRole',
            assumed_by=ServicePrincipal(
                'codebuild.amazonaws.com'
            )
        )
        public_log_read_policy = PolicyStatement(
            resources=[
                self._get_log_group_star_arn(),
            ],
            actions=[
                'logs:GetLogEvents'
            ],
        )
        resource_access_role.add_to_principal_policy(
            public_log_read_policy
        )
        cfn_project = self._get_underlying_cfn_project()
        cfn_project.resource_access_role = resource_access_role.role_arn
