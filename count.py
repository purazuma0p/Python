import time

def count_up_to(max):
    count = 1
    while count <= max:
        yield count
        count += 1    
for number in count_up_to(5):
    print(number)
    time.sleep(1)
    print("counting:", number)
    print("count up finished")
    