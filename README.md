<div align="center">

<img src="assets/pyokta-aws-cli-assume-role.png" width=300\>

<h3>pyokta-aws-cli-assume-role</h3>

[![build](https://travis-ci.org/mijdavis2/pyokta-aws-cli-assume-role.svg?branch=master)](https://travis-ci.org/mijdavis2/pyokta-aws-cli-assume-role) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

---

Okta-AWS auth tool for humans
</div>

If you login to AWS via Okta SAML federation and assume an IAM role, this tool will help you easily achieve pragmatic access to AWS via the [aws cli] and [SDKs]. Also helpful for running [terraform]/[terragrunt], [packer], and [credstash] with iam roles.

> Replaces [okta-aws-cli-assume-role]

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
# Table of Contents

- [Why a new tool?](#why-a-new-tool)
- [Getting Started](#getting-started)
  - [Requirements](#requirements)
  - [Install](#install)
  - [Configure](#configure)
- [Usage](#usage)
- [How it works](#how-it-works)
- [Roadmap](#roadmap)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

> NOTICE: Though this project works in a limited capacity, keep in mind that this project is still in rapid development phase. No security audits have been performed.

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

- Interactively select from multiple mfa options.
- Set desired mfa option via cli args, env vars, or config file.
- Support Okta Verify app mfa (currently only sms is verified to work).
- Cross-OS compatibility testing (current focus is Linux systems).
- Okta token caching/refresh.

# Getting Started

## Requirements

- python 3.5+
- pip
- awscli: `pip install awscli` -- Though it's not required to run the tool, the tool exists to support friendly awscli auth via Okta.

## Install

```pip install pyokta-aws-cli-assume-role```

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
password = <it is recommended to keep this blank>
sts_duration = 14400
```

- **region**: Target AWS region. (Will override default region in target aws cli profile)
- **okta_org**: Base domain for okta org.
- **okta_aws_app_url**: Okta app url (can be found by hovering over aws app chiclet).
- **aws_role_to_assume**: Found in AWS console under `IAM > Roles > <role_id>`. Look for `ARN`.
- **aws_idp**: Found in AWS console under `IAM > Identity Providers > <provider_id>`. Look for `ARN`.
- **username**: Okta username.
- **password**: _it is recommended to keep this blank_ and enter it interactively.
- **sts_duration**: Duration (in seconds) to keep token alive. Max duration found in `IAM > Identity Providers > <provider_id>`.

# Usage

The main command is `pyokta-aws auth`.

Basic usage: `pyokta-aws auth --profile <aws_profile>`.

For supported args, run `pyokta-aws auth --help`.

# How it works

The main `pyokta-aws auth` command authenticates with Okta and aquires a temporary set of credentials from AWS STS. These credentials get written to you local aws credentials file. This allows the awscli and other tools like [terraform]/[terragrunt], [packer], and [credstash] to run as expected without needing to override the awscli executable or export environment variables.

> Before auth happens, your local aws cli config profile is updated via the profile and region set in the pyokta-aws config. Treat you pyokta-aws config file as the single source of truth for aws cli config when authenticating with Okta.

# Roadmap
- [x] pypi package
- [x] cli and settings loaders
- [x] support multi-tenant settings
- [x] ci (testing) :construction_worker:
- [x] okta auth
- [x] okta 2fa (sms)
- [x] get saml from okta app
- [x] aws auth via okta auth
- [x] aws config if not previously setup
- [x] basic documentation :pencil:
- [ ] support multiple 2fa methods
- [ ] interactive initial config :children_crossing:
- [ ] readthedocs :pencil:
- [ ] tests :white_check_mark:
- [ ] windows support :checkered_flag:
- [ ] ci/cd (deploy to pypi)?
- [ ] aws role list selection in interactive mode :children_crossing:
- [ ] okta 2fa (others)
- [ ] use context managers to auto-cancel okta verifications on cancel
- [ ] okta token cache/refresh to speedup multiple logins :children_crossing:

[okta-aws-cli-assume-role]: https://github.com/oktadeveloper/okta-aws-cli-assume-role
[aws cli]: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html
[SDKs]: https://aws.amazon.com/tools/
[terraform]: https://www.terraform.io/intro/index.html
[terragrunt]: https://github.com/gruntwork-io/terragrunt
[packer]: https://www.packer.io/intro/index.html
[credstash]: https://github.com/fugue/credstash
