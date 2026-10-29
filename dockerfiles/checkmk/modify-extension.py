#!/usr/bin/env python3
#
#  modify extension configuration

from pathlib import Path
from pprint import pformat
from sys import argv, \
    exit

AUTHOR = 'Timothe Stoifl <timothe.stoifl@outlook.com>'
DOWNLOAD_URL = 'https://github.com/timothestoifl24/checkmk-agent-plugin-yum/releases'
YUM_AGENT_PATH = Path('/omd/sites/cmk/local/share/check_mk/agents/plugins/yum')

# only do stuff if repo path and config file path are given
if len(argv) > 2:
    repo_path = Path(argv[1])
    package_file_path = Path(argv[2])

    # version is maintained manually in the VERSION file at the repository root
    version_file_path = repo_path / 'VERSION'
    if not version_file_path.is_file():
        print(f'Version file {version_file_path} does not exist. :-(')
        exit(1)
    version = version_file_path.read_text().strip()
    if not version:
        print(f'Version file {version_file_path} is empty. :-(')
        exit(1)
    print(f'Version {version}')

    if package_file_path.is_file():
        # open package config file
        package_config = eval(package_file_path.read_text())

        # modify package config
        package_config['author'] = AUTHOR
        package_config['description'] = 'Checks for updates on RPM-based distributions via yum/dnf.'
        package_config['download_url'] = DOWNLOAD_URL
        package_config['title'] = 'YUM Update Check'
        package_config['version'] = version
        package_config['version.min_required'] = '2.3.0'

        # write package config file - nicely formatted with pformat
        package_file_path.write_text(pformat(package_config, indent=4))
    else:
        print(f'Package configuration file path {package_file_path} does not exist. :-(')
        exit(1)

    # update version number inside the yum agent plugin itself
    if YUM_AGENT_PATH.exists():
        content = YUM_AGENT_PATH.read_text()
        YUM_AGENT_PATH.write_text(content.replace('CMK_VERSION="0.0.0"', f'CMK_VERSION="{version}"'))
    else:
        print(f'File not found: {YUM_AGENT_PATH}')

else:
    print('Repository path or package configuration file path is missing at all. :-(')
    exit(1)
