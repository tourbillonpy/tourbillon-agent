#!/bin/sh
rm -f ../*.deb
dpkg-buildpackage -us -uc -tc
