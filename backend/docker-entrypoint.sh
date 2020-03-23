#!/bin/sh

if [ -n "$DB_URL" ]
    then
    url=`echo $DB_URL | awk -F[@//] '{print $4}'`
    database=`echo $url | awk -F[:] '{print $1}'`
    port=`echo $url | awk -F[:] '{print $2}'`
    echo "Waiting for $database:$port to be ready"
    while ! mysqladmin ping -h "$database" -P "$port" --silent; do
        echo -n '.';
        sleep 1;
    done
    echo;
    echo "$database is ready"
fi

exec gunicorn 'delivery:create_app()' \
    --bind '0.0.0.0:8000' \
    --workers $WORKERS \
    --worker-tmp-dir /dev/shm \
    --worker-class gevent \
    --access-logfile "$ACCESS_LOG" \
    --error-logfile "$ERROR_LOG"