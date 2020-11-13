#! /usr/bin/env python3

"""This script will install kubectl latest on GNU/Linux."""

import os
import requests
import urllib.request
import urllib.error
import shutil
import subprocess
from sys import platform
from requests.models import Response


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

    def get_kubectl(self) -> object:
        """Download and install the latest kubectl for Linux."""
        # 1. download kubectl to temporary location
        print(f'[STEP 1]: Beginning file download of the latest kubectl version'
              f' \'{self.latest_kube.text}\' from:\n{self.url}')
        try:
            urllib.request.urlretrieve(self.url, self.templocation)
        except urllib.error.URLError as e:
            exit(e.reason)

        # 2. make the downloaded file executable (775)
        print(f'[STEP 2]: Making the downloaded binary file \''
              f'{self.templocation}\' executable (mode 775)')
        os.chmod(self.templocation, 0o775)


def main():
    this_setup = KubectlInstallation()
    this_setup.get_kubectl()


if __name__ == '__main__':
    main()
