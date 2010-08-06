#!/usr/bin/env python
import os
import sys
import subprocess
import shutil

pwd = os.path.dirname(__file__)
vedir = os.path.join(pwd,"ve")

if os.path.exists(vedir):
    shutil.rmtree(vedir)

subprocess.call(["python",os.path.join(pwd,"pip.py"),"install",
                 "-E",os.path.join(pwd,"ve"),
                 "--enable-site-packages",
                 "--requirement",os.path.join(pwd,"requirements/apps.txt")])
subprocess.call([os.path.join(vedir,"bin/easy_install"),
                 os.path.join(pwd,"requirements/eggs/egenix_mx_base-3.1.3-py2.6-linux-x86_64.egg")])

subprocess.call([os.path.join(vedir,"bin/easy_install"),
                 os.path.join(pwd,"requirements/eggs/SilverCity-0.9.7-py2.6-linux-x86_64.egg")])
