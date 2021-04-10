#!/bin/bash

OPENGATE="/usr/share/hassio/homeassistant/opengate"
while true; do
    if [ -f $OPENGATE ]; then
            echo "Open gate"
            rm $OPENGATE
            opengate.py
    fi
    sleep 1
done

