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
from os import getenv

import requests


class OktaEndpoints(object):
    def __init__(self, url):
        self.authn = f"{url}/api/v1/authn"
        self.sms_challenge = f"{url}/api/v1/authn/factors/" + "{factorId}/verify"


class Api:
    def __init__(self, okta_org: str, usr: str, pw: str):
        self.okta_org = okta_org
        self.okta: OktaEndpoints = OktaEndpoints(self.okta_org)
        self.interactive: bool = True
        self.session: requests.Session = requests.session()
        self.session.headers['Accept']: str = 'application/json'
        self.session.headers['Content-Type']: str = 'application/json'

        self.factorId: str = ""

    def _get_credentials(self):
        usr = getenv('OKTA_USERNAME')
        passwd = getenv('OKTA_PASSWORD')
        if usr:
            print(f'Okta username: {usr}')
        if not usr or not passwd:
            if self.interactive:
                usr = usr if usr else input("Okta username: ")
                passwd = passwd if passwd else input("Okta password: ")
        return usr, passwd

    def _authenticate_primary(self):
        usr, passwd = self._get_credentials()
        data = {
            "username": usr,
            "password": passwd,
            "options": {
                "multiOptionalFactorEnroll": True,
                "warnBeforePasswordExpired": True,
            }
        }
        resp = self.session.get(url=self.okta.authn, data=data)
        if resp.status_code == requests.codes.ok:
            return resp
        else:
            resp.raise_for_status()

    def authn(self):
        resp = self._authenticate_primary()
        import ipdb
        ipdb.set_trace()
