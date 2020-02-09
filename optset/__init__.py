from enum import Enum
import json
import os

import argparsex
from box import Box

class OptionAttr(Enum):
    SUPPLIED = 1
    DEFAULT = 2
    SUPPLIED_DEFAULT = 3
    HIDDEN = 4

class Options:
    __initing = True

    def __init__(self, mapping, parse_function, hidden_options={}):
        self._mapping = {}

        for key, val in mapping.items():
            if val in self._mapping:
                raise ValueError('Dupe error with Options mapping for key {}, '
                                 'val {}'.format(key, val))
            self._mapping[val] = key

        self._parse_function = parse_function
        self._options = {}
        self._options_attr = {}

        self._add_hidden_options(hidden_options)
        supplied, supplied_as_default, default = self._parse_cmd_args()
        self._add_options(supplied, supplied_as_default, default)

        self._convert_options()

        self.__initing = False

    def _add_hidden_options(self, hidden):
        for key, val in hidden.items():
            self._options[key] = val
            self._options_attr[key] = {'src': OptionAttr.HIDDEN}

    def _add_options(self, supplied, supplied_as_default, default):
        for key, val in supplied.items():
            self._options[key] = val
            self._options_attr[key] = {'src': OptionAttr.SUPPLIED}

        for key, val in supplied_as_default.items():
            self._options[key] = val
            self._options_attr[key] = {'src': OptionAttr.SUPPLIED_DEFAULT}

        for key, val in default.items():
            self._options[key] = val
            self._options_attr[key] = {'src': OptionAttr.DEFAULT}

    def _convert_options(self):
        options = {}
        options_attr = {}

        for key, val in self._options.items():
            type_ = self._options_attr[key]
            if key not in self._mapping:
                options[key] = val
                options_attr[key] = type_
                continue
            split_ = self._mapping[key].split('.')

            root = options
            root_attr = options_attr
            max_split = len(split_) - 1
            for idx, part in enumerate(split_):
                if part not in root:
                    if idx == max_split:
                        root[part] = val
                        root_attr[part] = type_
                    else:
                        root[part] = dict()
                        root_attr[part] = dict()
                root = root[part]
                root_attr = root_attr[part]

        self._options = Box(options, frozen_box=True)
        self._options_attr = Box(options_attr, frozen_box=True)

    def __getattr__(self, key):
        if key in self._options:
            return self._options[key]
        else:
            raise AttributeError('\'{}\' object has no attribute \'{}\''
                                 ''.format(__class__.__name__,
                                           key))

    def __setattr__(self, key, value):
        if not self.__initing:
            if key not in self._options:
                raise AttributeError('\'{}\' object has no attribute \'{}\''
                                     ''.format(__class__.__name__,
                                               key))

            if key not in self.__allow_modify:
                raise AttributeError('can\'t set attribute')

        if key in {'_options', '_options_attr', '_mapping', '_parse_function',
                   '_Options__initing'}:
            self.__dict__[key] = value
            return

        raise Exception('Unhandled setattr {}: {}'.format(key, value))

    def _parse_cmd_args(self):
        par = self._parse_function()
        supplied = par.parse_supplied_args()
        supplied_as_default = par.parse_supplied_default_args()
        default = par.parse_default_args()
        return (vars(supplied), vars(supplied_as_default), vars(default))
