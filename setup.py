import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyokta-aws-cli-assume-role",
    version="0.0.1",
    author="mijdavis2",
    author_email="",
    description="The python tool to use the aws cli via assume role and Okta authentication.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mijdavis2/pyokta-aws-cli-assume-role",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
