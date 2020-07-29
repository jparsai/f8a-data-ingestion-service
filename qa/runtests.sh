#!/usr/bin/bash -ex

COVERAGE_THRESHOLD=60

export TERM=xterm
TERM=${TERM:-xterm}

# set up terminal colors
NORMAL=$(tput sgr0)
RED=$(tput bold && tput setaf 1)
GREEN=$(tput bold && tput setaf 2)
YELLOW=$(tput bold && tput setaf 3)
export DISABLE_AUTHENTICATION=1

printf "%sShutting down docker-compose ..." "${NORMAL}"

gc() {
  retval=$?
  docker-compose -f docker-compose.yml down -v || :
  exit $retval
}
trap gc EXIT SIGINT

# Enter local-setup/ directory
# Run local instances for: dynamodb, gremlin-websocket, gremlin-http
function start_ingestion_service {
    #pushd local-setup/
    echo "Invoke Docker Compose services"
    docker-compose -f docker-compose.yml up  --build --force-recreate -d
    #popd
}

start_ingestion_service

PYTHONPATH=$(pwd)/src
export PYTHONPATH

printf "%sCreate Virtualenv for Python deps ..." "${NORMAL}"

function prepare_venv() {
    VIRTUALENV=$(which virtualenv)
    if [ $? -eq 1 ]
    then
        # python34 which is in CentOS does not have virtualenv binary
        VIRTUALENV=$(which virtualenv-3)
    fi

    ${VIRTUALENV} -p python3 venv && source venv/bin/activate
    if [ $? -ne 0 ]
    then
        printf "%sPython virtual environment can't be initialized%s" "${RED}" "${NORMAL}"
        exit 1
    fi
}

prepare_venv

# now we are surely in the Python virtual environment

pip3 install -r requirements.txt
pip3 install git+https://github.com/fabric8-analytics/fabric8-analytics-worker.git@d403113
pip3 install git+https://github.com/fabric8-analytics/fabric8-analytics-auth.git@fff8f49
pip3 install radon==3.0.1
pip3 install pytest-flask

echo "*****************************************"
echo "*** Cyclomatic complexity measurement ***"
echo "*****************************************"
radon cc -s -a -i venv .
printf "%sCyclomatic complexity measurement passed%s\n\n" "${GREEN}" "${NORMAL}"

echo "*****************************************"
echo "*** Maintainability Index measurement ***"
echo "*****************************************"
radon mi -s -i venv .
printf "%sMaintainability Index measurement passed%s\n\n" "${GREEN}" "${NORMAL}"

echo "*****************************************"
echo "*** Unit tests ***"
echo "*****************************************"
python3 "$(which pytest)" --cov=src/ --cov-report term-missing --cov-fail-under=$COVERAGE_THRESHOLD -vv tests/
printf "%stests passed%s\n\n" "${GREEN}" "${NORMAL}"

codecov --token=357eac20-296a-434e-abca-0fdd7b3ccbdb

# deactivate virtual env before deleting it
deactivate
rm -rf venv/
