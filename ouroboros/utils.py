# encoding: utf-8

import types

def merge(x,y):
    merged = dict(x,**y)

    xkeys = x.keys()

    for key in xkeys:
        if type(x[key]) is types.DictType and y.has_key(key):
            merged[key] = merge(x[key],y[key])

    return merged
