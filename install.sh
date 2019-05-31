#!/usr/bin/env bash

get_privilage() {
    if ! [ $(id -u) = 0 ]; then
        export REAL_USER=$(whoami)
        echo "Need root - sudoing..."
        exec su --preserve-environment -c "sh $0 $@"
    fi
}

export_var() {
    export SECRET_KEY="${SECRET_KEY}"
    export RECAPTCHA_PUBLIC_KEY="${RECAPTCHA_PUBLIC_KEY}"
    export RECAPTCHA_PRIVATE_KEY="${RECAPTCHA_PRIVATE_KEY}"
    export DATABASE_URL="${DATABASE_URL}"
}

get_env_file() {
    local  __resultvar=$1

    DEFAULT_ENV="./default_env.sh"
    CUSTOM_ENV="./custom_env.sh"

    if test -f "${CUSTOM_ENV}"; then
        eval $__resultvar="'${CUSTOM_ENV}'"
    else
        eval $__resultvar="'${DEFAULT_ENV}'"
    fi
}

load_env() {
    # https://www.linuxjournal.com/content/return-values-bash-functions
    get_env_file ENV_FILE

    # https://stackoverflow.com/a/36164878
    if [ -f ${ENV_FILE} ]; then
        echo "Reading user config...." >&2

        # check if the file contains something we don't want
        CONFIG_SYNTAX="(^\s*#|^\s*$|^\s*[a-z_][^[:space:]]*=[^;&\(\`]*$)"
        if egrep -q -iv "${CONFIG_SYNTAX}" "${ENV_FILE}"; then
            echo "Config file is unclean, Please  cleaning it..." >&2
            exit 1
        fi
        # now source it, either the original or the filtered variant
        . "${ENV_FILE}"
    else
        echo "There is no configuration file call \`${CUSTOM_ENV}\` or \`${DEFAULT_ENV}\`"
        exit 1
    fi
}

check_var() {
    case $FLASK_ENV in
        development|default)      
            ROLE_NAME=${PSQL_DEV_ROLE_NAME}
            ROLE_PWD=${PSQL_DEV_ROLE_PWD}
            DB_NAME=${PSQL_DEV_DB_NAME}
            DATABASE_URL=${PSQL_DEV_DATABASE_URL}
        ;;
        testing)      
            ROLE_NAME=${PSQL_DEV_ROLE_NAME}
            ROLE_PWD=${PSQL_DEV_ROLE_PWD}
            DB_NAME=${PSQL_DEV_DB_NAME}
            DATABASE_URL=${PSQL_TEST_DATABASE_URL}
        ;;
        production)
            ROLE_NAME=${PSQL_DEV_ROLE_NAME}
            ROLE_PWD=${PSQL_DEV_ROLE_PWD}
            DB_NAME=${PSQL_DEV_DB_NAME}
            DATABASE_URL=${PSQL_PROD_DATABASE_URL}
            ;; 
        *)
            echo "\`FLASK_ENV\` variable setting error, please set to 'development', 'testing' or 'production'."
            exit 1
        ;;
    esac
}

install_package() {
    # python3
    apt-get install -y python3 python3-dev python3-pip

    # python virtualenv
    apt-get install virtualenv

    # libpq-dev
    apt-get install -y libpq-dev

    # PostgreSQL
    apt-get install -y postgresql postgresql-contrib
    
    # PostGIS
    apt-get install -y postgis
}

make_virtualenv() {
    if [ ! -d "${VENV}" ]; then
        sudo -u ${REAL_USER} virtualenv ${VENV} --python=python3
        chown -R ${REAL_USER} ${VENV} 
    fi
    . ${VENV}/bin/activate

    # Install python package
    sudo -u ${REAL_USER} ${VENV}/bin/pip install -r requirements/common.txt
}

generate_supervisor_conf() {
    # https://stackoverflow.com/a/39563967
    # https://askubuntu.com/a/970898
    sudo -u ${REAL_USER} cat > supervisor/${SUPERVISOR_PROGRAM}.conf << EOF
[program:${SUPERVISOR_PROGRAM}]
user=${SUPERVISOR_USER}
directory=${SUPERVISOR_DIR}
command=${SUPERVISOR_DIR}/boot.sh

autostart=true
autorestart=true

stderr_logfile=/var/log/${SUPERVISOR_PROGRAM}/stderr.log
stdout_logfile=/var/log/${SUPERVISOR_PROGRAM}/stdout.log
EOF

    chown ${REAL_USER} supervisor/${SUPERVISOR_PROGRAM}.conf
}

