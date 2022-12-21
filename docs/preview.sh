#!/usr/bin/env bash
make html
xdg-open "file://$(pwd)/build/html/index.html"
