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
import functools
import os


def no_positional(allow_self=False):
    """A decorator that doesn't allow for positional arguments.

    :param bool allow_self:
        Whether to allow ``self`` as a positional argument.
    """
    def reject_positional_args(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            allowed_positional_args = 0
            if allow_self:
                allowed_positional_args = 1
            received_positional_args = len(args)
            if received_positional_args > allowed_positional_args:
                function_name = function.__name__
                verb = 'were' if received_positional_args > 1 else 'was'
                raise TypeError(('{}() takes {} positional arguments but {} '
                                 '{} given').format(
                                     function_name,
                                     allowed_positional_args,
                                     received_positional_args,
                                     verb,
                ))
            return function(*args, **kwargs)
        return wrapper
    return reject_positional_args


class EnvironmentDefault(argparse.Action):
    """Get values from environment variable."""

    def __init__(self, env, required=True, default=None, **kwargs):
        default = os.environ.get(env, default)
        self.env = env
        if default:
            required = False
        super(EnvironmentDefault, self).__init__(
            default=default,
            required=required,
            **kwargs
        )

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


def let_user_pick(msg, options):
    print(msg)
    for idx, element in enumerate(options):
        print("{}) {}".format(idx+1, element))
    i = input("Enter number: ")
    try:
        if 0 < int(i) <= len(options):
            return int(i)
        print('Unrecognized option...')
        return let_user_pick(msg, options)
    except ValueError:
        print('Unrecognized option...')
        return let_user_pick(msg, options)
