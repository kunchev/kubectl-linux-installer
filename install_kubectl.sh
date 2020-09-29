#!/usr/bin/env bash

# Install the latest kubectl binary in Linux

set -eo pipefail

main_url="https://storage.googleapis.com/kubernetes-release/release/"
latest_vers_url="${main_url}stable.txt"


# check operating system:
on_name=$(uname -s | tr '[:upper]' '[:lower]')
if [ "${os_name}" = "linux" ]; then
  arch=$(uname -m | tr '[:upper]' '[:lower]')
  if echo "${arch}" | grep -q -E 'x86_64'
  then
    platform="linux64"
  elif
