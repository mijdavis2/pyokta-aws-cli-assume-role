# pyokta-aws-cli-assume-role

| branch | status |
|:-------|:-------|
| master |[![build](https://travis-ci.org/mijdavis2/pyokta-aws-cli-assume-role.svg?branch=master)](https://travis-ci.org/mijdavis2/pyokta-aws-cli-assume-role)|


Okta AWS CLI Assume Role Tool for Humans

If you login to AWS via Okta SAML federation and assume an iam role, this tool will help you easily achieve pragmatic access to AWS via the aws cli. Also helpful for running **terraform** and **packer**

> Replacement for [okta-aws-cli-assume-role]

> NOTICE: Though this project works in a limited capacity, keep in mind that this project is still in rapid development phase. No security audits have been performed.

## Why a new tool?

My cohorts and I wanted a tool that was easy to install and use, easy to configure, easy to improve and maintain, and supported multi-tenancy.

## Requirements

- python 3.5+
- pip
- awscli: `pip install awscli` -- Though it's not required to run the tool, the tool exists to support friendly awscli auth via Okta.

## Install

```pip install pyokta-aws-cli-assume-role```

## Configure

Run `pyokta-aws configure` for interactive configuration (WIP).

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

- *region*: Target AWS region
- *okta_org*: Base domain for okta org
- *okta_aws_app_url*: Okta app url (can be found by hovering over aws app chiclet)
- *aws_role_to_assume*: Found in AWS console under `IAM > Roles > <role_id>`. Look for `ARN`.
- *aws_idp*: Found in AWS console under `IAM > Identity Providers > <provider_id>`. Look for `ARN`.
- *username*: Okta username
- *password*: `<it is recommended to keep this blank>`
- *sts_duration*: Duration (in seconds) to keep token alive. Max duration found in `IAM > Identity Providers > <provider_id>`.

## Usage

Basic usage `pyokta-aws auth --profile <aws_profile>`.

See `pyokta-aws --help` for all supported usage.

Configuration can be input via cli args, env vars, or the pyokta-aws config file described above. Configuration takes presidence as follows: `cli args > env vars > config file`.

## How it works

The main `pyokta-aws auth` command authenticates with Okta and aquires a temporary set of credentials from AWS STS. These credentials get written to you local aws credentials file. This allows the awscli and other tools like `terraform` and `packer` to run as expected.

> Before auth happens, your local aws cli config profile is updated via the profile and region set in the pyokta-aws config. Treat you pyokta-aws config file as the single source of truth for aws cli config when authenticating with Okta.

## Roadmap:
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
- [ ] interactive initial config :children_crossing:
- [ ] readthedocs :pencil:
- [ ] tests :white_check_mark:
- [ ] windows support :checkered_flag:
- [ ] ci/cd (deploy to pypi)?
- [ ] aws role list selection in interactive mode :children_crossing:
- [ ] okta 2fa (others)
- [ ] use context managers to auto-cancel okta verifications on cancel

[okta-aws-cli-assume-role]: https://github.com/oktadeveloper/okta-aws-cli-assume-role
