#!/usr/bin/env python3
import os

user_input = input("update y or n: ").lower()

if user_input == "y":
    os.system("sudo apt update")
    os.system("clear")
    os.system("neofetch")
elif user_input == "n":
    os.system("clear")
    os.system("neofetch")
else:
    print("Invalid input. Please enter 'y' or 'n'.")

