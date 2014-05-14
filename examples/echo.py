#!/usr/bin/env python

import sys

while True:
  line = sys.stdin.readline()
  if not line or line.strip() in ('quit','exit','leave','bye'):
    break
  sys.stdout.write(line)

