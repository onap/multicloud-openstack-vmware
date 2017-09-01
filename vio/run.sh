#!/bin/bash

sed -i "s/MSB_SERVICE_IP =.*/MSB_SERVICE_IP = \"${MSB_ADDR}\"/g" vio/pub/config/config.py
sed -i "s/MSB_SERVICE_PORT =.*/MSB_SERVICE_PORT = \"${MSB_PORT}\"/g" vio/pub/config/config.py
sed -i "s/AAI_ADDR =.*/AAI_ADDR = \"${AAI_ADDR}\"/g" vio/pub/config/config.py
sed -i "s/AAI_PORT =.*/AAI_PORT = \"${AAI_PORT}\"/g" vio/pub/config/config.py
sed -i "s/AAI_SCHEMA_VERSION =.*/AAI_SCHEMA_VERSION = \"${AAI_SCHEMA_VERSION}\"/g" vio/pub/config/config.py
sed -i "s/AAI_USERNAME =.*/AAI_USERNAME = \"${AAI_USERNAME}\"/g" vio/pub/config/config.py
sed -i "s/AAI_PASSWORD =.*/AAI_PASSWORD = \"${AAI_PASSWORD}\"/g" vio/pub/config/config.py

nohup python manage.py runserver 0.0.0.0:9004 2>&1 &

while [ ! -f logs/runtime_vio.log ]; do
    sleep 1
done

tail -F logs/runtime_vio.log
