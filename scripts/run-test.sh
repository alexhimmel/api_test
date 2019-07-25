#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASEDIR=${DIR}/../

# hrun ${BASEDIR}/testcases/basic_api_test/cloudinary_images
# hrun ${BASEDIR}testcases/basic_api_test/addon_service

hrun ${BASEDIR}/testcases/basic_api_test