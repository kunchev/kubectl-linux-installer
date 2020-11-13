#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""This script will install kubectl latest on GNU/Linux.

- The 'kubectl' tool controls the Kubernetes cluster:
https://kubernetes.io/docs/reference/kubectl/kubectl/
https://kubernetes.io/docs/reference/kubectl/overview/

- Linux is a family of open-source Unix-like operating systems based on
the Linux kernel:
https://www.kernel.org/category/about.html

- Python is an interpreted, high-level, dynamically typed,
garbage-collected and general-purpose programming language:
https://en.wikipedia.org/wiki/Python_Software_Foundation_License
https://docs.python.org/3/license.html
"""

# TODO: Implement color print based on message type - green for ok,
#  red for error messages and blue for informational messages

__author__ = 'Petyo Kunchev'
__version__ = '1.0.0'
__maintainer__ = 'Petyo Kunchev'
__email__ = 'ptkunchev@gmail.com'
__license__ = 'MIT'

import os
import urllib.request
import urllib.error
import shutil
import subprocess
from sys import platform

try:
    import requests
    from requests.models import Response
except ModuleNotFoundError as err:
    print('Please install the required modules.')
    exit(err)


class KubectlInstallation:
    """kubectl installation class"""

    # URL with the latest kubectl version string
    version_url: str = 'https://storage.googleapis.com/kubernetes-release' \
                       '/release/stable.txt'

    # get the latest version into a variable
    latest_kube: Response = requests.get(version_url)

    # construct the kubectl latest download URL
    url: str = 'https://storage.googleapis.com/kubernetes-release/release/' + \
               latest_kube.text + '/bin/linux/amd64/kubectl'

    # local temporary download location
    templocation: str = '/tmp/kubectl'

    # local folder to move the kubectl binary package (must be in $PATH)
    binlocation: str = '/usr/local/bin/kubectl'

    @property
    def running_os(self) -> object:
        """:return: the running operating system"""
        return platform

    @property
    def running_id(self) -> object:
        """:return: the running user ID"""
        return os.getuid()

    def get_kubectl(self):
        """Download and install the latest kubectl for Linux."""

        # 1. download kubectl to temporary location
        print(f'[STEP 1]: Starting download of the latest kubectl version'
              f' \'{self.latest_kube.text}\' from:\n{self.url}')
        try:
            urllib.request.urlretrieve(self.url, self.templocation)
        except urllib.error.URLError as e:
            exit(e.reason)

        # 2. make the downloaded file executable (775)
        print(f'[STEP 2]: Making the downloaded binary file \''
              f'{self.templocation}\' executable (mode 775)')
        os.chmod(self.templocation, 0o775)

        # 3. move the downloaded file to the desired bin folder
        print(f'[STEP 3]: Moving \'{self.templocation}\' to the \''
              f'{self.binlocation}\' destination')
        shutil.move(self.templocation, self.binlocation)

        # 4. verify the installed version of kubectl
        print('[STEP 4]: Verifying the kubectl installed version:')
        verify_kubectl_version = subprocess.run([self.binlocation, 'version',
                                                 '--client'])
        print(f'[STEP 5]: Exit code: {verify_kubectl_version.returncode}')


def main():
    """Wrap up everything into the main function."""

    # create object from the KubectlInstallation class
    this_setup = KubectlInstallation()

    # define the required operating system (Linux)
    rq_os: str = 'linux'

    # define required user id (root)
    rq_id: str = '0'

    # get currently running os
    rn_os: str = str(this_setup.running_os)

    # get currently running user
    rn_id: str = str(this_setup.running_id)

    # check if operating system and user id requirements are met
    if rn_os != rq_os or rn_id != rq_id:
        exit(f'[ERROR]: Running on {rn_os} with {rn_id}, must run on {rq_os} '
             f'with user id {rq_id} please check. Exiting...')
    else:
        # if conditions are met, run the installation
        print(f'Install version: {this_setup.latest_kube.text}')
        print(f'Operating system is: {rn_os}')
        print(f'User ID is: {rn_id}')
        this_setup.get_kubectl()


if __name__ == '__main__':
    main()
