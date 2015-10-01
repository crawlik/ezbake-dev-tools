#!/usr/bin/env python
#
#   Copyright (C) 2015 Computer Sciences Corporation
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from setuptools import setup, find_packages

setup(
    name='ezbake-migration',
    version='2.1',
    description='Libraries to annotate conventional data with authorization data.',
    license='Apache License 2.0',
    author='EzBake Developers',
    author_email='coders@infochimps.com',
    namespace_packages=['ezbake'],
    packages=find_packages('lib', exclude=['test*']),
    package_dir={'': 'lib'},
    install_requires=[
        'elasticsearch==1.7.0',
        'ezbake-base-thrift==2.1',
        'ezbake-configuration-constants==2.1',
        'ezbake-discovery==2.1',
        'ezbake-thrift-utils==2.1',
        'kazoo==2.2.1',
        'six==1.9.0',
        'thrift==0.9.1',
        'urllib3==1.12',
        'wheel==0.24.0',
    ]
)
