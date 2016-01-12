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


# needs readline-devel, bzip2-devel, sqlite-devel, openssl-devel

sudo -u vagrant sh -c 'curl -sL https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash &>/dev/null'

sudo -u vagrant cat >> /home/vagrant/.bashrc << 'EOF'
export PYENV_ROOT="${HOME}/.pyenv"

if [ -d "${PYENV_ROOT}" ]; then
  export PATH="${PYENV_ROOT}/bin:${PATH}"
  eval "$(pyenv init -)" ; eval "$(pyenv virtualenv-init -)"
  env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install --skip-existing 2.7.6
fi
EOF

env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install --skip-existing 2.7.6

#REPLACE github.com below if code is in a local repo
sudo -u vagrant sh -c 'ssh-keyscan -H github.com > /home/vagrant/.ssh/known_hosts'
