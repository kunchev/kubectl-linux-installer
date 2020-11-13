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
    this_setup = KubectlInstallation()
    this_setup.get_kubectl()


if __name__ == '__main__':
    main()
