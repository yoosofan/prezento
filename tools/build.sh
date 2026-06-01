#!/bin/bash
function common_tasks1(){
    bash ./tools/clean.sh
    rsync -av --delete ~/research/projects/prezento/ ~/temp/prz/
    #uv tool uninstall --all
    #uv cache clean
    uv tool uninstall prezento
    uv cache clean prezento
    uv tool install ~/temp/prz/
}

function run22(){
    common_tasks1
    cd ~/research/projects/slide/
    prezento os.mem.rst
}

run22
# source /home/ahmad/install/uv.virtual.environments/p3.14.3/bin/activate
#bildumilo_test_run

: <<'COMMENT11'
uv self update
uv tool upgrade --all

uv tool install black
black . --check
black .

uv tool install ruff@latest

ruff check
ruff check --fix

uv tool install flake8
flake8 .
flake8 . --ignore=E501,W503,E203

uv tool install autopep8
autopep8 --in-place --aggressive  --recursive --list-fixes --max-line-length 79 .

# build by uv

uv build

# uv publish dist/*
# uv publish --token <your_pypi_token>

# build by wheel
# python -m build

uv tool install build
uv tool install wheel
uv tool install twine

twine check --strict dist/*
twine upload dist/*

COMMENT11
