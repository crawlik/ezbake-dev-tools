#!/bin/bash
#   Copyright (C) 2013-2015 Computer Sciences Corporation
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


THRIFT_VERSION="0.9.1"
THRIFT_INSTALLED=$(thrift -version 2>/dev/null | grep -F "${THRIFT_VERSION}" | wc -l)
CHECKSUM="d2e46148f6e800a9492dbd848c66ab6e"

if [ "${THRIFT_INSTALLED}" -ne 1 ]; then
    if [ -f thrift-${THRIFT_VERSION}.tar.gz ];
    then
        echo "thrift-${THRIFT_VERSION}.tar.gz exists, skipping download";
    else
        wget http://archive.apache.org/dist/thrift/${THRIFT_VERSION}/thrift-${THRIFT_VERSION}.tar.gz
        if [ "$CHECKSUM" != "$(md5sum "thrift-${THRIFT_VERSION}.tar.gz"  | grep --only-matching -m 1 '^[0-9a-f]*')" ];then
            echo "ERROR: invalid maven binary checksum" >&2
            exit 1
        fi
    fi
    if [ -d thrift-${THRIFT_VERSION} ];
    then
        rm -rf thrift-${THRIFT_VERSION}
    fi
    tar xzvf thrift-${THRIFT_VERSION}.tar.gz
    cd thrift-${THRIFT_VERSION}
    patch -p1 < /vagrant/provisioning/thrift_0.9.1_patches_2201_667_1755_2045_2229_.patch
    ./configure --without-ruby --without-tests
    make
    sudo make install
    cd lib/py
    sudo env PATH=$PATH pip install -U .
    cd ../../..
else
    echo "Thrift appears to be installed, skipping Thrift ${THRIFT_VERSION} build"
fi

cd ..

