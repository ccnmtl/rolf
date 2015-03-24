#!/usr/bin/env python
import os
import sys
import subprocess
import shutil

pwd = os.path.abspath(os.path.dirname(__file__))
vedir = os.path.abspath(os.path.join(pwd, "ve"))

if os.path.exists(vedir):
    shutil.rmtree(vedir)

virtualenv_support_dir = os.path.abspath(
    os.path.join(
        pwd, "requirements", "virtualenv_support"))

ret = subprocess.call(["python", "virtualenv.py",
                       "--extra-search-dir=%s" % virtualenv_support_dir,
                       "--never-download",
                       vedir])
if ret:
    exit(ret)

ret = subprocess.call(
    [os.path.join(vedir, 'bin', 'pip'), "install",
     "--index-url=https://pypi.ccnmtl.columbia.edu/",
     "wheel==0.24.0"])

if ret:
    exit(ret)

ret = subprocess.call(
    [os.path.join(vedir, 'bin', 'pip'), "install",
     "--use-wheel",
     "--no-deps",
     "--index-url=https://pypi.ccnmtl.columbia.edu/",
     "--requirement", os.path.join(pwd, "requirements.txt")])

if ret:
    exit(ret)

ret = subprocess.call(["python", "virtualenv.py", "--relocatable", vedir])
# --relocatable always complains about activate.csh, which we don't really
# care about. but it means we need to ignore its error messages
