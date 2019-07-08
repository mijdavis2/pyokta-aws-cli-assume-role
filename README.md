<div align="center">

<a href="https://github.com/mijdavis2/pyokta-aws-cli-assume-role/tree/master">
    <img src="https://raw.githubusercontent.com/mijdavis2/pyokta-aws-cli-assume-role/master/assets/pyokta-aws-cli-assume-role.png" width=300\>
</a>

<h3>pyokta-aws-cli-assume-role</h3>

[![pypi version](https://pypi.in/v/pyokta-aws-cli-assume-role)](https://pypi.org/project/pyokta-aws-cli-assume-role)
[![pypi downloads](https://pypi.in/d/pyokta-aws-cli-assume-role)](https://pypi.org/project/pyokta-aws-cli-assume-role)
[![source](https://img.shields.io/badge/source-github-teal.svg)](https://shields.io/)
[![build](https://travis-ci.org/mijdavis2/pyokta-aws-cli-assume-role.svg?branch=master)](https://travis-ci.org/mijdavis2/pyokta-aws-cli-assume-role) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

---

Okta-AWS auth tool for humans
</div>

If you login to AWS via Okta SAML federation and assume an IAM role, this tool will help you easily achieve pragmatic access to AWS via the [aws cli] and [SDKs]. Also helpful for running [terraform]/[terragrunt], [packer], and [credstash] with iam roles.

> Replaces [okta-aws-cli-assume-role]

**NOTICE**: This project is still in rapid development phase. You can [subscribe to new release notifications via github]. Upgrade to the most recent release via `pip install --upgrade --no-cache-dir pyokta-aws-cli-assume-role`.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
# Table of Contents

- [Support](#support)
- [Why a new tool?](#why-a-new-tool)
- [Getting Started](#getting-started)
  - [Requirements](#requirements)
  - [Install](#install)
  - [Configure](#configure)
    - [Interactive](#interactive)
    - [Config file](#config-file)
- [Usage](#usage)
- [How it works](#how-it-works)
- [Roadmap](#roadmap)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Support

- MFA: SMS
- MFA: Okta mobile app
- All major operating systems (Linux, Windows, Mac).

Please [create an issue] for bugs or feature requests (if not already mentioned in roadmap or other issues).

# Why a new tool?

## Benefits over existing tool

- No PATH changes or overriding aws executables - you're still using native awscli.
- Supports multiple tenants.
- One consistent config file for all tenants.
- Env var changes are 100% optional.
- Cleaner https error output.
- Easy to install.
- JVM not required.

## Existing tool features missing in this tool

These features are planned to be supported in the near future. See [roadmap](#roadmap).

- [x] ~~Interactively select from multiple mfa options.~~
- [x] ~~Set desired mfa option via cli args, env vars, or config file.~~
- [x] ~~Support Okta mobile app mfa (currently only sms is verified to work).~~
- [x] ~~Cross-OS compatibility~~
- [ ] Okta token caching/refresh.

# Getting Started

## Requirements

- python 3.5+
- pip
- awscli: `pip install --upgrade awscli`

## Install

```pip install --upgrade --no-cache-dir pyokta-aws-cli-assume-role```

---

To check the install and output the current version, run:
```pyokta-aws --version```

## Configure

Configuration can be input via cli args, env vars, or the pyokta-aws config file described above. Configuration takes presidence as follows: `cli args > env vars > config file`. For all supported args and env vars, run `pyokta-aws --help` and `pyokta-aws [COMMAND] --help`.

### Interactive

Run `pyokta-aws configure` for interactive configuration (WIP).

### Config file

Default configuration file location is `~/.pyokta_aws/config`.

Example config file:
```
[my-aws-profile]
region = us-east-1
okta_org = example.okta.com
okta_aws_app_url = https://example.okta.com/home/amazon_aws/123456789
aws_role_to_assume = arn:aws:iam::987654321:role/AWSAdmin
aws_idp = arn:aws:iam::987654321:saml-provider/Okta
username = johnsmith
sts_duration = 14400
mfa_choice = sms
```

- **region**: Target AWS region. (Will override default region in target aws cli profile)
- **okta_org**: Base domain for okta org.
- **okta_aws_app_url**: Okta app url (can be found by hovering over aws app chiclet).
- **aws_role_to_assume**: Found in AWS console under `IAM > Roles > <role_id>`. Look for `ARN`.
- **aws_idp**: Found in AWS console under `IAM > Identity Providers > <provider_id>`. Look for `ARN`.
- **username**: (optional) Okta username.
- **password**: (optional) _it is recommended to omit or leave it blank_ and enter it interactively.
- **sts_duration**: (optional) Duration (in seconds) to keep token alive. Max duration found in `IAM > Identity Providers > <provider_id>`.
- **mfa_choice**: (optional) If you have multiple MFA factors registered, you can skip interactive factor selection by setting preferred mfa choice. Current options are `sms` and `app` (i.e. [Okta mobile app]).

# Usage

To authenticate via okta and assume an aws profile, run:

```pyokta-aws auth --profile <aws_profile>```

---

For all supported auth args, run `pyokta-aws auth --help`.

For all supported commands, run `pyokta-aws --help`.

# How it works

The main `pyokta-aws auth` command authenticates with Okta and aquires a temporary set of credentials from AWS STS. These credentials get written to your local aws credentials file. This allows the [aws cli] and other tools like [terraform]/[terragrunt], [packer], and [credstash] to run as expected without needing to override the awscli executable or export environment variables.

> Before auth happens, your local aws cli config profile is updated via the profile and region set in the pyokta-aws config. Treat your pyokta-aws config file as the single source of truth for aws cli config when authenticating with Okta.

# Roadmap
- [x] ~~pypi package~~
- [x] ~~cli and settings loaders~~
- [x] ~~support multi-tenant settings~~
- [x] ~~ci (testing) [:construction_worker:]~~
- [x] ~~okta auth~~
- [x] ~~okta 2fa (sms)~~
- [x] ~~get saml from okta app~~
- [x] ~~aws auth via okta auth~~
- [x] ~~aws config if not previously setup~~
- [x] ~~basic documentation [:pencil:]~~
- [x] ~~support multiple 2fa methods~~
- [ ] interactive initial config [:children_crossing:]
- [ ] readthedocs [:pencil:]
- [ ] many more tests
- [x] ~~windows support [:checkered_flag:]~~
- [ ] ci/cd (deploy to pypi)?
- [ ] aws role list selection in interactive mode [:children_crossing:]
- [x] ~~okta 2fa (okta mobile app)~~
- [ ] push notification 2fa
- [ ] use context managers to auto-cancel okta verifications on cancel
- [ ] okta token cache/refresh to speedup multiple logins [:children_crossing:]

[:dog:]

[subscribe to new release notifications via github]: https://github.com/mijdavis2/pyokta-aws-cli-assume-role
[okta-aws-cli-assume-role]: https://github.com/oktadeveloper/okta-aws-cli-assume-role
[aws cli]: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html
[SDKs]: https://aws.amazon.com/tools/
[terraform]: https://www.terraform.io/intro/index.html
[terragrunt]: https://github.com/gruntwork-io/terragrunt
[packer]: https://www.packer.io/intro/index.html
[credstash]: https://github.com/fugue/credstash
[create an issue]: https://github.com/mijdavis2/pyokta-aws-cli-assume-role/issues
[okta mobile app]: https://help.okta.com/en/prod/Content/Topics/ReleaseNotes/mobile-release-status.htm#Release
[:construction_worker:]: https://youtu.be/dm2glu3WLGk?t=36
[:pencil:]: https://youtu.be/hHW1oY26kxQ
[:checkered_flag:]: https://youtu.be/HrPRtYvCvZI
[:children_crossing:]: https://youtu.be/dQw4w9WgXcQ
[:dog:]: https://omfgdogs.com/
