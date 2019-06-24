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
from pyokta_aws.okta.api import Api as OktaApi
from pyokta_aws import settings


def authenticate(settings):
    api = OktaApi(
        okta_org=settings.okta_org,
        usr=settings.username,
        pw=settings.password,
        app_url=settings.okta_aws_app_url
    )
    saml = api.authn()
    print(saml)
    print('TODO: use saml to auth with aws')


def main(args):
    parser = argparse.ArgumentParser(prog='pyokta-aws auth')
    settings.Settings.register_argparse_arguments(parser)
    args = parser.parse_args(args)
    auth_settings = settings.Settings.from_argparse(args)
    return authenticate(auth_settings)
