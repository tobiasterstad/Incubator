#!/bin/bash
INCUBATOR_HOME=/home/pi/incubator2
cd $INCUBATOR_HOME

if [ $USER != "root" ] ; then
    echo "Must be root"
    exit -1;
fi

if [ "$1" = "start" ] ; then
    echo "Starting incubator"
    sudo modprobe w1-gpio
    sudo modprobe w1-therm
    sudo python $INCUBATOR_HOME/incubator/Incubator.py >> $INCUBATOR_HOME/incubator.log 2>&1 &
elif [ "$1" = "stop" ] ; then
    curl http://localhost:4000/shutdown
    echo "Stopping incubator"
fi
