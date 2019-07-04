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
import argparse
import os.path

import boto3
from configobj import ConfigObj

from pyokta_aws import settings
from pyokta_aws.okta.api import Api as OktaApi


def aws_auth_with_saml(saml: str, aws_role_to_assume: str, aws_idp: str, sts_duration: str):
    data = {
        'SAMLAssertion': saml,
        'RoleArn': aws_role_to_assume,
        'PrincipalArn': aws_idp,
        'DurationSeconds': sts_duration,
    }
    client = boto3.client('sts')
    return client.assume_role_with_saml(**data)


def update_aws_credentials_file(profile: str, key_id: str, secret: str, session_token: str):
    aws_creds_file = os.path.expanduser('~/.aws/credentials')
    if not os.path.isfile(aws_creds_file):
        print('No aws credentials file found. Creating one for you...')
    conf = ConfigObj(aws_creds_file)
    if not conf.get(profile):
        conf[profile] = {}
    conf[profile]['aws_access_key_id'] = key_id
    conf[profile]['aws_secret_access_key'] = secret
    conf[profile]['aws_session_token'] = session_token
    conf.write()


def setup_aws_config_if_required(profile: str, region: str):
    aws_config_file = os.path.expanduser('~/.aws/config')
    if not os.path.isfile(aws_config_file):
        print('No aws config file found. Creating one for you...')
    conf = ConfigObj(aws_config_file)
    profile = 'profile {}'.format(profile)
    if not conf.get(profile):
        conf[profile] = {}
    conf[profile]['region'] = region
    conf.write()


def authenticate(settings):
    okta = OktaApi(
        okta_org=settings.okta_org,
        usr=settings.username,
        pw=settings.password,
        app_url=settings.okta_aws_app_url,
        mfa_choice=settings.mfa_choice,
    )
    saml = okta.get_saml_via_auth()
    resp = aws_auth_with_saml(
        saml=saml,
        aws_role_to_assume=settings.aws_role_to_assume,
        aws_idp=settings.aws_idp,
        sts_duration=settings.sts_duration,
    )
    creds = resp['Credentials']
    update_aws_credentials_file(
        profile=settings.profile,
        key_id=creds['AccessKeyId'],
        secret=creds['SecretAccessKey'],
        session_token=creds['SessionToken'],
    )
    print('SUCCESS!')


def main(args):
    aws_dir = os.path.expanduser('~/.aws')
    aws_dir_exists = os.path.isdir(aws_dir)
    if not aws_dir_exists:
        raise Exception('"{}" dir not found. Is the awscli installed?'.format(aws_dir))
    parser = argparse.ArgumentParser(prog='pyokta-aws auth')
    settings.Settings.register_argparse_arguments(parser)
    args = parser.parse_args(args)
    auth_settings = settings.Settings.from_argparse(args)
    setup_aws_config_if_required(
        profile=auth_settings.profile, region=auth_settings.region
    )
    return authenticate(auth_settings)
