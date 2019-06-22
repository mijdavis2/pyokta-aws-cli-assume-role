from dataclasses import dataclass
from os import getenv

# import requests


class OktaEndpoints(object):
    auth = "{url}/api/v1/authn"
    sms_challenge = "{url}/api/v1/authn/factors/{factorId}/verify"


okta = OktaEndpoints()


@dataclass
class Api:
    url: str = ""
    factorId: str = ""
    interactive: bool = True

    def _get_credentials(self):
        usr = getenv('OKTA_USERNAME')
        passwd = getenv('OKTA_PASSWD')
        if not usr or not passwd:
            if self.interactive:
                usr = usr if usr else input("Okta username: ")
                passwd = passwd if passwd else input("Okta password: ")
        return usr, passwd

    def authenticate(self):
        usr, passwd = self._get_credentials()
        print("WOO!")
        print(usr)
        print(passwd)
