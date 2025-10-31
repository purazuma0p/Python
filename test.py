#!usr/bin/env pythyon3
import os
import sys
import time

print("loop logic bomb!!....")
time.sleep(2)
def main():
    print("hello world")
    x = 0
    while x < 10:
        x += 1
        print(f"\r{x}s bomb!!", end = "")
        sys.stdout.flush()
        time.sleep(1)
        if x == 10:
             os.system('python3 c1.py')
             prihnt("this is loops bomb!!")

def time_sleep():
    for i in range(100):
        if i == 100:
            print(f"{i}logic bomb...... disanble")
            os.system("rm  program/python/c1.py")
        else:
            print(f"{i}loops.....")
time_sleep()
main()


