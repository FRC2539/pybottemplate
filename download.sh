#!/bin/bash

curl --silent --retry 3 --retry-delay 1 --head http://google.com > /dev/null
if [[ "$?" -ne 0 ]]; then
    echo "No internet connection available"
    echo "Aborting..."
    return
fi

robotpy-installer download-robotpy
robotpy-installer download-opkg robotpy-rev
robotpy-installer download-opkg robotpy-ctre
robotpy-installer download-opkg robotpy-navx
robotpy_installer download-opkg commands-v1
