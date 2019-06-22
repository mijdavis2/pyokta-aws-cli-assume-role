from os import getenv

import requests


class OktaEndpoints(object):
    def __init__(self, url):
        self.authn = f"{url}/api/v1/authn"
        self.sms_challenge = f"{url}/api/v1/authn/factors/" + "{factorId}/verify"


class Api:
    def __init__(self, settings):
        self.url: str = settings.okta_org
        self.okta: OktaEndpoints = OktaEndpoints(settings.okta_org)
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
