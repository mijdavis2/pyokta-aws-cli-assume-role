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

import pkg_resources
import requests
import setuptools

import pyokta_aws


def _registered_commands(group='pyokta_aws.registered_commands'):
    registered_commands = pkg_resources.iter_entry_points(group=group)
    return {c.name: c for c in registered_commands}


def list_dependencies_and_versions():
    return [
        ('requests', requests.__version__),
        ('setuptools', setuptools.__version__),
    ]


def dep_versions():
    return ', '.join(
        '{}: {}'.format(*dependency)
        for dependency in list_dependencies_and_versions()
    )


def dispatch(argv):
    registered_commands = _registered_commands()
    parser = argparse.ArgumentParser(prog="pyokta-aws")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s version {} ({})".format(
            pyokta_aws.__version__,
            dep_versions(),
        ),
    )
    parser.add_argument(
        "command",
        choices=registered_commands.keys(),
    )
    parser.add_argument(
        "args",
        help=argparse.SUPPRESS,
        nargs=argparse.REMAINDER,
    )

    args = parser.parse_args(argv)

    main = registered_commands[args.command].load()

    return main(args.args)
