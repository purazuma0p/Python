#!/usr/bin/env python3
import os
import sys
import time

user_input = input("update y or n: ").lower()
if user_input == "y":
   os.system('sudo apt update && clear')
   os.system('neofetch')
   x = 0
   while x < 20:
     x += 1
     print(f"\r{x}s<<<20s system loading countup ", end="")
     sys.stdout.flush()
     time.sleep(1)
     if x == 20:
        os.system('clear')
   print()

elif user_input == "n":
   os.system("clear")
else:
   print("Invalid input. Please enter 'y' or 'n'.")

