import functools
import argparse
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
