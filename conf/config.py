#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jerry Bai'

'''
Setting up configurations
'''

import config_default


class Dict(dict):
    '''
    Support direct object.key=value access
    :param dict:
    :return:
    '''

    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


def toDict(d):
    D = Dict()
    for k, v in d.items():
        D[k] = toDict(v) if isinstance(v, dict) else v
    return D


def merge(default, override):
    r = {}
    for k, v in default.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r


configs = config_default.configs

try:
    import config_override

    configs = merge(configs, config_override.configs)
except ImportError:
    pass

# Convert all config items to JSON format
configs = toDict(configs)
