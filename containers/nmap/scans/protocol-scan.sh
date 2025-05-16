#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <TARGET_IP>"
  exit 1
fi

TARGET_IP="$1"

for i in {1..32}
do
  nmap "$TARGET_IP" -p 1,2,17,132 -sO -Pn
done