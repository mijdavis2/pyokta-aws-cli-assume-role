import argparse
from pyokta_aws.api import Api
from pyokta_aws import settings


def main(args):
    parser = argparse.ArgumentParser(prog='pyokta-aws auth')
    settings.Settings.register_argparse_arguments(parser)
    args = parser.parse_args(args)
    auth_settings = settings.Settings.from_argparse(args)
    api = Api(auth_settings)
    return
