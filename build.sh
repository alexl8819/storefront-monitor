#!/usr/bin/env bash
set -e

rm -rf build
mkdir build

poetry export -f requirements.txt --output requirements.txt --without-hashes

pip install -r requirements.txt -t build
pip install . -t build

cp handler.py build/