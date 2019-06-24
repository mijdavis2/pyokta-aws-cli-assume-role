# pyokta-aws-cli-assume-role

| branch | status |
|:-------|:-------|
| master |[![build](https://travis-ci.org/mijdavis2/pyokta-aws-cli-assume-role.svg?branch=master)](https://travis-ci.org/mijdavis2/pyokta-aws-cli-assume-role)|

The python tool to use the aws cli via assume role and Okta authentication.

WIP - This project is still in rapid initial development phase.

## Roadmap:
- [x] pypi package
- [x] cli and settings loaders
- [x] support multi-tenant settings
- [x] ci (testing) :construction_worker:
- [x] okta auth
- [x] okta 2fa (sms)
- [x] get saml from okta app
- [x] aws auth via okta auth
- [x] setup aws config if not previously setup
- [ ] windows support :checkered_flag:
- [ ] ci/cd (deploy to pypi)?
- [ ] aws role list selection in interactive mode :children_crossing:
- [ ] okta 2fa (others)
- [ ] use context managers to auto-cancel okta verifications on cancel
