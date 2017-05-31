#!/bin/bash

celery multi start 2 -A web --logfile="/var/log/celery/%n%I.log" \
       --pidfile="/tmp/%n.pid" --loglevel=INFO
