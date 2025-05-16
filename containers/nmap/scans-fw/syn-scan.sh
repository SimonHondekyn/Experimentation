#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <TARGET_IP>"
  exit 1
fi

TARGET_IP="$1"

for i in {1..19}
do
  nmap "$TARGET_IP" -p 21,22,80,443,444 -Pn
done