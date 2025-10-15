#!/usr/bin/env python3
import os 
import sys
import time

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
RESET = '\033[0m'
for password in open('password.txt'):
    password = password.strip()
    time.sleep(1)
    with open('password.txt') as f:
        for line in f:
            if password in line:
                print(RED + f"[＊]192.168.3.1>31.45.123.78:> {password}" + RESET)
                break
            time.sleep(0.01)
        # Simulate processing time
  