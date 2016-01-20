FROM centos:centos6
MAINTAINER Infochimps <coders@infochimps.com>

COPY RPM-GPG-KEY-PGDG-93 RPM-GPG-KEY-EPEL-6 /etc/pki/rpm-gpg/
COPY pgdg-93-centos.repo epel.repo /etc/yum.repos.d/
RUN yum clean all

RUN yum install -y wget
RUN yum install -y tar
RUN yum install -y gcc
RUN yum install -y libevent-devel-1.4.13-4.el6
RUN yum install -y libevent-headers-1.4.13-4.el6
RUN yum install -y gcc-c++
RUN yum install -y git
RUN yum install -y rpmdevtools
RUN yum install -y python-devel
RUN yum install -y ant
RUN yum install -y boost-devel
RUN yum install -y bison
RUN yum install -y zlib-devel
RUN yum install -y openssl-devel
RUN yum install -y libtool # |
RUN yum install -y byacc   # |
RUN yum install -y flex    # -> for thrift build
RUN yum install -y nodejs-grunt     # |
RUN yum install -y nodejs-grunt-cli # -> for nodejs build
RUN yum install -y postgresql93-devel # -> for postgres visibility extention
RUN yum install -y augeas  # |
RUN yum install -y mlocate # -> Misc tools
RUN yum -y groupinstall "Development Tools"
RUN yum install -y which
RUN yum install -y java-1.7.0-openjdk
RUN yum install -y java-1.7.0-openjdk-devel

# Upgrade autoconf
ENV AUTOCONF_VER 2.69
WORKDIR /tmp
RUN curl -L http://ftp.gnu.org/gnu/autoconf/autoconf-$AUTOCONF_VER.tar.gz | tar xz
WORKDIR autoconf-$AUTOCONF_VER
RUN ./configure --prefix=/usr
RUN make install

# Upgrade automake
ENV AUTOMAKE_VER 1.14
WORKDIR /tmp
RUN curl -L http://ftp.gnu.org/gnu/automake/automake-$AUTOMAKE_VER.tar.gz | tar xz
WORKDIR automake-$AUTOMAKE_VER
RUN ./configure --prefix=/usr
RUN make install

# Upgrade bison
ENV BISON_VER 2.5.1
WORKDIR /tmp
RUN curl -L http://ftp.gnu.org/gnu/bison/bison-$BISON_VER.tar.gz | tar xz
WORKDIR bison-$BISON_VER
RUN ./configure --prefix=/usr
RUN make install

WORKDIR /root

# setup maven
RUN curl -L -o apache-maven-3.3.3-bin.tar.gz http://apache.claz.org/maven/maven-3/3.3.3/binaries/apache-maven-3.3.3-bin.tar.gz
RUN echo '794b3b7961200c542a7292682d21ba36  apache-maven-3.3.3-bin.tar.gz' > apache-maven-3.3.3-bin.tar.gz.md5
RUN md5sum -c apache-maven-3.3.3-bin.tar.gz.md5
RUN tar zxf apache-maven-3.3.3-bin.tar.gz -C /opt
RUN ln -s /opt/apache-maven-3.3.3 /opt/apache-maven
RUN ln -s /opt/apache-maven/bin/mvn /usr/bin/mvn
RUN rm -fv apache-maven-3.3.3-bin.tar.gz*
RUN rm -fv *.log *.log.*

# ruby installation
RUN yum install -y ruby
RUN yum install -y rubygems
RUN yum install -y ruby-devel
RUN gem install --no-rdoc --no-ri cabin -v 0.7.1
RUN gem install --no-rdoc --no-ri fpm -v 1.3.3

# NodeJS
RUN yum install -y npm
RUN npm install -g bower

# make boost MT lib default one
RUN ln -sf /usr/lib64/libboost_thread-mt.so /usr/lib64/libboost_thread.so

# set JAVA_HOME globaly
RUN echo 'export JAVA_HOME=/usr/lib/jvm/java-1.7.0' >> /etc/bashrc

# setup user builder
ENV BUSER builder
RUN useradd $BUSER
WORKDIR /home/$BUSER

# Python installation
USER $BUSER
ENV PY_VERSION 2.7.6
RUN curl -sL https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
RUN echo "export PYENV_ROOT=${HOME}/.pyenv" >> /$HOME/.bashrc
RUN echo 'export PATH=${PYENV_ROOT}/bin:${PATH}' >> /$HOME/.bashrc
RUN echo 'eval "$(pyenv init -)" ; eval "$(pyenv virtualenv-init -)"' >> /$HOME/.bashrc
RUN env PYTHON_CONFIGURE_OPTS="--enable-shared" $HOME/.pyenv/bin/pyenv install --skip-existing $PY_VERSION
RUN echo 'pyenv shell ezenv' >> /$HOME/.bashrc

# install thrift
ENV THRIFT_VERSION 0.9.1
USER $BUSER
WORKDIR /tmp
RUN curl -Ls http://archive.apache.org/dist/thrift/${THRIFT_VERSION}/thrift-${THRIFT_VERSION}.tar.gz | tar xz
WORKDIR /tmp/thrift-${THRIFT_VERSION}
# not sure why that patch is needed but applying because original source was doing it
COPY thrift_${THRIFT_VERSION}_patches_2201_667_1755_2045_2229_.patch .
RUN patch -p1 < thrift_${THRIFT_VERSION}_patches_2201_667_1755_2045_2229_.patch
RUN ./configure --without-ruby --without-tests
RUN make
# install thrift libs as root
USER root
RUN make install
# install py thrift package
USER $BUSER
RUN source $HOME/.bashrc ;\
    pyenv virtualenv $PY_VERSION ezenv;\
    pyenv global ezenv
WORKDIR lib/py
RUN source $HOME/.bashrc ; pip install -U .

# install custom pyinstaller
# it has something to do with ability properly add nested imports, but sure
RUN git clone -b develop \
    https://github.com/infochimps-forks/pyinstaller.git \
    $HOME/pyinstaller
WORKDIR /home/$BUSER/pyinstaller
RUN source $HOME/.bashrc ; pip install -U .

# set env variables

# clean up temp dir
USER root
RUN rm -rf /tmp/*

# update global file index
# useful for troubleshoting
RUN updatedb

# run all commands as builder by default
USER $BUSER
WORKDIR /home/$BUSER
