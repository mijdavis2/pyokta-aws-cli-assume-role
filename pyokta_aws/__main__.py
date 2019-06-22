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
import sys

import requests

from pyokta_aws import exceptions
from pyokta_aws.cli import dispatch


def main():
    try:
        return dispatch(sys.argv[1:])
    except (exceptions.PyOktaAwsException, requests.exceptions.HTTPError) as exc:
        return '{}: {}'.format(exc.__class__.__name__, exc.args[0])


if __name__ == "__main__":
    sys.exit(main())
