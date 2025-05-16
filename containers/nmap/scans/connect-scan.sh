#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <TARGET_IP>"
  exit 1
fi

TARGET_IP="$1"

for i in {1..81}
do
  nmap "$TARGET_IP" -sT -Pn
  sleep 1.2
done