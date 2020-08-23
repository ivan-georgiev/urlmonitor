#!/usr/bin/env python3

import subprocess

# git config --local include.path ../.gitconfig
subprocess.run(['git', 'config', '--local', 'include.path',
                '../.gitconfig'], shell=True, check=True, capture_output=True)
