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
import builtins

import mock
from pyokta_aws import utils


# TODO: Also test unsupported answer.
# Not sure how to do that for a recursive runction.
def test_let_user_pick():
    with mock.patch.object(builtins, 'input', lambda _: '1'):
        msg = "Pick one:"
        options = ['a', 'b']
        pick = utils.let_user_pick(msg, options)
        assert pick == 1
        assert options[pick - 1] == 'a'
