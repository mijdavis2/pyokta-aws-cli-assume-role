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
import os


def main(args):
    print('This command is a WIP. '
          'Simply creating the default "~/.pyokta_aws" dir and exiting... ')
    d = os.path.expanduser('~/.pyokta_aws')
    if not os.path.isdir(d):
        os.makedirs(d)
    open(os.path.expanduser('{}/config'.format(d)), 'a').close()
