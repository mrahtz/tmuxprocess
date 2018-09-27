#!/usr/bin/env bash

set -o errexit

git clean -df .
python3 setup.py sdist bdist_wheel
twine upload dist/*