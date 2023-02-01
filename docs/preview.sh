#!/usr/bin/env bash
BASEDIR=$(dirname "$0")
cd "$BASEDIR" || exit 1
make html
xdg-open "file://$(pwd)/build/html/index.html"
