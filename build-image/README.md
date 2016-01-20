## Introduction

It builds a docker image for building ezbake projects.

## Prerequisite

Docker and docker machine tool must be installed and functional.
[Installing Docker](https://docs.docker.com/engine/installation/)

## How to use it

```bash
# create a machine
# cpu-count must >= 2 otherwise java run-time hangs when run
docker-machine create --driver virtualbox --virtualbox-memory 8192
--virtualbox-cpu-count 2 ezbuild
eval "$(docker-machine env ezbuild)"
docker build --force-rm=true --rm=true -t ezbuilder .
```

## Status

WIP
