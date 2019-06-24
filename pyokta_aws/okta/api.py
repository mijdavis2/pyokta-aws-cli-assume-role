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
from getpass import getpass

import requests
from pyquery import PyQuery

from pyokta_aws.utils import let_user_pick


class OktaEndpoints:
    def __init__(self, okta_org, app_url):
        self.authn = "https://{}/api/v1/authn".format(okta_org)
        self.app_saml = "{}?onetimetoken=".format(app_url)


class Api:
    def __init__(self, okta_org: str, usr: str, pw: str, app_url: str):
        self.okta: OktaEndpoints = OktaEndpoints(okta_org, app_url)
        self.usr = usr
        self.pw = pw
        self.interactive: bool = True
        self.session: requests.Session = requests.session()
        self.session.headers['Accept'] = 'application/json'
        self.session.headers['Content-Type'] = 'application/json'

    def _get_credentials(self):
        if self.usr:
            print(f'Okta username: {self.usr}')
        if not self.usr or not self.pw:
            if self.interactive:
                self.usr = self.usr if self.usr else input("Okta username: ")
                self.pw = self.pw if self.pw else getpass("Okta password: ")

    def _authenticate_primary(self):
        self._get_credentials()
        data = {
            "username": self.usr,
            "password": self.pw,
            "options": {
                "multiOptionalFactorEnroll": True,
                "warnBeforePasswordExpired": True,
            }
        }
        resp = self.session.post(url=self.okta.authn, json=data)
        if resp.status_code == requests.codes.ok:
            return resp
        else:
            resp.raise_for_status()

    @staticmethod
    def _select_mfa_method(factors):
        print('-' * 15)
        msg = ('Multiple MFA methods registered.\n'
               'Note: "push" is not currently supported...')
        methods = [x['factorType'] for x in factors]
        pick = let_user_pick(msg, methods)
        method = [x for x in factors if x['factorType'] == methods[pick - 1]][0]
        if method == 'push':
            raise Exception('MFA method "push" is not yet implemented.')
        return method

    def _verify_via_mfa(self, data):
        if data.get('status') != 'MFA_REQUIRED':
            return
        state_token = data['stateToken']
        factors = [x for x in data['_embedded']['factors']]
        if len(factors) > 1:
            factor = self._select_mfa_method(factors)
        else:
            factor = factors[0]
        if factor.get('_links'):
            if factor['_links'].get('verify'):
                data = {
                    'stateToken': state_token
                }
                resp = self.session.post(
                    url=factor['_links']['verify']['href'],
                    json=data
                )
                data = resp.json()
                state_token = data.get('stateToken')
        mfa_code = input('Enter {} code:'.format(factor['factorType']))
        url = data['_links']['next']['href']
        data = {
            'stateToken': state_token,
            'passCode': mfa_code
        }
        return self.session.post(url=url, json=data)

    def _get_aws_app_saml(self, token):
        resp = self.session.post(url=self.okta.app_saml + token)
        doc = PyQuery(resp.text)
        saml_elem = doc('input:hidden')
        return saml_elem.val()

    def get_saml_via_auth(self):
        resp = self._authenticate_primary()
        resp = self._verify_via_mfa(resp.json())
        return self._get_aws_app_saml(resp.json().get('sessionToken'))
