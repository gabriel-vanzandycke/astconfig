import ast
import os
from typing import Any, Dict

import astunparse

from astconfig.ast import update_ast

def exec_wrapper(string: str, env=None) -> Dict[str, Any]:
    env = env or {}
    code = compile(string, 'input-string', 'exec')
    exec(code, None, env)
    return env


class DictObject(dict):
    def __getattr__(self, key):
        if key in dir(self):
            raise AttributeError(f"{key} cannot be retrieved as attribute. Use '[{key}]' instead")
        return self[key]


class Config(DictObject):
    def __init__(self, config: str):
        if os.path.isfile(config):
            with open(config) as config:
                config = config.read()
        self.ast = ast.parse(config)
        d = exec_wrapper(str(self))
        super().__init__(d)

    def __str__(self):
        return astunparse.unparse(self.ast)

    def update(self, overwrite):
        if isinstance(overwrite, str):
            overwrite = exec_wrapper(overwrite)
        update_ast(self.ast, overwrite) # consumes 'overwrite' items
        d = exec_wrapper(str(self))
        super().__init__(d)

    def __getstate__(self):
        return (self.ast, )

    def __setstate__(self, state):
        ast, = state
        self.__init__(astunparse.unparse(ast))
