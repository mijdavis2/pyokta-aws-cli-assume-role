# pyokta-aws-cli-assume-role
# Copyright (C) 2019  mijdavis2
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os.path

from configobj import ConfigObj

from pyokta_aws import utils

MFA_SETTING_MAP = {
    'sms': 'sms',
    'app': 'token:software:totp'
}

STS_DEFAULT = 3600


class Settings(object):
    """Object that manages the configuration for pyokta_aws.

    This object can only be instantiated with keyword arguments.

    For example,

    .. code-block:: python

        Settings('myprofile', username='fakeusername')

    Will raise a :class:`TypeError`. Instead, you would want

    .. code-block:: python

        Settings(profile='myprofile', username='fakeusername')
    """

    @utils.no_positional(allow_self=True)
    def __init__(self,
                 profile=None,
                 region=None,
                 username=None, password=None,
                 okta_org=None,
                 okta_aws_app_url=None,
                 aws_role_to_assume=None,
                 aws_idp=None,
                 sts_duration=None,
                 mfa_choice=None,
                 config_file='~/.pyokta_aws/config',
                 verbose=False,
                 interactive=True,
                 **ignored_kwargs
                 ):
        """Initialize our settings instance.

        :param str profile:
            AWS cli profile to use.

            This defaults to ``default``.
        :param str username:
            The username used to authenticate to Okta.
        :param str password:
            The password used to authenticate to Okta.
        :param str okta_org:
            The Okta Org base url.
        :param str config_file:
            The path to the configuration file to use.

            This defaults to ``~/.pyokta_aws/config``.
        :param bool verbose:
            Show verbose output.
        """
        self.profile = profile
        self.region = region
        self.username = username
        self.password = password
        self.okta_org = okta_org
        self.okta_aws_app_url = okta_aws_app_url
        self.aws_role_to_assume = aws_role_to_assume
        self.aws_idp = aws_idp
        self.sts_duration = sts_duration
        self.mfa_choice = mfa_choice
        self.config_file = config_file
        self.verbose = verbose

    @staticmethod
    def register_argparse_arguments(parser):
        """Register the arguments for argparse."""
        parser.add_argument(
            "-p", "--profile",
            action=utils.EnvironmentDefault,
            env="OKTA_AWS_PROFILE",
            default='default',
            required=False,
            help="AWS profile to use for authentication. "
                 "Example: myorg.okta.com "
                 "(Can also be set via %(env)s environment variable.)",
        )
        parser.add_argument(
            "-r", "--region",
            action=utils.EnvironmentDefault,
            env="OKTA_AWS_REGION",
            required=False,
            help="AWS region to use for profile. "
                 "This will override your aws config region for the given profile "
                 "(Can also be set via %(env)s environment variable.)",
        )
        parser.add_argument(
            "-o", "--okta-org",
            action=utils.EnvironmentDefault,
            env="OKTA_ORG",
            required=False,
            help="Your Okta Org base URL. "
                 "Example: myorg.okta.com "
                 "(Can also be set via %(env)s environment variable.)",
        )
        parser.add_argument(
            "-a", "--okta-aws-app-url",
            action=utils.EnvironmentDefault,
            env="OKTA_AWS_APP_URL",
            required=False,
            help="The url for the Okta AWS app url. "
                 "Example: https://myorg.okta.com/home/amazon_aws/1a2b3c4d5e "
                 "(Can also be set via %(env)s environment variable.)",
        )
        parser.add_argument(
            "-ar", "--aws-role-to-assume",
            action=utils.EnvironmentDefault,
            env="OKTA_AWS_ROLE_TO_ASSUME",
            required=False,
            help="The AWS role ARN to assume. "
                 "Consists of aws account id, role, and okta user "
                 "(username or email depending on okta app setup). "
                 "Example: <aws_accnt_id>:role/<role_name> "
                 "(Can also be set via %(env)s environment variable.)",
        )
        parser.add_argument(
            "-idp", "--aws-idp",
            action=utils.EnvironmentDefault,
            env="OKTA_AWS_IDP_ARN",
            required=False,
            help="The AWS identity provider. "
                 "Found in IAM > Identity Providers in AWS console. "
                 "Example: <aws_accnt_id>:saml-provider/<provider_name> "
                 "(Can also be set via %(env)s environment variable.)",
        )
        parser.add_argument(
            "-u", "--username",
            action=utils.EnvironmentDefault,
            env="OKTA_USERNAME",
            required=False,
            help="The username to authenticate to the repository "
                 "(package index) as. (Can also be set via "
                 "%(env)s environment variable.)",
        )
        parser.add_argument(
            "-pw", "--password",
            action=utils.EnvironmentDefault,
            env="OKTA_PASSWORD",
            required=False,
            help="The password to authenticate to the repository "
                 "(package index) with. (Can also be set via "
                 "%(env)s environment variable.)",
        )
        parser.add_argument(
            "-s", "--sts-duration",
            action=utils.EnvironmentDefault,
            env="OKTA_STS_DURATION",
            required=False,
            help="The AWS session duration. "
                 "(Can also be set via %(env)s environment variable.)",
        )
        parser.add_argument(
            "-m", "--mfa-choice",
            action=utils.EnvironmentDefault,
            env="OKTA_MFA_CHOICE",
            required=False,
            help="The preferred MFA factor choice. "
                 "Options: 'sms', 'app'. "
                 "The 'app' option refers to the Okta mobile MFA apps."
                 "(Can also be set via %(env)s environment variable.)",
        )
        parser.add_argument(
            "-c", "--config-file",
            action=utils.EnvironmentDefault,
            env="PYOKTA_AWS_CONFIG",
            default="~/.pyokta_aws/config",
            help="The pyokta_aws config file to use. "
                 "This is not referring to awscli config. "
                 "(Can also be set via %(env)s environment variable.)",
        )
        parser.add_argument(
            "--non-interactive",
            default=False,
            required=False,
            action="store_true",
            help="Run command non-interactively. "
                 "Requires that all settings are set "
                 "via cli, env vars, or config file.",
        )
        parser.add_argument(
            "--verbose",
            default=False,
            required=False,
            action="store_true",
            help="Show verbose output.",
        )

    @classmethod
    def from_argparse(cls, args):
        """Generate the Settings from parsed arguments."""
        settings = vars(args)
        settings['config_file'] = os.path.expanduser(settings['config_file'])
        settings['interactive'] = not settings.pop('non_interactive')
        if settings['config_file'].lower() != 'none':
            settings = cls.load_config_settings(settings)
        if not settings.get('sts_duration'):
            if settings['verbose']:
                print('Setting sts to default value "{}"'.format(STS_DEFAULT))
            settings['sts_duration'] = STS_DEFAULT
        # Format arn settings
        iam_string = 'arn:aws:iam::'
        settings['aws_role_to_assume'] = '{}{}'.format(
            iam_string, settings['aws_role_to_assume'].replace(iam_string, '')
        )
        settings['aws_idp'] = '{}{}'.format(
            iam_string, settings['aws_idp'].replace(iam_string, '')
        )
        if settings['verbose']:
            cls.print_settings(settings)
        settings = cls._handle_mfa_choice(settings)
        return cls(**settings)

    @staticmethod
    def _handle_mfa_choice(settings):
        mfa_choice = settings.get('mfa_choice')
        if mfa_choice:
            if mfa_choice not in MFA_SETTING_MAP.keys():
                print('Unknown mfa choice: "{}".'.format(mfa_choice))
                print('Please use one of {}'.format(MFA_SETTING_MAP.keys()))
                exit(1)
            settings['mfa_choice'] = MFA_SETTING_MAP[mfa_choice]
        return settings

    @staticmethod
    def load_config_settings(settings):
        """Load empty settings from config_file."""
        config_file = settings['config_file']
        profile = settings['profile']
        if not os.path.isfile(config_file):
            raise Exception('Config file "{}" does not exist.'.format(config_file))
        if settings['verbose']:
            print('Loading settings from config file "{}"...'.format(config_file))
        conf_settings = ConfigObj(config_file).get(profile)
        if not conf_settings:
            msg = 'Profile "{}" is not in config file "{}".'.format(profile, config_file)
            raise Exception(msg)
        for x, y in settings.items():
            if not y:
                settings[x] = conf_settings.get(x)
        try:
            settings['sts_duration'] = int(settings['sts_duration'])
        except ValueError as exc:
            print('STS duration "{}" cannot be converted to an int: {}'.format(
                  settings['sts_duration'], exc))
            exit(1)
        except TypeError:
            if settings['verbose']:
                print('STS duration "{}" cannot be converted to an int...'.format(
                      settings['sts_duration']))
            settings['sts_duration'] = None
        return settings

    @staticmethod
    def print_settings(settings):
        """Print all settings. Password is redacted."""
        print("Using the following settings...")
        for x, y in settings.items():
            print('{:.<18s}: {}'.format(x, str(y) if x != 'password' else '<redacted>'))
