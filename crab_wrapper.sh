#!/usr/bin/env bash
crabConfig=$1
echo "crab submit --proxy=/tmp/x509up_u$(id -u) $@"
crab submit --proxy=/tmp/x509up_u$(id -u) $@
