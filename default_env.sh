# python config
VENV="pyenv"

# flask config
FLASK_ENV="development"
RECAPTCHA_PUBLIC_KEY="enter_your_public_key"
RECAPTCHA_PRIVATE_KEY="enter_your_private_key"

# postgresql config
PSQL_DEV_ROLE_NAME="dev_user"
PSQL_DEV_ROLE_PWD="please_change_password"
PSQL_TEST_ROLE_NAME="test_user"
PSQL_TEST_ROLE_PWD="please_change_password"
PSQL_PROD_ROLE_NAME="prod_user"
PSQL_PROD_ROLE_PWD="please_change_password"
PSQL_DEV_DB_NAME="whereispts_dev"
PSQL_TEST_DB_NAME="whereispts_test"
PSQL_PROD_DB_NAME="whereispts"
PSQL_DEV_DATABASE_URL="postgresql://${PSQL_DEV_ROLE_NAME}:${PSQL_DEV_ROLE_PWD}@localhost/${PSQL_DEV_DB_NAME}"
PSQL_TEST_DATABASE_URL="postgresql://${PSQL_TEST_ROLE_NAME}:${PSQL_TEST_ROLE_PWD}@localhost/${PSQL_TEST_DB_NAME}"
PSQL_PROD_DATABASE_URL="postgresql://${PSQL_PROD_ROLE_NAME}:${PSQL_PROD_ROLE_PWD}@localhost/${PSQL_PROD_DB_NAME}"

# supervisor config
SUPERVISOR_PROGRAM="WhereIsPTS_API"
SUPERVISOR_FILE="${SUPERVISOR_PROGRAM}.conf"
SUPERVISOR_DIR="$PWD"
SUPERVISOR_USER="root"

# gunicorn config
GUNICORN_BIND_HOST="127.0.0.1"
GUNICORN_BIND_PORT="8080"

