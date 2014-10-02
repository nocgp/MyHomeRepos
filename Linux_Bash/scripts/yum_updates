#!/bin/sh

UPDATES_COUNT=$(yum list updates 2>/dev/null | grep `uname -p` | wc -l)
if [ -n "$UPDATES_COUNT" ]; then
        echo $UPDATES_COUNT > /tmp/yum_updates_qty
else
        echo 0 > /tmp/yum_updates_qty
fi

chmod 644 /tmp/yum_updates_qty
