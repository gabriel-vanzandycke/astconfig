import ast
import copy
import functools
import itertools
import os
import types
from typing import Any, Dict

import astunparse

from astconfig.ast import update_ast

def exec_wrapper(string: str, env=None) -> Dict[str, Any]:
    env = env or {}
    code = compile(string, 'input-string', 'exec')
    exec(code, None, env)
    return {k:v for k,v in env.items() if not isinstance(v, types.ModuleType)}

class DictObject(dict):
    def __getattr__(self, name):
        if name in dir(self):
            raise AttributeError(f"{name} cannot be retrieved as attribute. Use '[{name}]' instead")
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


class Config(DictObject):
    def __init__(self, config: str = ""):
        """ Creates a configuration object from a string or a filename.
        """
        if os.path.isfile(config):
            with open(config) as config:
                config = config.read()
        self.ast = ast.parse(config)
        super().__init__(exec_wrapper(str(self)))

    def __str__(self):
        return astunparse.unparse(self.ast)

    def update(self, *overwrite_args, **overwrite_kwargs):
        """ Updates in place current configuration with the given values.
            It accepts:
            - strings of format '<key>=<value>'
            - dictionaries
            - or keyword arguments
        """
        try:
            overwrite = functools.reduce(
                lambda acc, arg: {**acc, **(exec_wrapper(arg) if isinstance(arg, str) else arg)},
                overwrite_args, overwrite_kwargs
            )
        except TypeError as e:
            raise TypeError("'update' only supports str, dicts or **kwargs") from e
        update_ast(self.ast, overwrite) # consumes 'overwrite' items
        super().__init__(exec_wrapper(str(self)))

    def __or__(self, other):
        if isinstance(other, str):
            other = exec_wrapper(other)
        config = copy.deepcopy(self)
        config.update(other)
        return config

    def __xor__(self, other):
        return self.__or__(other)

    def __reduce__(self):
        return (self.__class__, (str(self), ))

    def __getstate__(self):
        return (self.ast, )

    def __setstate__(self, state):
        ast, = state
        self.__init__(astunparse.unparse(ast))

    def product(self, *args):
        args = [exec_wrapper(arg) if isinstance(arg, str) else arg
            for arg in args]
        args = functools.reduce(lambda x, y: x | y, args)
        kvs = [[(k, v) for v in args[k]] for k in args]
        for update in itertools.product(*kvs):
            update = dict(update)
            config = copy.deepcopy(self)
            config.update(update)
            yield config