generate_gunicorn_boot_script() {

    # https://www.howtogeek.com/howto/30184/10-ways-to-generate-a-random-password-from-the-command-line/
    SECRET_KEY=`date +%s | sha256sum | base64 | head -c 32`

    # https://stackoverflow.com/a/39563967
    sudo -u ${REAL_USER} cat > supervisor/boot_flask.sh << EOF
#!/usr/bin/env bash

$(`export_var`)

. ${VENV}/bin/activate
${VENV}/bin/gunicorn "app:create_app(\"${FLASK_ENV}\")" \\
    --bind ${GUNICORN_BIND_HOST}:${GUNICORN_BIND_PORT} \\
    --workers=$(( 2*$(nproc) + 1 )) \\
    --reload --max-requests 1
EOF

    chown ${REAL_USER} supervisor/boot_flask.sh
}

generate_testing_build_script () {
    sudo -u ${REAL_USER} cat > tests/build.sh << EOF
#!/usr/bin/env bash

$(`export_var`)

# Create production user
sudo -u postgres -H -- psql -c "SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = '${PSQL_TEST_ROLE_NAME}';" | grep -q 1 || sudo -u postgres -H -- psql -c  "CREATE ROLE ${PSQL_TEST_ROLE_NAME} LOGIN PASSWORD '${PSQL_TEST_ROLE_PWD}';"

# Create production database if not exists
sudo -u postgres -H -- psql -c "SELECT 1 FROM pg_database WHERE datname = '${PSQL_TEST_DB_NAME}';" | grep -q 1 || sudo -u postgres -H -- psql -c  "CREATE DATABASE ${PSQL_TEST_DB_NAME} OWNER ${PSQL_TEST_ROLE_NAME};"

# Create extension
sudo -u postgres -H -- psql -d ${PSQL_TEST_DB_NAME} -c "CREATE EXTENSION IF NOT EXISTS postgis;"

. ${VENV}/bin/activate
sudo -u ${REAL_USER} ${VENV}/bin/python manage.py db upgrade
EOF
    chown ${REAL_USER} tests/build.sh 
}

generate_deploy_script() {
    # https://stackoverflow.com/a/39563967
    sudo -u ${REAL_USER} cat > deploy.sh << EOF
#!/usr/bin/env bash

$(`export_var`)

# install supervisor
apt-get install -y supervisor

# install production requirements
. ${VENV}/bin/activate
${VENV}/bin/pip install -r requirements/prod.txt

# create production user
sudo -u postgres -H -- psql -c "SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = '${ROLE_NAME}';" | grep -q 1 || sudo -u postgres -H -- psql -c  "CREATE ROLE ${ROLE_NAME} LOGIN PASSWORD '${ROLE_PWD}';"

# create production database if not exists
sudo -u postgres -H -- psql -c "SELECT 1 FROM pg_database WHERE datname = '${DB_NAME}';" | grep -q 1 || sudo -u postgres -H -- psql -c  "CREATE DATABASE ${DB_NAME} OWNER ${ROLE_NAME};"

# create extension
sudo -u postgres -H -- psql -d ${DB_NAME} -c "CREATE EXTENSION IF NOT EXISTS postgis;"

# copy supervisor config
cp supervisor/${SUPERVISOR_FILE} /etc/supervisor/conf.d/${SUPERVISOR_FILE}

# make run_production executable
chmod u+x supervisor/boot.sh

# migrate database to newest
sudo -u ${REAL_USER} ${VENV}/bin/python manage.py db upgrade

# Start supervisor service
supervisorctl reread
service supervisor restart
EOF

    chown ${REAL_USER} deploy.sh
}

main() {
    get_privilage
    load_env
    check_var
    install_package
    make_virtualenv
    generate_supervisor_conf
    generate_gunicorn_boot_script
    generate_testing_build_script
    generate_deploy_script

    cp config_example.py config.py
}

main