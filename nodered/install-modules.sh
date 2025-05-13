#!/bin/bash

cd /data
npm install --unsafe-perm --no-update-notifier --no-fund \
    node-red-dashboard \
    node-red-node-ui-table \
    node-red-contrib-ui-svg \
    node-red-contrib-postgresql \
    node-red-contrib-mqtt-broker 