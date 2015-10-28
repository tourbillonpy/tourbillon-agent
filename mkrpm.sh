#!/bin/sh
rm -f dist/*.rpm
rpmvenv --verbose redhat/tourbillon-rpm.json --destination dist --source .
