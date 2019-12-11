#!/bin/bash

/usr/bin/uwsgi --ini /etc/myner.ini
/usr/bin/nginx
/usr/bin/nginx -s reload