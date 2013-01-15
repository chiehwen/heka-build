#!/usr/bin/env python
from __future__ import print_function
from __future__ import with_statement

import json
import os.path
import sys


go_tmpl = """package main

import (
{0}
)
"""


def main():
    scriptname = "setup_pluginloader.py"
    fpath = "etc/plugin_packages.json"
    pkgs_key = "plugin_packages"
    if not os.path.exists(fpath):
        msg = "{0}: No '{1}' file, exiting.".format(scriptname, fpath)
        print(msg)
        sys.exit()

    with open(fpath) as pkgs_file:
        msg = "Reading Heka plugin packages from '{0} key in '{1}' file."
        print(msg.format(pkgs_key, fpath))
        pkgs_file_blob = pkgs_file.read()
        try:
            pkgs_data = json.loads(pkgs_file_blob)
        except ValueError, e:
            print("{0}: Error parsing '{1}' JSON:".format(scriptname, fpath))
            print("---> {0}".format(e))
            sys.exit(1)

    packages = pkgs_data.get(pkgs_key, [])
    outfile_path = ("src/github.com/mozilla-services/heka/hekad/"
                    "plugin_loader.go")
    if os.path.exists(outfile_path):
        os.remove(outfile_path)

    imports = "\n".join(['\t_ "{0}"'.format(package) for package in packages])
    print("Imports:\n{0}".format(imports))
    outfile_content = go_tmpl.format(imports)

    with open(outfile_path, "w") as outfile:
        outfile.write(outfile_content)


if __name__ == "__main__":
    main()
