#!/bin/bash
INCUBATOR_HOME=/home/pi/incubator2
cd $INCUBATOR_HOME

if [ $USER != "root" ] ; then
    echo "Must be root"
    exit -1;
fi

if [ "$1" = "start" ] ; then
    echo "starting incubator"
    sudo modprobe w1-gpio
    sudo modprobe w1-therm
    sudo python $INCUBATOR_HOME/incubator/Incubator.py >> $INCUBATOR_HOME/incubator.log 2>&1 &
elif [ "$1" = "stop" ] ; then
#ps axf | grep python | grep -v grep | awk '{print "kill " $1}'

    PID=`ps axf | grep "sudo python $INCUBATOR_HOME/incubator/Incubator.py" | grep -v grep | awk '{print $1}'`
    kill "$PID"
    echo "Stopping incubator"
fi
