#!/bin/bash

raspivid -f -t 0 -w 790 -h 470 &
PID=$(($$+1))

getXY () {
	local inputNum=$(xinput --list | sed -n "s/^.*FT5406.*=\([0-9]*\).*/\1/p")
	local output=$(xinput --query-state $inputNum)
	local x=$(echo $output | sed -n "s/^.*valuator\[0\]=\([0-9]*\).*$/\1/p")
	local y=$(echo $output | sed -n "s/^.*valuator\[1\]=\([0-9]*\).*$/\1/p")
	xy="$x, $y"
}

getXY
while true; do
	lxy=$xy
	getXY
	if [ "$lxy" != "$xy" ]; then
		kill -9 $PID
		break
	fi
done
