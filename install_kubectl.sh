#!/usr/bin/env bash
set -eo pipefail

# Install the latest kubectl binary in Linux
#
# - The 'kubectl' tool controls the Kubernetes cluster:
# https://kubernetes.io/docs/reference/kubectl/kubectl/
# https://kubernetes.io/docs/reference/kubectl/overview/
#
# - Linux is a family of open-source Unix-like operating systems based on
# the Linux kernel:
# https://www.kernel.org/category/about.html


# define global scope variables
main_url="https://storage.googleapis.com/kubernetes-release/release/"
latest_vers_url="${main_url}stable.txt"
temp_dir="/tmp"
path_dir="/usr/local/bin/"


# check operating system:
on_name=$(uname -s | tr '[:upper]' '[:lower]')
if [ "${os_name}" = "linux" ]; then
  arch=$(uname -m | tr '[:upper]' '[:lower]')
  if echo "${arch}" | grep -q -E 'x86_64'
  then
    platform="linux64"
  elif echo "${arch}" | grep -q -E '(x86)|(i686)'
  then
    plafrorm="linux32"
    echo ">> Running linux32, please run 64 bit version. Exiting..."
    exit 1
  elif echo "${arch}" | grep -q -E 'ppc64le'
  then
    plafrorm="ppc64le"
  else
    echo ">> Unsupported Linux arch: ${arch}. Exiting..."
    exit 1
  fi
else
  echo ">> Unrecognized Linux platform detected: ${os_name}. Exiting..."
  exit 1
fi

# check if curl is present on the system:
if ! command -v curl &> /dev/null; then
  echo ">> curl could not be found. Exiting..."
  exit 1
fi

# make sure to always use sudo, if not running script as root:
[ "$(id -u)" -ne 0 ] && SUDO=sudo || SUDO=""

# download the kubectl binary:
cd ${temp_dir} || exit
echo ">> Downloading kubectl $(curl -s ${latest_ver_url}) ..."
if curl -s -LO "${main_url}"$(curl -s ${latest_ver_url})/bin/linux/amd64/kubectl"; then
  echo ">> Download complete."
else
  echo ">> Download failed. Please check your network connection. Exiting..."
  exit 1
fi

# make the kubectl binary executable
chmod +x ./kubectl

# move the binary from the current working folder in PATH:
if $SUDO sudo mv ./kubectl ${path_dir}kubectl; then
  echo ">> Install complete."
  exit 0
else
  echo ">> Install failed!"
  exit 1
fi
