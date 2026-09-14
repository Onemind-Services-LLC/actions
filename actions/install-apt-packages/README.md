# Install APT Packages

Installs Ubuntu packages through the kernel.org mirror over HTTPS. Ubuntu
archive signatures remain mandatory; failed index refreshes stop installation.
Both index and package downloads use retries and a 20-second HTTPS timeout.

```yaml
- name: Install Verification Tools
  uses: Onemind-Services-LLC/actions/actions/install-apt-packages@master
  with:
    packages: shellcheck skopeo
```

Pin the action to a reviewed commit in production workflows. The required
`packages` input accepts whitespace-separated package names, architecture
qualifiers and exact versions such as `skopeo:amd64=1.13.3+ds1-1build2`.
Option-like arguments and empty lists are rejected before changing APT sources.
Requires an Ubuntu runner with Bash and passwordless sudo.
