#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <TARGET_IP>"
  exit 1
fi

TARGET_IP="$1"

for i in {1..11}
do
  nmap "$TARGET_IP" -sV -Pn
  sleep 0.5
done