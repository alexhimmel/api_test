#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

NAME="api-test"

APP_NAME=$1
APP_VERSION=$2

docker build -t $APP_NAME:${APP_VERSION} -f Dockerfile --force-rm .
