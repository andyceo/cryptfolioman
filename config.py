#!/usr/bin/python3

import collections
import os
import pathlib
import sys
import yaml


def deep_dict_merge(d, merge_d):
    for k, v in merge_d.items():
        if k in d and isinstance(d[k], dict) and isinstance(merge_d[k], collections.Mapping):
            deep_dict_merge(d[k], merge_d[k])
        else:
            d[k] = merge_d[k]


cryptfolioman_config = os.path.dirname(os.path.abspath(sys.argv[0])) + "/config.yml"
user_config = str(pathlib.Path.home()) + "/.cryptfolioman"
config = {}

for ymlfilepath in [cryptfolioman_config, user_config]:
    if os.path.isfile(ymlfilepath):
        with open(ymlfilepath, 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
            if 'cryptfolioman' in cfg:
                cfg = cfg['cryptfolioman']
            deep_dict_merge(config, cfg)

# Write default user config if it is not exists
if not os.path.isfile(user_config):
    with open(user_config, 'w') as ymlfile:
        yaml.dump(config, ymlfile, default_flow_style=False)
