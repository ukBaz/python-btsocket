#!/usr/bin/env bash

# Ensure Python virtual environment is loaded
. venv/bin/activate

pycodestyle -v btsocket
lint_btsocket=$?
pycodestyle -v examples
lint_examples=$?

coverage run -m unittest discover -v tests
tests_result=$?

coverage report
coverage html
echo file://`pwd`/htmlcov/index.html

if [ $((lint_btsocket + lint_examples + tests_result)) -ne 0 ]; then
   echo -e "\n\n###  A test has failed!!  ###\n"
else
    echo -e "\n\nSuccess!!!\n"
fi
