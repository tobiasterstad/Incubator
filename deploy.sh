#!/bin/sh
rsync -av --exclude incubator.log --exclude incubator.properties src/* pi@incubator:incubator/