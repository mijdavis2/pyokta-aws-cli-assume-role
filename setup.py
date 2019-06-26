import setuptools

import pyokta_aws

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name=pyokta_aws.__title__,
    version=pyokta_aws.__version__,
    author=pyokta_aws.__author__,
    author_email=pyokta_aws.__email__,
    description=pyokta_aws.__summary__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=pyokta_aws.__url__,
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    python_requires='>=3.5',
    install_requires=[
        'boto3 >= 1.9',
        'configobj >= 5.0',
        'pyquery >= 1.4',
        'requests >= 2.22',
        # packaging reqs
        'pkginfo >= 1.5',
        'setuptools',
    ],
    py_modules=['pyokta_aws'],
    entry_points={
        'pyokta_aws.registered_commands': [
            'auth = pyokta_aws.commands.auth:main',
            'configure = pyokta_aws.commands.configure:main',
        ],
        'console_scripts': [
            'pyokta-aws = pyokta_aws.__main__:main',
        ]
    }
)
