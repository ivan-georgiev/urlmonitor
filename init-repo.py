#!/usr/bin/env python3

import subprocess


def main():
    """
    Main method of init repo.
    """
    subprocess.run(['git', 'config', '--local', 'include.path', '../.gitconfig'],
                   shell=True, check=True, capture_output=True
                   )


if __name__ == '__main__':
    main()
