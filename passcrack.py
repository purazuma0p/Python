#!/usr/bin/env python3
import os 
import sys
import time

RED = '\033[31m'
for password in open('password.txt'):
    password = password.strip()
    time.sleep(1)
    with open('password.txt') as f:
        for line in f:
            if password in line:
                print(RED + f"[＊]found:> {password}" )
                break
            time.sleep(0.01)
        # Simulate processing time
  
