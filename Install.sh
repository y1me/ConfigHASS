#!/bin/bash

if [ $EUID != 0 ]; then
    sudo "$0" "$@"
    exit $?
fi

if [[ $EUID -ne 0 ]]; then
    echo "You must be a root user" 
    exit 1
else
    echo "You are root"
fi

HERE=$(pwd)

cp -r ./usr /
cp -r ./etc /

systemctl enable LaunchScript.service
systemctl restart LaunchScript.service

echo "Install done!"
exit 0
