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

DISPLAY_NAMES = {
    'push': 'Push notification (not yet supported)',
    'sms': 'SMS',
    'token:software:totp': 'Okta mobile app'
}

HANDLED_STATUS = ['MFA_REQUIRED', 'SUCCESS']


class OktaEndpoints:
    def __init__(self, okta_org, app_url):
        self.authn = "https://{}/api/v1/authn".format(okta_org)
        self.app_saml = "{}?onetimetoken=".format(app_url)


class Api:
    def __init__(self, okta_org: str, usr: str, pw: str, app_url: str, mfa_choice: str):
        self.okta: OktaEndpoints = OktaEndpoints(okta_org, app_url)
        self.usr = usr
        self.pw = pw
        self.mfa_choice = mfa_choice
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
    def _select_mfa_factor(factors):
        print('-' * 15)
        msg = ('Multiple MFA factors registered.\n'
               'Note: "push" is not currently supported...')
        f_types = [x['factorType'] for x in factors]
        # Format factor types for user experience ;)
        display_f_types = [
            DISPLAY_NAMES.get(x) if DISPLAY_NAMES.get(x) else x for x in f_types
        ]
        pick = let_user_pick(msg, display_f_types)
        # Filter for selected factor type
        factor = list(filter(lambda x: x['factorType'] == f_types[pick - 1], factors))[0]
        if factor == 'push':
            raise Exception('MFA factor "push" is not yet implemented.')
        return factor

    def _handle_multiple_mfa_factors(self, factors):
        if self.mfa_choice:
            return list(filter(lambda x: x['factorType'] == self.mfa_choice, factors))[0]
        else:
            return self._select_mfa_factor(factors)

    def _initiate_mfa(self, factor, state_token):
        data = {
            'stateToken': state_token
        }
        return self.session.post(
            url=factor['_links']['verify']['href'],
            json=data
        )

    def _input_and_send_code(self, data, factor):
        # Format for user experience
        display_name = DISPLAY_NAMES.get(factor) if DISPLAY_NAMES.get(factor) else factor
        mfa_code = input('Enter {} code: '.format(display_name))
        url = data['_links']['next']['href']
        resp = self.session.post(
            url=url,
            json={
                'stateToken': data['stateToken'],
                'passCode': mfa_code
            }
        )
        if resp.status_code == 200:
            return resp
        elif resp.status_code == 403:
            print('Incorrect or stale code.\n'
                  'Please check code...')
            return self._input_and_send_code(data, factor)
        else:
            raise Exception('Something went wrong.\nresp: {}\n'
                            'You may be locked out of Okta'.format(resp.content))

    def _verify_via_mfa(self, data):
        factors = [x for x in data['_embedded'].get('factors')]
        if len(factors) == 0:
            raise Exception("No MFA methods registered...")
        if len(factors) > 1:
            factor = self._handle_multiple_mfa_factors(factors)
        else:
            factor = factors[0]
        resp = self._initiate_mfa(factor, data['stateToken'])
        resp = self._input_and_send_code(resp.json(), factor['factorType'])
        return resp.json()

    def _get_token(self, data):
        if data.get('status') not in HANDLED_STATUS:
            raise Exception("Something went wrong.\n"
                            "Don't know how to handle status '{}'".format(data.get('status')))
        if data['status'] != 'SUCCESS':
            data = self._verify_via_mfa(data)
        token = data.get('sessionToken')
        if not token:
            raise Exception('No session token found in response: \n{}'.format(data))
        return token

    def _get_aws_app_saml(self, token):
        resp = self.session.post(url=self.okta.app_saml + token)
        doc = PyQuery(resp.text)
        saml_elem = doc('input:hidden')
        return saml_elem.val()

    def get_saml_via_auth(self):
        resp = self._authenticate_primary()
        token = self._get_token(resp.json())
        return self._get_aws_app_saml(token)
