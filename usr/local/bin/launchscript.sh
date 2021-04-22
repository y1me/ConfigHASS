#!/bin/bash

OPENGATE="/usr/share/hassio/homeassistant/opengate"
OPENGARAGE="/usr/share/hassio/homeassistant/opengarage"
OPENGARAGEHALF="/usr/share/hassio/homeassistant/opengaragehalf"
while true; do
    if [ -f $OPENGATE ]; then
            echo "Open gate"
            rm $OPENGATE
            opengate.py
    fi
    if [ -f $OPENGARAGE ]; then
            echo "Open garage"
            rm $OPENGARAGE
            opengarage.py
    fi
    if [ -f $OPENGARAGEHALF ]; then
            echo "Open garage"
            rm $OPENGARAGEHALF
            opengaragehalf.py
    fi
    sleep 1
done

