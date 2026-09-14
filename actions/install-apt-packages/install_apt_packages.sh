#!/usr/bin/env bash
set -euo pipefail

: "${APT_PACKAGES:?Set APT_PACKAGES to a whitespace-separated package list}"
read -r -a packages <<< "${APT_PACKAGES//$'\n'/ }"
if ((${#packages[@]} == 0)); then
  echo 'At least one package is required' >&2
  exit 2
fi
for package in "${packages[@]}"; do
  if [[ ! "$package" =~ ^[a-z0-9][a-z0-9+.-]*(:[a-z0-9-]+)?(=[A-Za-z0-9.+:~_-]+)?$ ]]; then
    echo 'Invalid package name or version' >&2
    exit 2
  fi
done

# Use a reachable Ubuntu mirror while retaining archive signature checks.
for source in /etc/apt/sources.list /etc/apt/sources.list.d/ubuntu.sources; do
  if test -f "$source"; then
    sudo sed -i \
      -e 's|https\?://archive.ubuntu.com/ubuntu|https://mirrors.edge.kernel.org/ubuntu|g' \
      -e 's|https\?://security.ubuntu.com/ubuntu|https://mirrors.edge.kernel.org/ubuntu|g' \
      "$source"
  fi
done
apt_options=(-o APT::Update::Error-Mode=any -o Acquire::Retries=3 -o Acquire::https::Timeout=20)
sudo apt-get "${apt_options[@]}" update -qq
sudo apt-get "${apt_options[@]}" install -y --no-install-recommends -- "${packages[@]}"
